from flask import Blueprint, request, render_template
from pipeline.database.database import SessionLocal, engine
from sqlalchemy import select, MetaData

search = Blueprint("search", __name__)


@search.route('/search', methods=['GET', 'POST'])
def search_function():
    if request.method == "POST":
        # gets the info from the form
        searched_book = request.form['book']
        print(f"books searched was {searched_book}")

        #for user_obj in result.scalars():
        #    print(user_obj)
        #result = select([func.count()]).select_from(tables).where("book_title" == "Selected Poems").scalar()
        #result = select(tables.c.isbn).where(tables.c.book_title == "Stone Butch Blues;Leslie Feinberg").scalar()
        #result = select(tables.c.isbn).count()
        #result = select(tables).where(tables.c.book_title == "Selected Poems").scalars()
        # result = Book.query.filter_by(book_title=searched_book).all()


        try:
            meta_data = MetaData(bind=engine)
            MetaData.reflect(meta_data)
            tables = meta_data.tables["books_table"]
            session = SessionLocal()
            stmt = select(tables.c.isbn).where(tables.c.book_title == searched_book)
            result = session.execute(stmt).fetchall()
            test = session.execute(stmt).fetchall()
            print(dir(test))
            print(test.__class__)
            print(test[0].__class__)
            print(dir(test[0]))
            print(test[0]._fields)
            print(test[0].isbn)
            for x in test[0].isbn:
                print(x)
            #print(isbn)
            #print(result)

            return render_template("/search.html", books=result)
        except:
            return "There was an error adding the book"

    else:
        return render_template('/search.html')
