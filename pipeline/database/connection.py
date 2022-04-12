from pipeline.database.database import SessionLocal, engine
from sqlalchemy import select, MetaData

def database_connection():
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    books_table = meta_data.tables["books_table"]
    ratings_table = meta_data.tables["ratings_table"]
    session = SessionLocal()

    return books_table, ratings_table, session