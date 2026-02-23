import pytest
import tempfile
import os
from app import create_app


@pytest.fixture
def app():
    tf = tempfile.NamedTemporaryFile(suffix='.db', delete=False)
    tf.close()
    app = create_app({
        'TESTING': True,
        'DATABASE_PATH': tf.name,
        'JWT_SECRET_KEY': 'test-secret-key',
    })
    yield app
    os.unlink(tf.name)


@pytest.fixture
def client(app):
    with app.app_context():
        from flask_jwt_extended import create_access_token
        token = create_access_token(identity='admin')

    flask_client = app.test_client()
    auth_header = {'Authorization': f'Bearer {token}'}

    class AuthTestClient:
        """Wraps Flask test client to automatically inject a JWT Authorization header."""

        def _h(self, kwargs):
            headers = dict(kwargs.pop('headers', None) or {})
            headers.update(auth_header)
            kwargs['headers'] = headers
            return kwargs

        def get(self, *args, **kwargs):
            return flask_client.get(*args, **self._h(kwargs))

        def post(self, *args, **kwargs):
            return flask_client.post(*args, **self._h(kwargs))

        def put(self, *args, **kwargs):
            return flask_client.put(*args, **self._h(kwargs))

        def delete(self, *args, **kwargs):
            return flask_client.delete(*args, **self._h(kwargs))

    return AuthTestClient()
