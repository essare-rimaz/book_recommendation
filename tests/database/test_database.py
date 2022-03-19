from pipeline.database.database import SessionLocal, engine
from sqlalchemy import MetaData, select, func, text
import pytest


@pytest.fixture
def create_session():
    session = SessionLocal()
    return session


@pytest.fixture
def create_metadata():
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    tables = meta_data.tables["books_table"]
    return tables


def test_shape_of_database(create_session, create_metadata):
    assert create_session.query(func.count(create_metadata.c.isbn)).scalar() == 271379


def test_book_retrieval(create_session, create_metadata):
    query = f"SELECT COUNT({create_metadata.c.isbn}) FROM {create_metadata} WHERE {create_metadata.c.book_title} == 'Into the Deep'"
    assert create_session.execute(text(query)).fetchall()[0][0] == 2
