import tempfile
import os
from flask import Flask
from flask_cors import CORS
from app.database import init_db, set_db_path


def create_app(config=None):
    app = Flask(__name__)

    if config:
        app.config.update(config)

    if app.config.get('TESTING') and app.config.get('DATABASE_PATH') == ':memory:':
        # For in-memory testing we can't share a single connection across requests easily,
        # so we use a temp file per test session instead
        tf = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
        tf.close()
        set_db_path(tf.name)
        app.config['_tmp_db'] = tf.name
    elif app.config.get('DATABASE_PATH'):
        set_db_path(app.config['DATABASE_PATH'])

    CORS(app, resources={r"/api/*": {"origins": "*"}})

    init_db()

    from app.routes.expenses import expenses_bp
    from app.routes.income import income_bp
    from app.routes.loans import loans_bp
    from app.routes.budgets import budgets_bp
    from app.routes.categories import categories_bp
    from app.routes.analytics import analytics_bp
    from app.routes.export import export_bp
    from app.routes.settings import settings_bp

    app.register_blueprint(expenses_bp, url_prefix='/api')
    app.register_blueprint(income_bp, url_prefix='/api')
    app.register_blueprint(loans_bp, url_prefix='/api')
    app.register_blueprint(budgets_bp, url_prefix='/api')
    app.register_blueprint(categories_bp, url_prefix='/api')
    app.register_blueprint(analytics_bp, url_prefix='/api')
    app.register_blueprint(export_bp, url_prefix='/api')
    app.register_blueprint(settings_bp, url_prefix='/api')

    return app
