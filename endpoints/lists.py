from http import HTTPStatus

from flask_restplus import Resource
from datetime import datetime
from api import api
from api.api_models import bookModel, postModel
from api.parsers import book_parser,book_get_parser, book_update_parser, list_get_parser
from database import db
from database.db_models import Book as BookModel

ns = api.namespace('bookslist', description='Operations with respect to books list')

@ns.route('/')
@api.doc(description='Get all lists of books with \n\n ')
class Lists(Resource):
    @api.expect(list_get_parser, validate=False)
    @api.doc(description='Get List of books . \n\n ')
    def get(self):
        """ Get all books """
        result = {}
        lists = []
        # args = list_get_parser.parse_args()
        # resp_query = ListsModel.query
        # if args['author']:
        #     resp_query = resp_query.filter_by(author=args['author'])
