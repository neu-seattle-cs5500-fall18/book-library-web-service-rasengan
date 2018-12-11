from http import HTTPStatus

from flask_restplus import Resource

from api import api
from api.api_models import borrowerModel
from api.parsers import borrower_update_parser, borrower_parser
from database import db
from database.db_models import Book as BookDBModel, Borrower as BorrowerDBModel

ns = api.namespace('borrowers', description='Operations with respect to borrowers')


@ns.route('/')
@api.doc(description='List of borrowers. \n\n ')
class Borrowers(Resource):
    @api.doc(description='Get List of borrowers . \n\n ')
    def get(self):
        """ Get all borrowers """
        try:
            result = {}
            borrowers = []

            resp = BorrowerDBModel.query.all()
            if not resp:
                return []
            for x in resp:
                borrowers.append(x.to_dict())
            result['borrowers'] = borrowers
            return result, HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(borrower_parser, validate=False)
    @api.response(HTTPStatus.CREATED, 'Borrower added successfully', borrowerModel)
    @api.doc(description='Add new borrower by name & email. \n\n ')
    def post(self):
        """ add borrower """
        try:
            args = borrower_parser.parse_args()
            borrower = BorrowerDBModel(args['name'], args['email'])
            db.session.add(borrower)
            db.session.commit()
            return {'success': True}, HTTPStatus.CREATED
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST


@ns.route('/<string:id>')
@api.doc(params={'id': 'Id of borrower'})
class Borrower(Resource):
    @api.doc(description='Get borrower by borrower id. \n\n ' \
                         '* [Test query] `id`=1')
    @api.response(HTTPStatus.OK, 'Borrower fetched successfully!', borrowerModel)
    def get(self, id):
        """ Get borrower by id """
        try:
            result = BorrowerDBModel.query.get(id)
            return (result.to_dict() if result else {'success': False, 'msg': 'borrower does not exist'}), HTTPStatus.OK
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(HTTPStatus.OK, 'Borrower successfully deleted')
    @api.doc(description='Delete Borrower  by book id. \n\n ' \
                         '* [Test query] `id`=1')
    def delete(self, id):
        """ Delete borrower by id """
        try:
            borrower = BorrowerDBModel.query.get(id)
            if borrower:
                if BookDBModel.query.filterBy(lent_to=borrower.id).first():
                    return {'success': False, 'msg': 'borrower can not be deleted'}, HTTPStatus.BAD_REQUEST
                else:
                    db.session.delete(borrower)
                    db.session.commit()
                    return {'success': True}, HTTPStatus.OK
            else:
                return {'success': False, 'msg': 'borrower does not exist'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(borrower_update_parser, validate=False)
    @api.response(HTTPStatus.OK, 'Borrower updated successfully')
    def put(self, id):
        """ Update borrower by id """
        try:
            borrower = BorrowerDBModel.query.get(id)
            if borrower:
                args = borrower_update_parser.parse_args()
                if args.get('name'):
                    borrower.name = args['name']
                if args.get('email'):
                    borrower.email = args['email']
                db.session.commit()
                return {'success': True}, HTTPStatus.OK
            else:
                return {'success': False, 'msg': 'borrower does not exist'}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            return {'msg': 'There was an error', 'error': str(e)}, HTTPStatus.BAD_REQUEST
