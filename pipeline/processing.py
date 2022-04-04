import dask.dataframe as dd
from pipeline.database.database import engine, SessionLocal
from sqlalchemy import MetaData, select, func,desc, text


# TODO dismbiguation...


def database_connection():
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    books_table = meta_data.tables["books_table"]
    ratings_table = meta_data.tables["ratings_table"]
    session = SessionLocal()

    return books_table, ratings_table, session


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


def recommend_book(searched_book):
    books_table, ratings_table, session = database_connection()


    #get ISBN of the searched book
    print(searched_book)
    stmt = select(books_table.c.isbn).where(books_table.c.book_title == searched_book)

    search_book_isbn = session.execute(stmt).fetchall()[0].isbn
    print(search_book_isbn)
    #with the found ISBN, filter users who gave it a positive rating
    stmt = select(ratings_table.c.user_id).where(ratings_table.c.isbn == search_book_isbn
                                                 and ratings_table.c.book_rating > 5)
    users_who_liked_searched_book = session.execute(stmt).fetchall()
    users = []
    for user in users_who_liked_searched_book:
        users.append(user.user_id)
    stmt = select([ratings_table.c.isbn, ratings_table.c.book_rating], (ratings_table.c.user_id.in_(users)) & (ratings_table.c.book_rating>5))
    books_liked_by_those_users = session.execute(stmt).fetchall()
    books = []
    for book in books_liked_by_those_users:
        books.append(book.isbn)
    stmt = select([ratings_table.c.isbn, func.round(func.avg(ratings_table.c.book_rating)).label("mean"),
                   func.count(ratings_table.c.user_id).label("count")],
                  (ratings_table.c.isbn.in_(books) & (ratings_table.c.book_rating != 0))).group_by("isbn")\
        .having(text("count>9")).order_by(desc(text("count"))).limit(1)
    candidate_book_isbn = session.execute(stmt).fetchone().isbn
    print([candidate_book_isbn])
    stmt = select([books_table.c.book_title], books_table.c.isbn == candidate_book_isbn)
    candidate_book_name = session.execute(stmt).fetchone().book_title
    return [candidate_book_name]


    #these books may have good rating by these users, but are those books good in general?
    #I need a metric that will help me decide which books are actually good
    # what are the parameters?
    # - number of users that gave a vote
    # - ratio of good vs bad ratings
    # - the mean/median score of ratings
    # I could always award points for a book being in top 5 in each category
    # throw a book into a list everytime it scores a point, then count how many times each books is in the
    # list

def get_positive_feedback_users(selected_isbn: str, threshold: int = 7) -> list:
    ratings = dd.read_csv("data\\BX-Book-Ratings_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})

    filter_by_isbn = (ratings["isbn"] == selected_isbn)
    filter_by_threshold_rating = (ratings["book_rating"] >= threshold)
    subselection = ratings[filter_by_isbn & filter_by_threshold_rating].compute()

    if len(subselection) > 0:
        print("We found users who liked this book as well, lets see what other books they liked")
        users = subselection.get("user_id").values
        return users
    else:
        raise SystemExit("Unfortunately, we cannot give you recommendations based on this book")


def candidate_books(users: list, threshold: int = 7) -> list:
    candidates = dd.read_csv("data\\BX-Book-Ratings_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
    filtered_by_candidates = candidates[candidates["user_id"].isin(users)].compute()
    filtering_by_book_rating = filtered_by_candidates[filtered_by_candidates["book_rating"] >= threshold]
    shortlist = filtering_by_book_rating.get("isbn").values

    return shortlist

#TODO pozor mel bych asi resit co se libilo spolecne tem uzivatelum co se libila knizka A


def compute_their_ranking(books: list):
    # filtruje hodnoceni podle seznamu set(uzivatelu) minus puvodni isbn, udela set vsech knizek

    # pro kazdou knizku na seznamu spocita na ?nefiltrovanem datasetu? jake ma hodnoceni; vraci jednu knizku s nejvyssim
    # hodnocenim

    computation = dd.read_csv("data\\BX-Book-Ratings_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
    filtered_for_computation = computation[computation["isbn"].isin(books)].compute()
    print(filtered_for_computation)
    isbn_indexes = filtered_for_computation.groupby("isbn")["book_rating"].sum().reset_index()
    print(isbn_indexes)
    rating_sum = filtered_for_computation.groupby("isbn")["book_rating"].sum().reset_index()["book_rating"]
    rating_count = filtered_for_computation.groupby("isbn")["book_rating"].count().reset_index()["book_rating"]
    custom_rating_metric = rating_sum*rating_count
    highest_rated_index = custom_rating_metric.idxmax()
    highest_rated_isbn = isbn_indexes.loc[highest_rated_index, "isbn"]
    return highest_rated_isbn


def find_the_name(isbn: str) -> str:
    books = dd.read_csv("data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
    filtering = (books["isbn"] == isbn)
    final_recommendation = books[filtering]["book_title"].compute()
    print(f"You will definnetly like {final_recommendation} too!")
    return final_recommendation
