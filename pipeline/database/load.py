import pandas as pd
from pipeline.database import models
from pipeline.database.database import SessionLocal, engine


def something():
    print("creating database")

    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    FILE_NAME = r"data/BX-Books_cleaned.txt"

    with open(FILE_NAME, 'r') as file:
        data_df = pd.read_csv(file, encoding="latin1", delimiter=";")
    data_df.to_sql('books_table', con=engine, index=False,  if_exists='append')

#
# with open("data/BX-Books_cleaned.csv", "r") as f:
#     csv_reader = csv.DictReader(f)
#
#     for row in csv_reader:
#         print(row)
#         db_record = models.Book(
#             isbn=row["isbn"],
#             book_title = row["book_title"],
#             book_author = row["book_author"],
#             year_of_publication = row["year_of_publication"],
#             publisher = row["publisher"],
#             image_url_s = row["image_s"],
#             image_url_m = row["image_m"],
#             image_url_l = row["image_l"],
#         )
#         db.add(db_record)
#     db.commit()
