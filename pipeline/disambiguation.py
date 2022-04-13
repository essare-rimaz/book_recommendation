import dask.dataframe as dd
import pyinputplus as pyip
import re

#TODO momentalne hledam vse v datech, ale uz mam databazi -> zmenit?

def disambiguate_book_choice(book_title: str) -> str:
    books = dd.read_csv("data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})
    filter_by_book_title = (books["book_title"] == book_title)

    books_with_this_title = books[filter_by_book_title].compute()
    print(f"subselection is {books_with_this_title}")
    if len(books_with_this_title) > 1:
        isbn = ask_for_specification(give_duplicated_entries_options(books_with_this_title))
        return isbn
    elif len(books_with_this_title) == 1:
        author = list(books_with_this_title.get("book_author"))[0]
        isbn = get_isbn_of_given_book(book_title, author)
        return isbn
    else:
        print("We could not find the book you are looking for")


def give_duplicated_entries_options(subselection) -> list:
    # Create an empty list
    possible_isbn_choices = []

    # Iterate over each row
    for index, rows in subselection.iterrows():
        # Create list for the current row
        isbn_choice = "ISBN: " + rows.isbn+" "+"by " + rows.book_author +" from "+ str(rows.year_of_publication)

        # append the list to the final list
        possible_isbn_choices.append(isbn_choice)

    return possible_isbn_choices


def ask_for_specification(choices: list):
    print("This book title exists for multiple authors.")
    result = pyip.inputMenu(choices, lettered=False, numbered=True)

    isbn_regex = re.search('ISBN:\s(.*?)\s', result)

    isbn = isbn_regex.group(1)

    return isbn


def get_isbn_of_given_book(book_title: str, book_author: str) -> str:
    books = dd.read_csv("data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"isbn": "string"})

    filter_by_book_title = (books["book_title"] == book_title)
    filter_by_book_author = (books["book_author"] == book_author)
    subselection = books[filter_by_book_title & filter_by_book_author].compute()
    selected_isbn = subselection.get("isbn").values[0]

    print(f"It's isbn is {selected_isbn}")
    return selected_isbn
