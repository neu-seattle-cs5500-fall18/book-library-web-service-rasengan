from http import HTTPStatus

from flask import (
    Blueprint, jsonify, request
)


from database.models import db, Book
book_app = Blueprint('book_app', __name__)


@book_app.route('/')
def show():
    return jsonify(response='Book stuff'), HTTPStatus.OK


@book_app.route('/add', methods=['POST'])
def add():
    content = request.get_json()
    book = Book(content['title'], content['author'], content['genre'], content['published_on'])
    db.session.add(book)
    db.session.commit()
    return jsonify(response='Successfully added'), HTTPStatus.CREATED


@book_app.route('/all')
def record_show():
    test_records = Book.query.all()
    for record in test_records:
        print(str(record.id)+" "+record.title+" "+record.author+" "+record.genre+" "+record.notes)
    return jsonify(response=str(len(test_records))), HTTPStatus.OK


@book_app.route('/delete', methods=['POST'])
def record_delete():
    content = request.get_json()
    if 'title' in content:
        record = Book.query.filter_by(title=content['title']).first()
        db.session.delete(record)
        db.session.commit()
        return jsonify(response='Successfully deleted'), HTTPStatus.OK
    else:
        return jsonify(response='Needs a book title to delete'), HTTPStatus.BAD_REQUEST


@book_app.route('/update', methods=['POST'])
def record_update():
    content = request.get_json()
    if 'title' in content:
        record = Book.query.filter_by(title=content['title']).first()
    if 'genre' in content:
        record.genre = content['genre']
    if 'author' in content:
        record.author = content['author']
    if 'published_on' in content:
        record.published_on = content['published_on']
    if 'notes' in content:
        record.notes = content['notes']
    if 'lent_to' in content:
        record.lent_to = content['lent_to']
    if 'to_be_returned_on' in content:
        record.to_be_returned_on = content['to_be_returned_on']
    if 'is_returned' in content:
        record.is_returned = content['is_returned']
    db.session.commit()
    return jsonify(response='Successfully updated'), HTTPStatus.OK


