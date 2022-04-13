import dask.dataframe as dd

#TODO zkusit vyuzivat stejny processing jako webapp?

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
    print(f"You will definitely like {final_recommendation} too!")
    return final_recommendation