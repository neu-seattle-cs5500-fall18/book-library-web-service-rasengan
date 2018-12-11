import os

from apscheduler.schedulers.background import BackgroundScheduler
from flask import Flask, Blueprint

from api import api
from config import database_uri
from database import db
from endpoints.books import ns as books_ns
from endpoints.borrowers import ns as borrowers_ns, Borrower
from endpoints.lists import ns as lists_ns
from endpoints.loans import ns as loans_ns, LoanedBooks
from mail import mail, send_reminder_mail

mail_settings = {
    "MAIL_SERVER": 'smtp.gmail.com',
    "MAIL_PORT": 465,
    "MAIL_USE_TLS": False,
    "MAIL_USE_SSL": True,
    "MAIL_DEFAULT_SENDER": os.environ['CATALOG_SERVICE_EMAIL_USER'],
    "MAIL_USERNAME": os.environ['CATALOG_SERVICE_EMAIL_USER'],
    "MAIL_PASSWORD": os.environ['CATALOG_SERVICE_EMAIL_PASSWORD']
}

app = Flask(__name__)


def create_app():
    app.config[
        'SQLALCHEMY_DATABASE_URI'] = database_uri
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.SWAGGER_UI_JSONEDITOR = True
    app.config.update(mail_settings)

    db.init_app(app)
    mail.init_app(app)

    # with app.app_context():
    #     db.create_all()

    blueprint = Blueprint('api', __name__, url_prefix='/doc')
    api.init_app(blueprint)
    api.add_namespace(books_ns)
    api.add_namespace(borrowers_ns)
    api.add_namespace(loans_ns)
    api.add_namespace(lists_ns)
    app.register_blueprint(blueprint)

    @app.route('/')
    def hello_world():
        return 'Hello Rasengan'

    # init BackgroundScheduler job
    scheduler = BackgroundScheduler()
    scheduler.add_job(reminder_job, trigger='interval', days=1)
    scheduler.start()

    try:
        return app
    except:
        scheduler.shutdown()


def reminder_job():
    try:
        with app.app_context():
            resp = LoanedBooks().get()
            for book in resp['loaned_books']:
                if book['return_status'] == 'Late':
                    borrower = Borrower().get(book['lent_to'])
                    send_reminder_mail(borrower['email'], book['title'])
    except Exception as e:
        print(e)


application = create_app()

if __name__ == '__main__':
    application.run()
