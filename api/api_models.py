from flask_restplus import fields

from api import api

book_model = api.model('A book model', {
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

borrower_model = api.model('A borrower model', {
    "borrower_id": fields.Integer,
    "name": fields.String,
    "email": fields.String
})

success_model = api.model('A successful request', {
    "success": fields.Boolean
})

loan_model = api.inherit('A loan model', book_model, {
    "return_status": fields.String
})

list_model = api.model('A book list', {
    "list_id": fields.Integer,
    "description": fields.String,
    "book_ids": fields.List(fields.Integer)
})
