import re
import dask.dataframe as dd

#books = dd.read_csv(".\\data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
#ratings = dd.read_csv(".\\data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})


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
    new_csv_path = './data/BX-Books.txt'  # or whatever path and name you want
    with open(new_csv_path, 'w') as f:
        f.write(new_csv_str)

    #TODO turn into a test or at least formalize?

    #TODO remove any than 1 space in Books-Author (eg. T.           T Gunn)

    #TODO remove TRUE duplicates! e.g. "Selected Poems by Rita Dove", "The Kitchen God's Wife", "Into the Deep",
    # Simlarillion
    # so if book title and author name is the same,
    # only one should stay in database -> only the one who has ratings? merge ratings too?

#for better manipulation with DB
def rename_book_table_cols(books):
    books_renamed = books.rename(columns={"ISBN": "isbn",
                                           "Book-Title": "book_title",
                                           "Book-Author": "book_author",
                                           "Year-Of-Publication": "year_of_publication",
                                           "Publisher": "publisher",
                                           "Image-URL-S": "image_s",
                                           "Image-URL-M": "image_m",
                                           "Image-URL-L": "image_l"}).compute()

    # open new file and save
    new_csv_path = './data'  # or whatever path and name you want
    books_renamed.to_csv(".\\data\\BX-Books_cleaned.txt", sep=";", index=False)
    #books_renamed.write("\data\myfile.txt")


def rename_rating_table_cols(ratings):
    ratings_renamed = ratings.rename(columns={"User-ID": "user_id",
                                              "ISBN": "isbn",
                                              "Book-Rating": "book_rating"}).compute()
    ratings_renamed.to_csv(".\\data\\BX-Book-Ratings_cleaned.txt", sep=";", index=False)


#najdi mi vsechny isbn, ktery nejsou v books
def remove_unknown_books(books, ratings):
    books_unique = books["isbn"].unique().compute()
    ratings_unique = ratings["isbn"].unique().compute()
    books_set = set(books_unique)
    ratings_set = set(ratings_unique)
    existing = list(books_set.intersection(ratings_set))
    return existing


#TODO asi nema momentalne na nic efekt?
def subset_only_existing(existing, books):
    books_filtered = books[books["isbn"].isin(existing)].compute()
    return books_filtered

removing_extra_semicolons()
books = dd.read_csv(".\\data\\BX-Books.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
ratings = dd.read_csv(".\\data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})

rename_book_table_cols(books)
rename_rating_table_cols(ratings)
ratings = dd.read_csv(".\\data\\BX-Book-Ratings_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
books = dd.read_csv(".\\data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
x = remove_unknown_books(books, ratings)

print(len(subset_only_existing(x, books)))
