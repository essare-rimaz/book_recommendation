from flask import Blueprint, redirect, render_template, request

insert = Blueprint("insert", __name__)


#endpoint for insert
@insert.route('/insert', methods=['GET', 'POST'])
def insert_function():
    if request.method == "POST":
        try:
            return redirect("/insert")
        except:
            return "There was an error adding the book"

    else:
        return render_template('/insert.html')

