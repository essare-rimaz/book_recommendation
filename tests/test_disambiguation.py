from pipeline.disambiguation import get_isbn_of_given_book
import pytest

TESTING_ISBN = [
    ("The Mummies of Urumchi", "E. J. W. Barber", "0393045218"),
    ("IBM PC & XT assembly language: A guide for programmers", "Leo J Scanlon", "0893035750"),
    ("Rhyming Cockney slang", "Jack Jones", "0902920049")

]


@pytest.mark.parametrize("test_book_title, test_book_author, expected_isbn", TESTING_ISBN)
def test_book_validation(test_book_title, test_book_author, expected_isbn):
    assert get_isbn_of_given_book(test_book_title, test_book_author) == expected_isbn


    #assert isinstance("Rhyming Cockney slang", str)