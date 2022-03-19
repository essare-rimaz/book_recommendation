from pipeline.database.cleaning import remove_unknown_books, subset_only_existing
import dask.dataframe as dd
import pytest

#TODO prepsat at to testuje vystup z cleaning
# pouzit teardown <3


BOOK_LIST = [
    r"^Tropical aquariums$",
    #r"^Selected poems$", # TODO jsou tam dvakrat! To je dost zasadni info, takze by se navic hodilo mit promennou output
    #ISBN ...744 a 726, ...800, ... 465, ...58X, ...548, ....984, ...541,....897,...190,....498,...265,...830...
    r"^The captive$",
    r"^Songs & Rhymes for Wiggle Worms$",
    r"^Earth, air, fire & water: Poems$",
    r"^Three Weddings & a Kiss$",
    r"^Bathrooms Planning & Remodeling: Planning & Remodeling \(Southern Living \(Paperback Sunset\)\)$",
    r"^The First Jewish Catalog; A Do-It-Yourself Kit$",
    r"^The Israelis;: Founders and sons$",
    r"^The heart of the matter ; Stamboul train ; A burnt-out case ; The third man ; The quiet American ; Loser takes all ; The power and the glory$"
]

DUPLICATED_LIST = [
    r"^Selected Poems$"
]

@pytest.fixture
def get_cleaned_books_data():
    books = dd.read_csv(".\\data\\BX-Books_cleaned.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
    return books


@pytest.fixture
def get_ratings_data():
    ratings = dd.read_csv(".\\data\\BX-Book-Ratings.txt", encoding="latin1", delimiter=";", dtype={"ISBN": "string"})
    return ratings


@pytest.mark.parametrize("book_list", BOOK_LIST)
def test_book_validation_trailing_semicolon(get_cleaned_books_data, book_list):
    """testing cleaning of ';";"'
    For example ";"Tropical aquariums;";"
    """
    assert len(get_cleaned_books_data["Book-Title"][
                   get_cleaned_books_data["Book-Title"].str.contains(book_list, regex=True)].compute()) == 1


@pytest.mark.parametrize("book_list", DUPLICATED_LIST)
def test_duplicated_books(get_cleaned_books_data, book_list):
    assert len(get_cleaned_books_data["Book-Title"][get_cleaned_books_data["Book-Title"].str.contains(book_list, regex=True)].compute()) > 1


def test_shape_of_table_with_only_known_books(get_cleaned_books_data, get_ratings_data):
    existing = remove_unknown_books(get_cleaned_books_data, get_ratings_data)
    assert len(subset_only_existing(existing, get_cleaned_books_data)) == 270170

