from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.parsers import book_loan_parser
from database import db
from database.db_models import Book as BookDBModel

ns = api.namespace('loan', description='Operations with respect to loaning a book')


@ns.route('/')
@api.doc(description='List of books loaned. \n\n ')
class LoanedBooks(Resource):
    @api.doc(description='Get List of books loaned . \n\n ')
    def get(self):
        result = {}
        loaned_books = []

        resp = BookDBModel.query.filter(BookDBModel.lent_to.isnot(None)).all()
        if not resp:
            return []
        for x in resp:
            loaned_books.append(x.to_dict())
        result['loaned_books'] = loaned_books
        return result

    @api.expect(book_loan_parser, validate=True)
    @api.response(HTTPStatus.OK, 'Updated')
    @api.doc(description='Lend a book to a borrower . \n\n ')
    def post(self):
        """ add borrower """
        args = book_loan_parser.parse_args()
        if args['book_id'] and args['lent_to']:
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            db.session.commit()
        return {'success': True}
