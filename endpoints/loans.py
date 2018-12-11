import datetime
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
            book = x.to_dict()
            if book.get('to_be_returned_on', None) and 'is_returned' not in book:
                today = datetime.datetime.now()
                to_be_returned_on = datetime.datetime.fromisoformat(book['to_be_returned_on'])
                if today < to_be_returned_on:
                    book['return_status'] = 'Not late'
                else:
                    book['return_status'] = 'Late'
            else:
                book['return_status'] = 'No issues with return'
            loaned_books.append(book)
        result['loaned_books'] = loaned_books
        return result

    @api.expect(book_loan_parser, validate=True)
    @api.response(HTTPStatus.OK, 'Loaned')
    @api.doc(description='Lend a book to a borrower . \n\n ')
    def post(self):
        """ loaned book """
        args = book_loan_parser.parse_args()
        if args.get('book_id') and args.get('lent_to'):
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            if args.get('is_borrowing', 'false') == "true":
                book.to_be_returned_on = datetime.datetime.now() + datetime.timedelta(days=10)
                book.is_returned = False
            else:
                book.is_returned = True
            db.session.commit()
        return {'success': True}
