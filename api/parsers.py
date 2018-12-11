from flask_restplus import reqparse

# Request Parsing
book_parser = reqparse.RequestParser()
book_parser.add_argument('title', required=True, help='name of book', location='args')
book_parser.add_argument('author', required=True, help='name of author', location='args')
book_parser.add_argument('genre', required=True, help='book genre', location='args')
book_parser.add_argument('published_on', required=True, help='book publication date', location='args')
book_parser.add_argument('notes',required=False, help='notes about the book', location='args')

book_update_parser = reqparse.RequestParser()
book_update_parser.add_argument('title', required=False, help='name of book', location='args')
book_update_parser.add_argument('author', required=False, help='author of book', location='args')
book_update_parser.add_argument('genre', required=False, help='genre of book', location='args')
book_update_parser.add_argument('published_on', required=False, help='book publication date', location='args')
book_update_parser.add_argument('notes', required=False, help='notes for book', location='args')
book_update_parser.add_argument('lent_to', required=False, help='id of borrower', location='args')
book_update_parser.add_argument('to_be_returned_on', required=False, help='date by which borrower should return the book', location='args')
book_update_parser.add_argument('is_returned', required=False, help='book is returned', location='args')

borrower_parser = reqparse.RequestParser()
borrower_parser.add_argument('name', required=True, help='name of borrower', location='args')
borrower_parser.add_argument('email', required=True, help='email of borrower', location='args')

borrower_update_parser = reqparse.RequestParser()
borrower_update_parser.add_argument('id', required=True, help='id of borrower', location='args')
borrower_update_parser.add_argument('name', required=False, help='id of borrower', location='args')

book_loan_parser = reqparse.RequestParser()
book_loan_parser.add_argument('book_id', required=True, help='id of book being borrowed', location='args')
book_loan_parser.add_argument('lent_to', required=True, help='id of borrower being lent to', location='args')
book_loan_parser.add_argument('is_borrowing', required=True, help='is person borrowing or returning', location='args',
                              type=bool, default=True)
