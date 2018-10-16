from http import HTTPStatus

from flask import Flask, jsonify
from config import database_uri
from database.models import db


def create_app():
    app = Flask(__name__)
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'
    with app.app_context():
        db.init_app(app)
        db.create_all()

    from api.booksDAO import book_app
    app.register_blueprint(book_app, url_prefix='/book')

    from borrower import borrower_app
    app.register_blueprint(borrower_app, url_prefix='/borrower')

    @app.route('/')
    def hello_world():
        return jsonify(response='Hello World! Heroku deployed'), HTTPStatus.OK
    return app


application = create_app()


if __name__ == '__main__':
    application.run()
