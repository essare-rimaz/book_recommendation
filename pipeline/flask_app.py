from flask import Flask, request, render_template, redirect
from flask_sqlalchemy import SQLAlchemy
from test_load import books_table

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///books.db"

#TODO prehodit databazi mimo appku
#initialize the db
db = SQLAlchemy(app)



#create a db model
#had to create it manually using: WHY?!
# from flask_app import db
# db.create_all()
# adding db.create_all() in if __name__ = "__main__" did no help
class Books(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)

    def __init__(self, name):
        self.name = name


#endpoint for search
@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == "POST":
        # gets the info from the form
        searched_book = request.form['book']
        try:
            books_from_db = Books.query.filter_by(name=searched_book).all()
            return render_template("/search.html", books=books_from_db)
        except:
            return "There was an error adding the book"

    else:
        return render_template('/index.html')


@app.route('/search', methods=['GET', 'POST'])
def search():
    if request.method == "POST":
        # gets the info from the form
        searched_book = request.form['book']
        try:
            books_from_db = Books.query.filter_by(name=searched_book).all()
            return render_template("/search.html", books=books_from_db)
        except:
            return "There was an error adding the book"

    else:
        return render_template('/search.html')


#endpoint for insert
@app.route('/insert', methods=['GET', 'POST'])
def insert():
    if request.method == "POST":
        # gets the info from the form
        book = request.form['book']
        print(book)
        # search by author or book
        new_book = Books(name=book)

        try:
            db.session.add(new_book)
            db.session.commit()
            return redirect("/insert")
        except:
            return "There was an error adding the book"

    else:
        books = Books.query.order_by(Books.name)
        return render_template('/insert.html', books=books)


if __name__ == "__main__":
    app.run()
