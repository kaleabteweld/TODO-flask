from flask import Flask

from src.routes import registerRoutes
from src.utilities.session import initSession
from src.utilities.consts import db
from ..error._init__ import addRoutesErrorsHandled


def makeApp():
    app = Flask(__name__)
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///project.db"
    app.config["SECRET_KEY"] = "secret"

    registerRoutes(app)
    addRoutesErrorsHandled(app)
    initSession(app)

    db.init_app(app)

    initDb(app)
    return app


def initDb(app: Flask):
    from src.models.users import User

    with app.app_context():
        db.create_all()


# def create_app(test_config=None):
#     # create and configure the app
#     app = Flask(__name__, instance_relative_config=True)
#     app.config.from_mapping(
#         SECRET_KEY='dev',
#         DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
#     )

#     if test_config is None:
#         # load the instance config, if it exists, when not testing
#         app.config.from_pyfile('config.py', silent=True)
#     else:
#         # load the test config if passed in
#         app.config.from_mapping(test_config)

#     # ensure the instance folder exists
#     try:
#         os.makedirs(app.instance_path)
#     except OSError:
#         pass

#     # a simple page that says hello
#     @app.route('/hello')
#     def hello():
#         return 'Hello, World!'

#     return app
