import sys
from pipeline.interface import parse_args
from pipeline.processing import get_positive_feedback_users, candidate_books, \
    compute_their_ranking, find_the_name
from pipeline.disambiguation import get_isbn_of_given_book, check_for_duplicates


if __name__ == "__main__":
    parser = parse_args(sys.argv[1:])
    disambiguated_book_title, author = check_for_duplicates(parser.book_title[0])
    isbn = get_isbn_of_given_book(disambiguated_book_title, author)
    users = get_positive_feedback_users(isbn)
    books = candidate_books(users)
    find_the_name(compute_their_ranking(books))
