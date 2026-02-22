import os

class Config:
    DATABASE_PATH = os.environ.get('DATABASE_PATH', 'expense_tracker.db')
    DEBUG = os.environ.get('DEBUG', 'True') == 'True'
    TESTING = False

class TestingConfig(Config):
    TESTING = True
    DATABASE_PATH = ':memory:'
