import pandas as pd
from sqlalchemy.sql import text
from sqlalchemy import create_engine
from sqlalchemy import Table, Column, String, MetaData

#TODO try to setup the project so that it makes sense from DB point of view -> seperate engine, metadata, setup of table
# data,...

FILE_NAME = "data/BX-Books_cleaned.txt"
SQLALCHEMY_DATABSE_URL = "sqlite:///pipeline/test.db"

engine = create_engine(
    SQLALCHEMY_DATABSE_URL, echo=True, future=True
)

metadata_obj = MetaData()

books_table = Table(
    "book_metadata",
    metadata_obj,
    Column("isbn", String, primary_key=True),
    Column("book_title", String(200)),
    Column("book_author", String(100)),
    Column("year_of_publication", String(100)),
    Column("publisher", String(100)),
    Column("image_url_s", String(200)),
    Column("image_url_m", String(200)),
    Column("image_url_l", String(200)),
)

metadata_obj.create_all(engine)

# insert the orignal csv into the database
with open(FILE_NAME, 'r') as file:
    data_df = pd.read_csv(file, encoding="latin1", delimiter=";")
data_df.to_sql('books_table', con=engine, index=True, index_label='id', if_exists='replace')

# check if the length is equal to 271379
print(metadata_obj.tables.keys())
s = text("SELECT count(isbn) FROM books_table")
with engine.connect() as conn:
    with conn.begin():
        result = conn.execute(s).fetchall()
        #TODO make proper tests
        print(result[0])
        assert result[0][0] == 271379
