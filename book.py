from http import HTTPStatus

from flask import (
    Blueprint, jsonify
)

book_app = Blueprint('book_app', __name__)


@book_app.route('/')
def show():
    return jsonify(response='Book stuff'), HTTPStatus.OK
