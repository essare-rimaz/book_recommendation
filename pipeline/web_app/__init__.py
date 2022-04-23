from flask import Flask, _app_ctx_stack
from sqlalchemy.orm import scoped_session
from pipeline.database.database import SessionLocal

DB_NAME = "database.db"


def create_app():
    """ Setup of the web application

    """
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "very secret"
    # a fix for multithreading, probably not necessary for dev
    app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    # Path creating with possible prefixes
    from pipeline.web_app.views.index import index
    from pipeline.web_app.views.search import search
    from pipeline.web_app.views.insert import insert

    app.register_blueprint(index)
    app.register_blueprint(search)
    app.register_blueprint(insert)

    return app



