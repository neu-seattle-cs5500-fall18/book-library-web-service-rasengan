from http import HTTPStatus

import pytest

from run import application

sample_book = {
    'book_id': '1',
    'title': 'Test',
    'author': 'Survi',
    'genre': 'Mathenatics',
}

sample_borrower = {
    'borrower_id': '1',
    'name': 'aditya',
    'email': 'abcd@gmail.com',
}

sample_list = {
    'list_id': '1',
    'description': 'My fav books',
}


@pytest.fixture
def client():
    application.config['TESTING'] = True
    return application.test_client()


def test_hello_world(client):
    resp = client.get('/')
    assert resp.get_data(as_text=True) == 'Hello Rasengan'


def test_doc(client):
    resp = client.get('/doc', follow_redirects=True)
    assert resp.status_code == HTTPStatus.OK


def test_book(client):
    resp = client.get('/doc/books/' + sample_book['book_id'], follow_redirects=True)
    book = resp.get_json()
    assert book['title'] == sample_book['title']
    assert book['author'] == sample_book['author']
    assert book['genre'] == sample_book['genre']


def test_borrower(client):
    resp = client.get('/doc/borrowers/' + sample_borrower['borrower_id'], follow_redirects=True)
    book = resp.get_json()
    assert book['name'] == sample_borrower['name']
    assert book['email'] == sample_borrower['email']


def test_list(client):
    resp = client.get('/doc/lists/' + sample_list['list_id'], follow_redirects=True)
    book = resp.get_json()
    assert book['description'] == sample_list['description']
