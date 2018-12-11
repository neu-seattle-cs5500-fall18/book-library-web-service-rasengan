import datetime
from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.api_models import loan_model
from api.parsers import book_loan_parser
from database import db
from database.db_models import Book as BookDBModel, Borrower as BorrowerDBModel
from mail import send_reminder_mail

ns = api.namespace('loan', description='Operations with respect to loaning a book')


@ns.route('/')
@api.doc(description='List of books loaned. \n\n ')
class LoanedBooks(Resource):
    @api.marshal_with(loan_model, as_list=True)
    @api.doc(description='Get List of books loaned . \n\n ')
    def get(self):
        """ Get all lent books """
        try:
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
            return loaned_books, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_loan_parser, validate=True)
    @api.marshal_with(loan_model)
    @api.doc(description='Lend a book to a borrower . \n\n ')
    def post(self):
        """ Loan a book """
        try:
            args = book_loan_parser.parse_args()
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            book.to_be_returned_on = datetime.datetime.now() + datetime.timedelta(days=10)
            book.is_returned = False
            result = book.to_dict()
            result['return_status'] = 'Not late'
            db.session.commit()
            return result, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_loan_parser, validate=True)
    @api.marshal_with(loan_model)
    @api.response(HTTPStatus.OK, 'Returned book successfully')
    @api.doc(description='Mark a lent book as returned . \n\n ')
    def delete(self):
        """ Return a book """
        try:
            args = book_loan_parser.parse_args()
            book = BookDBModel.query.get(args['book_id'])
            book.lent_to = args['lent_to']
            book.is_returned = True
            result = book.to_dict()
            result['return_status'] = 'No issues with return'
            db.session.commit()
            return result, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST


@ns.route('/remind')
@api.doc(description='Remind for a particular lent book. \n\n ')
class LoanReminder(Resource):
    @api.expect(book_loan_parser, validate=True)
    @api.response(HTTPStatus.OK, 'Mail sent successfully')
    @api.doc(description='Remind borrower for a book . \n\n ')
    def post(self):
        """ Loan a book """
        try:
            args = book_loan_parser.parse_args()
            book = BookDBModel.query.get(args['book_id'])
            borrower = BorrowerDBModel.query.get(args['lent_to'])
            send_reminder_mail(borrower.email, book.title)
            return {'success': True}, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST
