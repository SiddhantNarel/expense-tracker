import pytest
import tempfile
import os
from app import create_app


@pytest.fixture
def app():
    tf = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    tf.close()
    app = create_app({'TESTING': True, 'DATABASE_PATH': tf.name})
    yield app
    os.unlink(tf.name)


@pytest.fixture
def client(app):
    return app.test_client()
