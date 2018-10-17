from http import HTTPStatus

from flask import Flask
from flask_restplus import reqparse, Api, Resource

from api.models import ApiModel
from config import database_uri
from database.models import db, Book as BookModel, Borrower as BorrowerModel

# Request Parsing
book_parser = reqparse.RequestParser()
book_parser.add_argument('title', required=True, help='name of book', location='args')
book_parser.add_argument('author', required=True, help='name of author', location='args')
book_parser.add_argument('genre', required=True, help='book genre', location='args')
book_parser.add_argument('published_on', required=True, help='book publication date', location='args')

book_update_parser = reqparse.RequestParser()
book_update_parser.add_argument('title', required=False, help='name of book', location='args')
book_update_parser.add_argument('author', required=False, help='author of book', location='args')
book_update_parser.add_argument('genre', required=False, help='genre of book', location='args')
book_update_parser.add_argument('published_on', required=False, help='book publication date', location='args')
book_update_parser.add_argument('notes', required=False, help='notes for book', location='args')
book_update_parser.add_argument('lent_to', required=False, help='id of borrower', location='args')
book_update_parser.add_argument('to_be_returned_on', required=False, help='id of borrower', location='args')
book_update_parser.add_argument('is_returned', required=False, help='book is returned', location='args')

borrower_parser = reqparse.RequestParser()
borrower_parser.add_argument('name', required=True, help='name of borrower', location='args')

borrower_update_parser = reqparse.RequestParser()
borrower_update_parser.add_argument('id', required=True, help='id of borrower', location='args')
borrower_update_parser.add_argument('name', required=False, help='id of borrower', location='args')


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    with app.app_context():
        db.init_app(app)
        db.create_all()

    api = Api(app)
    api_model = ApiModel(api)

    @api.route('/')
    class GoToBooks(Resource):
        @api.doc(description='You are in home. \n\n ')
        @api.response(HTTPStatus.OK, 'Success', api_model.postModel)
        def get(self):
            return {'success': True}

    @api.route('/books/')
    @api.doc(description='List of books \n\n ')
    class Books(Resource):
        def __init__(self, Resource):
            self.api = api

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
        @api.response(HTTPStatus.CREATED, 'Success', api_model.postModel)
        @api.doc(description='Add new book by title,author,genre, published_on . \n\n ')
        def post(self):
            """ add book """
            args = book_parser.parse_args()
            book = BookModel(args['title'], args['author'], args['genre'], args['published_on'])
            db.session.add(book)
            db.session.commit()
            return {'success': True}

    @api.route('/books/<string:id>')
    @api.doc(params={'id': 'Id of book'})
    class Book(Resource):
        def __init__(self, Resource):
            self.api = api

        @api.doc(description='Get Book by book id. \n\n ' \
                             '* [Test query] `id`=1')
        @api.response(HTTPStatus.OK, 'Success', api_model.bookModel)
        def get(self, id):
            """ Get book by id """
            result = {}

            result = BookModel.query.get(id)

            return result.to_dict() if result else {'success': False, 'msg': 'book does not exist'}

        @api.response(HTTPStatus.OK, 'Success', api_model.postModel)
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
        @api.response(HTTPStatus.CREATED, 'Success', api_model.postModel)
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

    @api.route('/borrowers/')
    @api.doc(description='List of borrowers. \n\n ')
    class Borrowers(Resource):
        def __init__(self, Resource):
            self.api = api

        @api.doc(description='Get List of borrowers . \n\n ')
        def get(self):
            """ Get all borrowers """
            result = {}
            borrowers = []

            resp = BorrowerModel.query.all()
            if not resp:
                return []
            for x in resp:
                borrowers.append(x.to_dict())
            result['borrowers'] = borrowers
            return result

        @api.expect(borrower_parser, validate=False)
        @api.response(HTTPStatus.CREATED, 'Success', api_model.borrowerModel)
        @api.doc(description='Add new borrower by name . \n\n ')
        def post(self):
            """ add borrower """
            args = borrower_parser.parse_args()
            borrower = BorrowerModel(args['name'])
            db.session.add(borrower)
            db.session.commit()
            return {'success': True}

    @api.route('/borrowers/<string:id>')
    @api.doc(params={'id': 'Id of borrower'})
    class Borrower(Resource):
        def __init__(self, Resource):
            self.api = api

        @api.doc(description='Get borrower by borrower id. \n\n ' \
                             '* [Test query] `id`=1')
        @api.response(HTTPStatus.OK, 'Success', api_model.borrowerModel)
        def get(self, id):
            """ Get borrower by id """
            result = {}

            result = BookModel.query.get(id)

            return result.to_dict() if result else {'success': False, 'msg': 'borrower does not exist'}

        @api.response(HTTPStatus.OK, 'Success', api_model.borrowerModel)
        @api.doc(description='Delete Borrower  by book id. \n\n ' \
                             '* [Test query] `id`=1')
        def delete(self, id):
            """ Delete borrower by id """

            borrower = BorrowerModel.query.get(id)

            if borrower:
                if BookModel.query.filterBy(lent_to=borrower.id).first():
                    return {'success': False, 'msg': 'borrower can not be deleted'}
                else:
                    db.session.delete(borrower)
                    db.session.commit()
                    return {'success': True}
            else:
                return {'success': False, 'msg': 'borrower does not exist'}

        @api.expect(book_update_parser, validate=False)
        @api.response(HTTPStatus.CREATED, 'Success', api_model.borrowerModel)
        def put(self, id):
            """ Update borrower by id """
            borrower = BorrowerModel.query.get(id)
            if borrower:
                args = book_update_parser.parse_args()
                if args['title']:
                    borrower.name = args['name']
                    db.session.commit()
                    return {'success': True}
            else:
                return {'success': False, 'msg': 'borrower does not exist'}

    return app


application = create_app()

if __name__ == '__main__':
    application.run()
