from flask import Blueprint, redirect, render_template, request

insert = Blueprint("insert", __name__)


#endpoint for insert
@insert.route('/insert', methods=['GET', 'POST'])
def insert_function():
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

