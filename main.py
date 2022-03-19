from pipeline.web_app import create_app
from os import path, getcwd
from pipeline.database.load import create_database

# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
app = create_app()


if not path.exists(path.join(getcwd(), r"pipeline\database\database.db")):
    create_database()

if __name__ == "__main__":
    app.run(debug=True)

