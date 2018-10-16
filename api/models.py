from flask_restplus import fields


# Model definition
class ApiModel:
    def __init__(self, api):
        self.bookModel = api.model('bookModel', {
            "id": fields.Integer,
            "title": fields.String,
            "author": fields.String,
            "genre": fields.String,
            "published_on": fields.Date,
            "notes": fields.String,
            "lent_to": fields.Integer,
            "to_be_returned_on": fields.Date,
            "is_returned": fields.Boolean
        }),
        self.booksModel = api.model('booksModel', {
            "books": fields.List(fields.Nested(self.bookModel))
        })

        self.borrowerModel = api.model('borrowerModel',{
            "id": fields.Integer,
            "name": fields.String
        })

        self.postModel = api.model('postModel', {
            "success": fields.Boolean
        })