import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


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
