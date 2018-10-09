from http import HTTPStatus

from flask import Flask, jsonify

from .config import database_uri
from .database.db import db, Borrower


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    @app.route('/')
    def hello_world():
        return jsonify(response='Hello World! Heroku deployed'), HTTPStatus.OK

    @app.route('/add')
    def record_add():
        db.create_all()
        borrower1 = Borrower("Survi")
        db.session.add(borrower1)
        db.session.commit()
        return jsonify(response='Successfully added'), HTTPStatus.CREATED

    @app.route('/show')
    def record_show():
        test_record = Borrower.query.filter_by(name='Survi').first()
        print(test_record.id, " ", test_record.name)
        return test_record.name

    @app.route('/delete')
    def record_delete():
        record = record_show()
        before_delete = Borrower.query.filter_by(name=record).first()
        db.session.delete(before_delete)
        db.session.commit()
        after_delete = Borrower.query.filter_by(name="Survi").first()
        print(after_delete.id)
        return "Successfully deleted"

    db.init_app(app)
    return app


application = create_app()


if __name__ == '__main__':
    application.run()
