from http import HTTPStatus

from flask import Flask, jsonify

from book import book_app
from borrower import borrower_app
from config import database_uri
from database.models import db


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    with app.app_context():
        db.init_app(app)
        db.create_all()
    app.register_blueprint(book_app, url_prefix='/book')
    app.register_blueprint(borrower_app, url_prefix='/borrower')

    @app.route('/')
    def hello_world():
        return jsonify(response='Hello World! Heroku deployed'), HTTPStatus.OK
    return app


application = create_app()


if __name__ == '__main__':
    application.run()
