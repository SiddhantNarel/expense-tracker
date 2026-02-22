import sqlite3
import os

_db_path = None


def set_db_path(path):
    global _db_path
    _db_path = path


def get_db_path():
    return _db_path or os.environ.get('DATABASE_PATH', 'expense_tracker.db')


def get_connection():
    path = get_db_path()
    conn = sqlite3.connect(path)
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db():
    conn = get_connection()
    c = conn.cursor()

    c.executescript("""
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
        );
    """)

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
        c.execute(
            "INSERT OR IGNORE INTO categories (name, emoji, color, is_custom) "
            "SELECT ?, ?, ?, ? WHERE NOT EXISTS (SELECT 1 FROM categories WHERE name=? AND is_custom=0)",
            (name, emoji, color, is_custom, name)
        )

    # Seed default settings
    c.execute("INSERT OR IGNORE INTO settings (key, value) VALUES ('dark_mode', 'false')")

    conn.commit()
    conn.close()
