from flask import Blueprint, request, render_template
from pipeline.processing import find_searched_book_title_isbn, find_users_who_liked_searched_book, find_candidate_books

search = Blueprint("search", __name__)


@search.route('/search', methods=['GET', 'POST'])
def search_function():
    if request.method == "POST":
        # gets the info from the form
        #print(type(request.form["book"]))
        #print(f">>{request.form['book']}<<")
        if "book" in request.form:
            searched_book = request.form['book']
            try:
                result = find_searched_book_title_isbn(searched_book)

                if len(result) > 1:
                    return render_template("/search_disambiguation.html", books=result)
                else:
                    users = find_users_who_liked_searched_book(result)
                    result_real = find_candidate_books(users)
                    return render_template("/search.html", books=result_real)
            except:
                if searched_book == "":
                    return render_template("/search.html", books=["Please submit a book title"])
                else:
                    return render_template("/search.html", books=["There was an error searching the book"])

        if "isbn" in request.form:
            searched_book_isbn = [request.form['isbn']]
            print(searched_book_isbn)
            try:
                users = find_users_who_liked_searched_book(searched_book_isbn)
                result_real = find_candidate_books(users)
                return render_template("/search.html", books=result_real)
            except:
                if searched_book_isbn == "":
                    return render_template("/search.html", books=["Please submit a book title"])
                else:
                    return render_template("/search.html", books=["There was an error searching the book"])


    else:
        return render_template('/search.html')
