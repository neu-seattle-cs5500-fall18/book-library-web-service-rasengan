from flask_restplus import fields

from api import api

bookModel = api.model('bookModel', {
    "book_id": fields.Integer,
    "title": fields.String,
    "author": fields.String,
    "genre": fields.String,
    "published_on": fields.Date,
    "notes": fields.String,
    "lent_to": fields.Integer,
    "to_be_returned_on": fields.Date,
    "is_returned": fields.Boolean
})

booksModel = api.model('booksModel', {
    "books": fields.List(fields.Nested(bookModel))
})

borrowerModel = api.model('borrowerModel', {
    "borrower_id": fields.Integer,
    "name": fields.String,
    "email": fields.String
})

borrowersModel = api.model('borrowersModel', {
    "borrowers": fields.List(fields.Nested(borrowerModel))
})

successModel = api.model('successModel', {
    "success": fields.Boolean
})
