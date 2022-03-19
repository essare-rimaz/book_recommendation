from flask import Flask, _app_ctx_stack
from sqlalchemy.orm import scoped_session
from pipeline.database.database import SessionLocal

DB_NAME = "database.db"


def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = "very secret"
    app.session = scoped_session(SessionLocal, scopefunc=_app_ctx_stack.__ident_func__)

    from .index import index
    from .search import search
    from .insert import insert

    app.register_blueprint(index)
    app.register_blueprint(search)
    app.register_blueprint(insert)

    return app



