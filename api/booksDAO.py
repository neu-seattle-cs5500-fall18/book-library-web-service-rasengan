from .models import ApiModel
from flask import Blueprint
from flask_restplus import reqparse, Resource, Api, fields, Namespace
from database.models import Book as BookModel, db


book_app = Blueprint('book_app', __name__)
api = Api(book_app, version='1.0', title='Book API', description='Book class API', doc='/doc/')
apiModel = ApiModel(api)

# Request Parsing
parser = reqparse.RequestParser()
parser.add_argument('title', required=True, help='name of book', location='args')
parser.add_argument('author', required=True, help='name of author', location='args')
parser.add_argument('genre', required=True, help='book genre', location='args')
parser.add_argument('published_on', required=True, help='book publication date', location='args')

parserUpdate = reqparse.RequestParser()
parserUpdate.add_argument('title', required=False, help='name of book', location='args')
parserUpdate.add_argument('author', required=False, help='author of book', location='args')
parserUpdate.add_argument('genre', required=False, help='genre of book', location='args')
parserUpdate.add_argument('published_on', required=False, help='book publication date', location='args')
parserUpdate.add_argument('notes', required=False, help='notes for book', location='args')
parserUpdate.add_argument('lent_to', required=False, help='id of borrower', location='args')
parserUpdate.add_argument('to_be_returned_on', required=False, help='id of borrower', location='args')
parserUpdate.add_argument('is_returned', required=False, help='book is returned', location='args')


@api.route('/')
class Books(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get List of books . \n\n ')
    @api.response(200, 'Success', apiModel.booksModel)
    def get(self):
        """ Get all books """
        result = {}
        books = []

        resp = BookModel.query.all()
        if resp == None:
            return []

        for x in resp:
            books.append(x.to_dict())
        result['books'] = books
        return result

    @api.expect(parser, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Add new book by title,author,genre, publishedOn . \n\n ')
    def post(self):
        """ add book """
        args = parser.parse_args()
        book = BookModel(args['title'], args['author'], args['genre'], args['published_on'])
        db.session.add(book)
        db.session.commit()
        return {'success': True}


@api.route('/<int:id>')
@api.doc(params={'id': 'Id of book'})
class Book(Resource):
    def __init__(self, Resource):
        self.api = api

    @api.doc(description='Get Book by book id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(200, 'Success', apiModel.bookModel)
    def get(self, id):
        """ Get user by id """
        result = {}

        result = BookModel.query.get(id)

        return result.to_dict() if result != None else {'success': False, 'msg': 'book does not exist'}

    @api.response(200, 'Success', apiModel.postModel)
    @api.doc(description='Delete Book  by book id. \n\n ' \
                         '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete book by id """

        book = BookModel.query.get(id)
        if book != None:
            db.session.delete(book)
            db.session.commit()
            return {'success': True}
        else:
            return {'success': False, 'msg': 'book does not exist'}

    @api.expect(parserUpdate, validate=False)
    @api.response(200, 'Success', apiModel.postModel)
    def put(self, id):
        """ Update user by id """
        book = BookModel.query.get(id)
        if book != None:
            args = parserUpdate.parse_args()
            if args['title'] != None:
                book.title = args['title']
            if args['author'] != None:
                book.author = args['author']
            if args['genre'] != None:
                book.genre = args['genre']
            if args['published_on'] != None:
                book.published_on = args['published_on']
            if args['notes'] != None:
                book.notes = args['notes']
            if args['lent_to'] != None:
                book.lent_to = args['lent_to']
            if args['to_be_returned_on'] != None:
                book.is_returned = args['to_be_returned_on']
            if args['is_returned'] != None:
                book.is_returned = args['is_returned']
            db.session.commit()
            return {'success': True}
        else:
            return {'success': False, 'msg': 'book does not exist'}
