import argparse
# TODO chci aby to byl bud jeden nebo druhy, ne oba
# TODO az budu umet tohle, tak umet vyprint to co se zrovna zadalo
# TODO optional argument, ktery bude defaultne 1 -> pocet doporucovanych knih


def parse_args(args):
    parser = argparse.ArgumentParser(prog="Book recommendation system",
                                     description='Insert a book you liked to get a recommendation on another one')
    parser.add_argument('book_title', metavar='bt', type=str, nargs=1,
                        help='a title of the book you want your recommendation to be based on')
    # ...Create your parser as you like...
    parsed_args = parser.parse_args(args)
    print(f"You want to recommend similar book as: {parsed_args.book_title[0]}")
    return parser.parse_args(args)


# https://docs.python.org/3/library/argparse.html
# chci vytvorit interface pro prikazovou radku kde budu moct zadat bud isbn nebo book title



