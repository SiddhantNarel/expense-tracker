import os
import re
import sqlite3

_db_path = None


def set_db_path(path):
    global _db_path
    _db_path = path


def get_db_path():
    return _db_path or os.environ.get('DATABASE_PATH', 'expense_tracker.db')


def _is_postgres():
    url = os.environ.get('DATABASE_URL', '')
    return url.startswith('postgres://') or url.startswith('postgresql://')


def _postgres_url():
    url = os.environ.get('DATABASE_URL', '')
    # Render uses postgres:// but psycopg2 requires postgresql://
    if url.startswith('postgres://'):
        url = 'postgresql://' + url[len('postgres://'):]
    return url


_INSERT_RE = re.compile(r'^\s*INSERT\b', re.IGNORECASE)
_RETURNING_RE = re.compile(r'\bRETURNING\b', re.IGNORECASE)


def _adapt_query(query):
    """Convert SQLite SQL syntax to PostgreSQL-compatible SQL."""
    # Parameter placeholders
    query = query.replace('?', '%s')
    # AUTOINCREMENT → SERIAL (schema)
    query = re.sub(
        r'\bINTEGER PRIMARY KEY AUTOINCREMENT\b', 'SERIAL PRIMARY KEY', query, flags=re.IGNORECASE
    )
    # datetime function
    query = re.sub(r"datetime\('now'\)", 'NOW()', query, flags=re.IGNORECASE)
    query = re.sub(r"DEFAULT \(datetime\('now'\)\)", 'DEFAULT NOW()', query, flags=re.IGNORECASE)
    # strftime date formatting
    query = re.sub(
        r"strftime\('%Y-%m',\s*(\w+)\)", r'substring(\1, 1, 7)', query, flags=re.IGNORECASE
    )
    query = re.sub(
        r"strftime\('%Y-W%W',\s*(\w+)\)", r"to_char(\1::date, 'IYYY-IW')", query, flags=re.IGNORECASE
    )
    # NULL-safe equality: IS %s → IS NOT DISTINCT FROM %s
    query = re.sub(r'\bIS\s+%s\b', 'IS NOT DISTINCT FROM %s', query)
    # INSERT OR IGNORE → INSERT ... ON CONFLICT DO NOTHING
    if re.search(r'\bINSERT\s+OR\s+IGNORE\s+INTO\b', query, re.IGNORECASE):
        query = re.sub(
            r'\bINSERT\s+OR\s+IGNORE\s+INTO\b', 'INSERT INTO', query, flags=re.IGNORECASE
        )
        if 'ON CONFLICT' not in query.upper():
            query = query.rstrip(';').rstrip() + ' ON CONFLICT DO NOTHING'
    return query


class _PGCursorProxy:
    """Wraps a psycopg2 RealDictCursor to expose a sqlite3-like interface."""

    def __init__(self, cursor):
        self._c = cursor
        self.lastrowid = None

    def execute(self, query, params=None):
        adapted = _adapt_query(query)
        is_insert = bool(_INSERT_RE.match(adapted))
        has_returning = bool(_RETURNING_RE.search(adapted))
        if is_insert and not has_returning:
            adapted = adapted.rstrip(';').rstrip() + ' RETURNING id'
            self._c.execute(adapted, params or [])
            row = self._c.fetchone()
            self.lastrowid = row['id'] if row else None
        else:
            self._c.execute(adapted, params or [])
        return self

    def fetchone(self):
        return self._c.fetchone()

    def fetchall(self):
        return self._c.fetchall()

    def __iter__(self):
        return iter(self._c)


class _PGConnectionProxy:
    """Wraps a psycopg2 connection to expose a sqlite3-like interface."""

    def __init__(self, pg_conn):
        import psycopg2.extras
        self._conn = pg_conn
        self._cursor_factory = psycopg2.extras.RealDictCursor

    def cursor(self):
        return _PGCursorProxy(self._conn.cursor(cursor_factory=self._cursor_factory))

    def execute(self, query, params=None):
        c = self.cursor()
        c.execute(query, params)
        return c

    def executescript(self, script):
        """Execute multiple semicolon-separated SQL statements (SQLite compat)."""
        import psycopg2.extras
        raw_cursor = self._conn.cursor()
        for stmt in script.split(';'):
            stmt = stmt.strip()
            if stmt:
                raw_cursor.execute(_adapt_query(stmt))

    def commit(self):
        self._conn.commit()

    def close(self):
        self._conn.close()


def get_connection():
    if _is_postgres():
        import psycopg2
        import psycopg2.extras
        conn = psycopg2.connect(_postgres_url())
        return _PGConnectionProxy(conn)
    path = get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute('PRAGMA foreign_keys = ON')
    return conn


def init_db():
    conn = get_connection()

    schema_sql = """
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            emoji TEXT DEFAULT '',
            color TEXT DEFAULT '#6366f1',
            is_custom INTEGER DEFAULT 0,
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS expenses (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            category_id INTEGER,
            date TEXT NOT NULL,
            description TEXT DEFAULT '',
            payment_method TEXT DEFAULT 'Cash',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE SET NULL
        );

        CREATE TABLE IF NOT EXISTS income (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            amount REAL NOT NULL,
            source TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            updated_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS friends (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT DEFAULT '',
            notes TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now'))
        );

        CREATE TABLE IF NOT EXISTS loan_transactions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            friend_id INTEGER NOT NULL,
            type TEXT NOT NULL CHECK(type IN ('gave','received','settlement')),
            amount REAL NOT NULL,
            date TEXT NOT NULL,
            description TEXT DEFAULT '',
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (friend_id) REFERENCES friends(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS budgets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            category_id INTEGER,
            amount REAL NOT NULL,
            month INTEGER NOT NULL,
            year INTEGER NOT NULL,
            created_at TEXT DEFAULT (datetime('now')),
            FOREIGN KEY (category_id) REFERENCES categories(id) ON DELETE CASCADE
        );

        CREATE TABLE IF NOT EXISTS settings (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key TEXT UNIQUE NOT NULL,
            value TEXT NOT NULL
        )
    """

    if _is_postgres():
        conn.executescript(schema_sql)
    else:
        c = conn.cursor()
        c.executescript(schema_sql)

    # Seed default categories
    default_categories = [
        ('Food & Dining', '🍔', '#f59e0b', 0),
        ('Transport', '🚗', '#3b82f6', 0),
        ('Entertainment', '🎬', '#8b5cf6', 0),
        ('Shopping', '🛒', '#ec4899', 0),
        ('Bills & Utilities', '💡', '#06b6d4', 0),
        ('Health', '🏥', '#10b981', 0),
        ('Education', '📚', '#6366f1', 0),
        ('Groceries', '🛍️', '#84cc16', 0),
        ('Subscriptions', '📱', '#f97316', 0),
        ('Gym & Fitness', '🏋️', '#14b8a6', 0),
        ('Coffee', '☕', '#92400e', 0),
        ('Personal Care', '💇', '#db2777', 0),
        ('Gifts', '🎁', '#dc2626', 0),
        ('Miscellaneous', '📦', '#6b7280', 0),
    ]
    for name, emoji, color, is_custom in default_categories:
        conn.execute(
            "INSERT OR IGNORE INTO categories (name, emoji, color, is_custom) "
            "SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name=? AND is_custom=0)",
            (name, emoji, color, is_custom, name)
        )

    # Seed default settings
    conn.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('dark_mode', 'false')")

    conn.commit()
    conn.close()
