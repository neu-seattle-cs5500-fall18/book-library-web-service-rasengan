from flask import Flask, Blueprint

from api import api
from api.endpoints.books import ns as books_ns
from api.endpoints.borrowers import ns as borrowers_ns
from config import database_uri
from database import db

app = Flask(__name__)


def create_app():
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.SWAGGER_UI_DOC_EXPANSION = 'list'

    db.init_app(app)

    blueprint = Blueprint('api', __name__, url_prefix='/doc/')
    api.init_app(blueprint)
    api.add_namespace(books_ns)
    api.add_namespace(borrowers_ns)
    app.register_blueprint(blueprint)

    @app.route('/')
    def hello_world():
        return 'Hello World'
    return app


application = create_app()

if __name__ == '__main__':
    application.run()
