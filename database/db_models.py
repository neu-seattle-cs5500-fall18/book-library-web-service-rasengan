import datetime

from database import db


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

    def __init__(self, title, author, genre, published_on,notes):
        self.title = title
        self.author = author
        self.genre = genre
        self.published_on = published_on
        self.notes = notes

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
    email = db.Column(db.String(100))

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def to_dict(self):
        borrower_dict = {}
        for c in self.__table__.columns:
            borrower_dict[c.name] = getattr(self, c.name, None)
        return borrower_dict


class List(db.Model):
    list_id = db.Column('list_id', db.Integer, primary_key=True)
    description = db.Column(db.String(100))

    def __init__(self, description):
        self.description = description

    def to_dict(self):
        list_dict = {}
        for c in self.__table__.columns:
            list_dict[c.name] = getattr(self, c.name, None)
        return list_dict


class ListBook(db.Model):
    list_id = db.Column('list_id', db.Integer, primary_key=True, autoincrement=False)
    book_id = db.Column('book_id', db.Integer, primary_key=True, autoincrement=False)

    def __init__(self, list_id, book_id):
        self.list_id = list_id
        self.book_id = book_id

    def to_dict(self):
        list_book_dict = {}
        for c in self.__table__.columns:
            list_book_dict[c.name] = getattr(self, c.name, None)
        return list_book_dict
