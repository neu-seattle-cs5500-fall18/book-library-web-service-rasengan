from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.api_models import bookModel, postModel
from api.parsers import book_parser, book_update_parser
from database import db
from database.db_models import Book as BookModel

ns = api.namespace('books', description='Operations with respect to books')


@ns.route('/')
@api.doc(description='List of books \n\n ')
class Books(Resource):
    @api.doc(description='Get List of books . \n\n ')
    def get(self):
        """ Get all books """
        result = {}
        books = []

        resp = BookModel.query.all()
        if not resp:
            return []
        for x in resp:
            books.append(x.to_dict())
        result['books'] = books
        return result

    @api.expect(book_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Success', postModel)
    @api.doc(description='Add new book by title,author,genre, published_on . \n\n ')
    def post(self):
        """ add book """
        args = book_parser.parse_args()
        book = BookModel(args['title'], args['author'], args['genre'], args['published_on'])
        db.session.add(book)
        db.session.commit()
        return {'success': True}


@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of book'})
class Book(Resource):
    @api.doc(description='Get Book by book id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(HTTPStatus.OK, 'Success', bookModel)
    def get(self, id):
        """ Get book by id """
        result = {}

        result = BookModel.query.get(id)

        return result.to_dict() if result else {'success': False, 'msg': 'book does not exist'}

    @api.response(HTTPStatus.OK, 'Success', postModel)
    @api.doc(description='Delete Book  by book id. \n\n ' \
                         '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete book by id """

        book = BookModel.query.get(id)
        if book:
            db.session.delete(book)
            db.session.commit()
            return {'success': True}
        else:
            return {'success': False, 'msg': 'book does not exist'}

    @api.expect(book_update_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Success', postModel)
    def put(self, id):
        """ Update book by id """
        book = BookModel.query.get(id)
        if book:
            args = book_update_parser.parse_args()
            if args['title']:
                book.title = args['title']
            if args['author']:
                book.author = args['author']
            if args['genre']:
                book.genre = args['genre']
            if args['published_on']:
                book.published_on = args['published_on']
            if args['notes']:
                book.notes = args['notes']
            if args['lent_to']:
                book.lent_to = args['lent_to']
            if args['to_be_returned_on']:
                book.is_returned = args['to_be_returned_on']
            if args['is_returned']:
                book.is_returned = args['is_returned']
            db.session.commit()
            return {'success': True}
        else:
            return {'success': False, 'msg': 'book does not exist'}
