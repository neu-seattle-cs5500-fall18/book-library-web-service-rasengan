from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.models import borrowerModel
from api.parsers import book_update_parser, borrower_parser
from database import db
from database.dbmodels import Book as BookDBModel, Borrower as BorrowerDBModel

ns = api.namespace('borrowers', description='Operations with respect to borrowers')


@ns.route('/')
@api.doc(description='List of borrowers. \n\n ')
class Borrowers(Resource):
    @api.doc(description='Get List of borrowers . \n\n ')
    def get(self):
        """ Get all borrowers """
        result = {}
        borrowers = []

        resp = BorrowerDBModel.query.all()
        if not resp:
            return []
        for x in resp:
            borrowers.append(x.to_dict())
        result['borrowers'] = borrowers
        return result

    @api.expect(borrower_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Success', borrowerModel)
    @api.doc(description='Add new borrower by name . \n\n ')
    def post(self):
        """ add borrower """
        args = borrower_parser.parse_args()
        borrower = BorrowerDBModel(args['name'])
        db.session.add(borrower)
        db.session.commit()
        return {'success': True}


@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of borrower'})
class Borrower(Resource):
    @api.doc(description='Get borrower by borrower id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(HTTPStatus.OK, 'Success', borrowerModel)
    def get(self, id):
        """ Get borrower by id """
        result = {}

        result = BookDBModel.query.get(id)

        return result.to_dict() if result else {'success': False, 'msg': 'borrower does not exist'}

    @api.response(HTTPStatus.OK, 'Success', borrowerModel)
    @api.doc(description='Delete Borrower  by book id. \n\n ' \
                         '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete borrower by id """

        borrower = BorrowerDBModel.query.get(id)

        if borrower:
            if BookDBModel.query.filterBy(lent_to=borrower.id).first():
                return {'success': False, 'msg': 'borrower can not be deleted'}
            else:
                db.session.delete(borrower)
                db.session.commit()
                return {'success': True}
        else:
            return {'success': False, 'msg': 'borrower does not exist'}

    @api.expect(book_update_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Success', borrowerModel)
    def put(self, id):
        """ Update borrower by id """
        borrower = BorrowerDBModel.query.get(id)
        if borrower:
            args = book_update_parser.parse_args()
            if args['title']:
                borrower.name = args['name']
                db.session.commit()
                return {'success': True}
        else:
            return {'success': False, 'msg': 'borrower does not exist'}
