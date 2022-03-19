from pipeline.web_app import create_app
from sqlalchemy import MetaData
from os import path, getcwd
from pipeline.database.load import something

# https://auth0.com/blog/sqlalchemy-orm-tutorial-for-python-developers/
app = create_app()
print("ahoj")
print(MetaData.tables)
#print(app.session.query())

print(path.join(getcwd(), r"pipeline\database\database.db"))

if not path.exists(path.join(getcwd(), r"pipeline\database\database.db")):
    something()

if __name__ == "__main__":
    app.run(debug=True)

