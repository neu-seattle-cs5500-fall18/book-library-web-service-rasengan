from http import HTTPStatus

from flask import (
    Blueprint
)
from flask_restplus import Resource, Api

borrower_app = Blueprint('borrower_app', __name__)
api = Api(borrower_app)


@api.route('/')
class Borrower(Resource):
    def get(self):
        return 'Borrower API!', HTTPStatus.OK
