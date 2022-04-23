import pandas as pd
from pipeline.database import models
from pipeline.database.database import SessionLocal, engine


def create_database():
    print("Creating database")

    db = SessionLocal()

    models.Base.metadata.create_all(bind=engine)

    BOOKS_FILE_NAME = r"data/BX-Books_cleaned.txt"
    RATINGS_FILE_NAME = r"data/BX-Book-Ratings_cleaned.txt"
    with open(BOOKS_FILE_NAME, 'r') as file:
        data_df = pd.read_csv(file, encoding="latin1", delimiter=";")
    data_df.to_sql('books_table', con=engine, index=False,  if_exists='append')

    with open(RATINGS_FILE_NAME, 'r') as file:
        data_df = pd.read_csv(file, encoding="latin1", delimiter=";")
    data_df.to_sql('ratings_table', con=engine, index=False,  if_exists='append')
