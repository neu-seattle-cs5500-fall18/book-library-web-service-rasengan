from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.api_models import list_model
from api.api_models import success_model
from api.parsers import list_get_parser, list_add_parser
from database import db
from database.db_models import Book as BookModel, ListBook, List as ListModel

ns = api.namespace('lists', description='Operations with respect to books list')


@ns.route('/')
@api.doc(description='Get all lists of books with \n\n ')
class Lists(Resource):
    @api.expect(list_get_parser, validate=False)
    @api.marshal_with(list_model, as_list=True)
    @api.response(HTTPStatus.OK, 'Fetching lists successful')
    @api.response(HTTPStatus.BAD_REQUEST, 'Fetching lists unsuccessful')
    @api.doc(description='Get List of books . \n\n ')
    def get(self):
        """ Get all lists """
        try:
            lists = []
            args = list_get_parser.parse_args()
            resp_query = ListModel.query
            if args['description']:
                resp_query = resp_query.filter_by(description=args['description'])
            resp = resp_query.all()
            if not resp:
                return []
            for x in resp:
                list_dict = x.to_dict()
                book_ids = ListBook.query.filter_by(list_id=list_dict['list_id']).all()
                if len(book_ids) > 0:
                    list_dict['book_ids'] = []
                    for book in book_ids:
                        temp = book.to_dict()
                        list_dict['book_ids'].append(temp.get('book_id'))
                    lists.append(list_dict)
                else:
                    lists.append(list_dict)
            return lists, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(list_get_parser, validate=True)
    @api.response(HTTPStatus.CREATED, 'Successfully created a list', success_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Creating list unsuccessful')
    @api.doc(description='Add new custom list by providing a description . \n\n ')
    def post(self):
        """ create a list for books """
        try:
            args = list_get_parser.parse_args()
            list_dict = ListModel(args['description'])
            db.session.add(list_dict)
            db.session.commit()
            return {'success': True}, HTTPStatus.CREATED
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST


@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of list'})
class List(Resource):
    @api.doc(description='Get List by list id. \n\n '
                         '* [Test query] `id`=1')
    @api.marshal_with(list_model)
    @api.response(HTTPStatus.OK, 'Fetched list successfully')
    @api.response(HTTPStatus.BAD_REQUEST, 'Fetching list unsuccessful')
    def get(self, id):
        """ Get list by id """
        try:
            resp = ListModel.query.get(id)
            list_dict = resp.to_dict()
            book_ids = ListBook.query.filter_by(list_id=list_dict['list_id']).all()
            if len(book_ids) > 0:
                list_dict['book_ids'] = []
                for book in book_ids:
                    temp = book.to_dict()
                    list_dict['book_ids'].append(temp.get('book_id'))
            return list_dict, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.doc(description='Add books to a list. \n\n')
    @api.expect(list_add_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Added books to list successfully', success_model)
    @api.response(HTTPStatus.BAD_REQUEST, 'Adding books to list unsuccessful')
    def post(self, id):
        """ Add books to a list by list_id and book id """
        try:
            result = ListModel.query.get(id)
            if result:
                args = list_add_parser.parse_args()
                if args.get('book_id'):
                    book = BookModel.query.get(args.get('book_id'))
                    if book:
                        book_id = book.to_dict().get('book_id')
                        list_id = result.to_dict().get('list_id')
                        list_book = ListBook(list_id, book_id)
                        db.session.add(list_book)
                        db.session.commit()
                        return {'success': True}, HTTPStatus.CREATED
                    else:
                        return {'success': False}, HTTPStatus.BAD_REQUEST
                else:
                    return {'success': False}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST
