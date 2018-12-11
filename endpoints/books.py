from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.api_models import book_model
from api.parsers import book_parser, book_get_parser, book_update_parser
from database import db
from database.db_models import Book as BookModel

ns = api.namespace('books', description='Operations with respect to books')


@ns.route('/')
@api.doc(description='List of books \n\n ')
class Books(Resource):
    @api.expect(book_get_parser, validate=False)
    @api.marshal_with(book_model, as_list=True)
    @api.doc(description='Get List of books . \n\n ')
    def get(self):
        """ Get all books """
        try:
            books = []
            args = book_get_parser.parse_args()
            resp_query = BookModel.query
            if args.get('author'):
                resp_query = resp_query.filter_by(author=args['author'])
            if args.get('genre'):
                resp_query = resp_query.filter_by(genre=args['genre'])
            if args.get('published range'):
                start = args['published range'].split('-')[0]
                end = args['published range'].split('-')[1]
                resp_query = resp_query.filter(BookModel.published_on.between(start, end))
            resp = resp_query.all()
            if not resp:
                return []
            for x in resp:
                books.append(x.to_dict())
            return books, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Book added successfully!', book_model)
    @api.doc(description='Add new book by title,author,genre, published_on . \n\n ')
    def post(self):
        """ add book """
        try:
            args = book_parser.parse_args()
            book = BookModel(args['title'], args['author'], args['genre'], args['published_on'], args['notes'])
            db.session.add(book)
            db.session.commit()
            return book.to_dict(), HTTPStatus.CREATED
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST


@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of book'})
class Book(Resource):
    @api.doc(description='Get Book by book id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(HTTPStatus.OK, 'Fetched book successfully', book_model)
    def get(self, id):
        """ Get book by id """
        try:
            result = BookModel.query.get(id)
            return (result.to_dict() if result else {'success': False, 'msg': 'book does not exist'}), HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(HTTPStatus.OK, 'Deleted book successfully', book_model)
    @api.doc(description='Delete Book  by book id. \n\n '
                         '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete book by id """
        try:
            book = BookModel.query.get(id)
            if book:
                db.session.delete(book)
                db.session.commit()
                return book.to_dict(), HTTPStatus.OK
            else:
                return {'success': False, 'msg': 'book does not exist'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(book_update_parser, validate=False)
    @api.response(HTTPStatus.OK, 'Book successfully updated', book_model)
    def put(self, id):
        """ Update book by id """
        try:
            book = BookModel.query.get(id)
            if book:
                args = book_update_parser.parse_args()
                if args.get('title'):
                    book.title = args['title']
                if args.get('author'):
                    book.author = args['author']
                if args.get('genre'):
                    book.genre = args['genre']
                if args.get('published_on'):
                    book.published_on = args['published_on']
                if args.get('notes'):
                    book.notes = args['notes']
                if args.get('lent_to'):
                    book.lent_to = args['lent_to']
                if args.get('to_be_returned_on'):
                    book.is_returned = args['to_be_returned_on']
                if args.get('is_returned'):
                    book.is_returned = args['is_returned']
                db.session.commit()
                return book.to_dict(), HTTPStatus.OK
            else:
                return {'success': False, 'msg': 'book does not exist'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST
