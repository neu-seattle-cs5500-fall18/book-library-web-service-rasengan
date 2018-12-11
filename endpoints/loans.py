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
        """ Get all lent books """
        try:
            result = {}
            loaned_books = []

            resp = BookDBModel.query.filter(BookDBModel.lent_to.isnot(None)).all()
            if not resp:
                return []
            for x in resp:
                book = x.to_dict()
                if book.get('to_be_returned_on') and 'is_returned' not in book:
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
            return result, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_loan_parser, validate=True)
    @api.response(HTTPStatus.OK, 'Loaned book successfully')
    @api.doc(description='Lend a book to a borrower . \n\n ')
    def post(self):
        """ Loan a book """
        try:
            args = book_loan_parser.parse_args()
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            book.to_be_returned_on = datetime.datetime.now() + datetime.timedelta(days=10)
            book.is_returned = False
            db.session.commit()
            return book.to_dict(), HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_loan_parser, validate=True)
    @api.response(HTTPStatus.OK, 'Returned book successfully')
    @api.doc(description='Mark a lent book as returned . \n\n ')
    def delete(self):
        """ Return a book """
        try:
            args = book_loan_parser.parse_args()
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            book.is_returned = True
            db.session.commit()
            return book.to_dict(), HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST
