import dask.dataframe as dd
import pyinputplus as pyip


def check_for_duplicates(book_title: str) -> tuple[str, str]:
    books = dd.read_csv("data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
    filter_by_book_title = (books["Book-Title"] == book_title)

    books_with_this_title = books[filter_by_book_title].compute()
    if len(books_with_this_title) > 1:
        disambiguated_author = ask_for_author_specification(give_duplicated_authors_options(books_with_this_title))
        return book_title, disambiguated_author
    else:
        author = list(books_with_this_title.get("Book-Author"))[0]
        return book_title, author


def give_duplicated_authors_options(subselection: dd) -> list:
    possible_author_choices = subselection["Book-Author"]
    return possible_author_choices


def ask_for_author_specification(authors: list):
    print("This book title exists for multiple authors.")
    result = pyip.inputMenu(list(authors))
    return result


def get_isbn_of_given_book(book_title: str, book_author: str) -> str:
    books = dd.read_csv("data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})

    filter_by_book_title = (books["Book-Title"] == book_title)
    filter_by_book_author = (books["Book-Author"] == book_author)
    subselection = books[filter_by_book_title & filter_by_book_author].compute()
    selected_isbn = subselection.get("ISBN").values[0]

    print(f"It's ISBN is {selected_isbn}")
    return selected_isbn
