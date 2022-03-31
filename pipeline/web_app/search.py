from flask import Blueprint, request, render_template
from pipeline.database.database import SessionLocal, engine
from sqlalchemy import select, MetaData
from pipeline.processing import recommend_book, find_searched_book_title_isbn, find_users_who_liked_searched_book, find_candidate_books

search = Blueprint("search", __name__)


@search.route('/search', methods=['GET', 'POST'])
def search_function():
    if request.method == "POST":
        # gets the info from the form
        print(type(request.form["book"]))
        print(f">>{request.form['book']}<<")
        searched_book = request.form['book']
        print(f"books searched was {searched_book}")

        try:
            #TODO replace with a defined function
            # meta_data = MetaData(bind=engine)
            # MetaData.reflect(meta_data)
            # tables = meta_data.tables["books_table"]
            # session = SessionLocal()
            # stmt = select(tables.c.isbn).where(tables.c.book_title == searched_book)
            # result = session.execute(stmt).fetchall()
            # result = recommend_book(searched_book)
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


    else:
        return render_template('/search.html')
