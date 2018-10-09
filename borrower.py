from http import HTTPStatus

from flask import (
    Blueprint, jsonify
)

borrower_app = Blueprint('borrower_app', __name__)


@borrower_app.route('/borrower')
def show():
    return jsonify(response='Borrower stuff'), HTTPStatus.OK
