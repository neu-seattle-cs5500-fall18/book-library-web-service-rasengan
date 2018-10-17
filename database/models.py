import datetime

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Book(db.Model):
    book_id = db.Column('book_id', db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    author = db.Column(db.String(50), nullable=False)
    genre = db.Column(db.String(200), nullable=False)
    published_on = db.Column(db.DateTime, default=datetime.datetime.utcnow)
    notes = db.Column(db.String(50), default="")
    lent_to = db.Column(db.Integer, default=None)
    to_be_returned_on = db.Column(db.DateTime, default=None)
    is_returned = db.Column(db.Boolean, default=False)

    def __init__(self, title, author, genre, published_on):
        self.title = title
        self.author = author
        self.genre = genre
        self.published_on = published_on

    def to_dict(self):
        book_dict = {}
        for c in self.__table__.columns:
            if getattr(self, c.name, None):
                if c.name == 'published_on' or c.name == 'to_be_returned_on':
                    book_dict[c.name] = getattr(self, c.name, None).isoformat()
                else:
                    book_dict[c.name] = getattr(self, c.name, None)
        return book_dict


class Borrower(db.Model):
    borrower_id = db.Column('borrower_id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))

    def __init__(self, name):
        self.name = name

    def to_dict(self):
        borrower_dict = {}
        for c in self.__table__.columns:
            borrower_dict[c.name] = getattr(self, c.name, None)
        return borrower_dict
