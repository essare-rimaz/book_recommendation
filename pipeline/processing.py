from pipeline.database.database import engine, SessionLocal
from pipeline.database.connection import database_connection
from sqlalchemy import MetaData, select, func,desc, text


# TODO dismbiguation...



def find_searched_book_title_isbn(searched_book_title):
    books_table, ratings_table, session = database_connection()

    stmt = select(books_table.c.isbn, books_table.c.book_author, books_table.c.year_of_publication).where(books_table.c.book_title == searched_book_title)
    #TODO figure out how to turn the tuples into a list or something
    searched_book_isbn = session.execute(stmt).fetchall()
    # try to check if the list has a value, if empty that would raise an error
    searched_book_isbn[0]
    result_isbn = []
    print(f"The isbn of this book is {searched_book_isbn}")
    if len(searched_book_isbn) == 1:
        for isbn in searched_book_isbn:
            result_isbn.append(isbn.isbn)
        return result_isbn
    else:
        for isbn in searched_book_isbn:
            result_isbn.append([isbn.isbn+" written by "+isbn.book_author+" from "+str(isbn.year_of_publication)])
            print(result_isbn)
        return result_isbn


def find_users_who_liked_searched_book(searched_book_isbn):
    books_table, ratings_table, session = database_connection()
    stmt = select(ratings_table.c.user_id).where(ratings_table.c.isbn == searched_book_isbn[0]
                                                 and ratings_table.c.book_rating > 5)
    users_who_liked_searched_book = session.execute(stmt).fetchall()
    users = []
    for user in users_who_liked_searched_book:
        users.append(user.user_id)
    return users


def find_candidate_books(users):
    books_table, ratings_table, session = database_connection()
    stmt = select([ratings_table.c.isbn, ratings_table.c.book_rating],
                  (ratings_table.c.user_id.in_(users)) & (ratings_table.c.book_rating > 5))
    books_liked_by_those_users = session.execute(stmt).fetchall()
    books = []
    for book in books_liked_by_those_users:
        books.append(book.isbn)

    stmt = select([ratings_table.c.isbn, func.round(func.avg(ratings_table.c.book_rating)).label("mean"),
                   func.count(ratings_table.c.user_id).label("count")],
                  (ratings_table.c.isbn.in_(books) & (ratings_table.c.book_rating != 0))).group_by("isbn") \
        .having(text("count>9")).order_by(desc(text("count"))).limit(1)
    candidate_book_isbn = session.execute(stmt).fetchone().isbn
    print([candidate_book_isbn])
    stmt = select([books_table.c.book_title], books_table.c.isbn == candidate_book_isbn)
    candidate_book_name = session.execute(stmt).fetchone().book_title
    return [candidate_book_name]



