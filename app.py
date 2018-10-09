from http import HTTPStatus

from flask import Flask, jsonify

from book import book_app
from borrower import borrower_app
from config import database_uri
from database.models import db, Borrower


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.register_blueprint(book_app, url_prefix='/book')
    app.register_blueprint(borrower_app, url_prefix='/borrower')

    @app.route('/')
    def hello_world():
        return jsonify(response='Hello World! Heroku deployed'), HTTPStatus.OK

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
