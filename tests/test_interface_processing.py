from pipeline.interface_processing import get_positive_feedback_users
from pipeline.disambiguation import get_isbn_of_given_book
import pytest


POSITIVE_RANKING = [
    ("Tell Me This Isn't Happening", "Robynn Clairday")
]


@pytest.mark.parametrize("test_book_title, test_book_author", POSITIVE_RANKING)
def test_rating_validation_positive_exists(test_book_title, test_book_author):
    assert len(get_positive_feedback_users(get_isbn_of_given_book(test_book_title, test_book_author), 7)) > 0


# https://miguendes.me/how-to-check-if-an-exception-is-raised-or-not-with-pytest
def test_exit():
    with pytest.raises(BaseException) as pytest_wrapped_e:
        get_positive_feedback_users("0393045218", 7)
    assert pytest_wrapped_e.type == SystemExit
    assert "Unfortunately, we cannot give you recommendations based on this book" in str(pytest_wrapped_e.value)


