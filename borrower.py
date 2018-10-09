from http import HTTPStatus

from flask import (
    Blueprint, jsonify
)

from database.models import db, Borrower

borrower_app = Blueprint('borrower_app', __name__)


@borrower_app.route('/')
def show():
    return jsonify(response='Borrower stuff'), HTTPStatus.OK


@borrower_app.route('/add')
def record_add():
    db.create_all()
    borrower1 = Borrower("Survi")
    db.session.add(borrower1)
    db.session.commit()
    return jsonify(response='Successfully added'), HTTPStatus.CREATED
