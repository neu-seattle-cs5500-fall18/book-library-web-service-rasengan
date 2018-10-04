import datetime
from http import HTTPStatus

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = 'postgres://mtwahsiiuuodov:ea5fbd9f4720b2ddfbc9998cd490f8be902e86a01aa8b8b5e0fc31dc904f8219@ec2-50-17-225-140.compute-1.amazonaws.com:5432/dc86b8ec8qdppu'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @app.route('/')
    def hello_world():
        return jsonify(response='Hello World! Heroku deployed'), HTTPStatus.OK

    @app.route('/add')
    def record_add():
        db.create_all()
        borrower1 = Borrower("Survi")
        db.session.add(borrower1)
        db.session.commit()
        return jsonify(response='Successfully added'), HTTPStatus.CREATED

    @app.route('/show')
    def record_show():
        test_record = Borrower.query.filter_by(name='Survi').first()
        print(test_record.id, " ", test_record.name)
        return test_record.name

    @app.route('/delete')
    def record_delete():
        record = record_show()
        before_delete = Borrower.query.filter_by(name=record).first()
        db.session.delete(before_delete)
        db.session.commit()
        after_delete = Borrower.query.filter_by(name="Survi").first()
        print(after_delete.id)
        return "Successfully deleted"

    db.init_app(app)
    return app


class Book(db.Model):
    id = db.Column('book_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    author = db.Column(db.String(50))
    genre = db.Column(db.String(200))
    published_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    notes = db.Column(db.String(50))
    lent_to = db.Column(db.Integer)
    to_be_returned_on = db.Column(db.DateTime)
    is_returned = db.Column(db.Boolean)

    def __init__(self, title, author, genre, published_on, notes, lent_to, to_be_returned_on, is_returned):
        self.title = title
        self.author = author
        self.genre = genre
        self.published_on = published_on
        self.notes = notes
        self.lent_to = lent_to
        self.to_be_returned_on = to_be_returned_on
        self.is_returned = is_returned


class Borrower(db.Model):
    id = db.Column('borrower_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name


application = create_app()


if __name__ == '__main__':
    application.run()
