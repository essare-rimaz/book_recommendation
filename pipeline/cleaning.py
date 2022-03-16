import re
import dask.dataframe as dd

books = dd.read_csv(".\\data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
ratings = dd.read_csv(".\\data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})


def removing_extra_semicolons():
    with open("./data/BX-Books.csv", 'r') as f:
        my_csv_text = f.read()

    find_str = '&amp;'
    replace_str = '&'
    find_pokus = r'((?<!\");\".*?)((?<!\");(?!\"))(.*?\";\")'
    replace_pokus = '\\1\\3'
    find_str_2 = r'\\"'
    replace_str_2 = ''

    find_str_4 = " ; "
    replace_str_4 = " "
    find_str_5 = r'((?<!\");\".*?)((?<!\");)(.*?\";\")'
    replace_str_5 = r'\\1\\3'
    find_str_6 = r';";"'
    replace_str_6 = r'";"'


    new_csv_str = re.sub(find_str, replace_str, my_csv_text)
    new_csv_str = re.sub(find_pokus, replace_pokus, new_csv_str)
    new_csv_str = re.sub(find_str_2, replace_str_2, new_csv_str)
    new_csv_str = re.sub(find_str_5, replace_str_5, new_csv_str)
    new_csv_str = re.sub(find_str_6, replace_str_6, new_csv_str)


    # open new file and save
    new_csv_path = './data/BX-Books_cleaned.txt'  # or whatever path and name you want
    with open(new_csv_path, 'w') as f:
        f.write(new_csv_str)

    #TODO turn into a test or at least formalize?

    #TODO remove any than 1 space in Books-Author (eg. T.           T Gunn)

    #TODO remove TRUE duplicates! e.g. "Selected Poems by Rita Dove", "The Kitchen God's Wife", "Into the Deep",
    # Simlarillion
    # so if book title and author name is the same,
    # only one should stay in database -> only the one who has ratings? merge ratings too?

#najdi mi vsechny isbn, ktery nejsou v books
def remove_unknown_books(books, ratings):
    books_unique = books["ISBN"].unique().compute()
    ratings_unique = ratings["ISBN"].unique().compute()
    books_set = set(books_unique)
    ratings_set = set(ratings_unique)
    existing = list(books_set.intersection(ratings_set))
    return existing


def subset_only_existing(existing, books):
    books_filtered = books[books["ISBN"].isin(existing)].compute()
    return books_filtered


ratings = dd.read_csv(".\\data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
books = dd.read_csv(".\\data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
x = remove_unknown_books(books, ratings)

subset_only_existing(x, books)