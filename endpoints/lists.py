from http import HTTPStatus

from flask_restplus import Resource
from api import api
from api.api_models import  postModel
from api.parsers import list_get_parser,list_add_parser
from database import db
from database.db_models import Book as BookModel, ListBook, List as ListModel

ns = api.namespace('lists', description='Operations with respect to books list')

@ns.route('/')
@api.doc(description='Get all lists of books with \n\n ')
class Lists(Resource):
    @api.expect(list_get_parser, validate=False)
    @api.doc(description='Get List of books . \n\n ')
    def get(self):
        """ Get all lists """
        result = {}
        lists = []
        args = list_get_parser.parse_args()
        resp_query = ListModel.query
        if args['description']:
            resp_query = resp_query.filter_by(description=args['description'])
        resp = resp_query.all()
        if not resp:
            return []
        for x in resp:
            list = x.to_dict()
            book_ids=ListBook.query.filter_by(list_id=list['list_id']).all()
            if len(book_ids)>0:
                list['book_ids']=[]
                for book in book_ids:
                    temp=book.to_dict()
                    list['book_ids'].append(temp.get('book_id'))
                lists.append(list)
            else:
                lists.append(list)
        result['lists'] = lists
        return result

    @api.expect(list_get_parser, validate=True)
    @api.response(HTTPStatus.CREATED, 'Success', postModel)
    @api.doc(description='Add new custom list by providing a description . \n\n ')
    def post(self):
        """ add list of books """
        args = list_get_parser.parse_args()
        list=ListModel(args['description'])
        db.session.add(list)
        db.session.commit()
        return {'success': True}




@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of list'})
class List(Resource):

    @api.doc(description='Get List by list id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(HTTPStatus.OK, 'Success')
    def get(self, id):
        """ Get list by id """
        result={}
        lists = []
        resp = ListModel.query.get(id)
        if resp:
            list = resp.to_dict()
            book_ids=ListBook.query.filter_by(list_id=list['list_id']).all()
            if len(book_ids)>0:
                list['book_ids']=[]
                for book in book_ids:
                    temp=book.to_dict()
                    list['book_ids'].append(temp.get('book_id'))
                lists.append(list)
            else:
                lists.append(list)
            result['list'] = lists
        return result

    @api.doc(description='Add books to a list. \n\n')
    @api.expect(list_add_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Success')
    def post(self,id):
        """ Add books to a list by list_id and book id """
        result = {}
        result = ListModel.query.get(id)
        if result:
            args = list_add_parser.parse_args()
            if args.get('book_id'):
                book=BookModel.query.get(args.get('book_id'))
                if book:
                    book_id=book.to_dict().get('book_id')
                    list_id=result.to_dict().get('list_id')
                    listBook = ListBook(list_id,book_id)
                    db.session.add(listBook)
                    db.session.commit()
                    return {'success': True}
                else:
                    return {'success': False}
            else:
                return {'success': False}




