import sys
from pipeline.interface import parse_args
from pipeline.interface_processing import get_positive_feedback_users, candidate_books, \
    compute_their_ranking, find_the_name
from pipeline.disambiguation import disambiguate_book_choice


if __name__ == "__main__":
    parser = parse_args(sys.argv[1:])
    isbn = disambiguate_book_choice(parser.book_title[0])
    users = get_positive_feedback_users(isbn)
    books = candidate_books(users)
    find_the_name(compute_their_ranking(books))
