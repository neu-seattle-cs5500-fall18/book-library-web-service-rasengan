from http import HTTPStatus

from flask import (
    Blueprint, jsonify
)

from database.models import db, Borrower

borrower_app = Blueprint('borrower_app', __name__)


@borrower_app.route('/add/<person>')
def add(person):
    borrower = Borrower(person)
    db.session.add(borrower)
    db.session.commit()
    return jsonify(response='Successfully added ' + person), HTTPStatus.CREATED
