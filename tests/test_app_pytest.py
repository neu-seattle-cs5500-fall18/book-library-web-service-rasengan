from http import HTTPStatus

import pytest

from app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    yield app.test_client()


def test_hw(client):
    res = client.get('/')
    assert res.status_code == HTTPStatus.OK
    assert res.json == {'response': 'Hello World! Heroku deployed'}


def test_add(client):
    res = client.get('/add')
    assert res.status_code == HTTPStatus.CREATED
    assert res.json == {'response': 'Successfully added'}
