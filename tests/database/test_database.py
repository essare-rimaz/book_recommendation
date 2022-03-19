from pipeline.database.database import SessionLocal, engine
from sqlalchemy import MetaData, select, func, text
import pytest


@pytest.fixture
def create_session():
    session = SessionLocal()
    return session


@pytest.fixture
def create_book_metadata():
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    table = meta_data.tables["books_table"]
    return table


@pytest.fixture
def create_rating_metadata():
    meta_data = MetaData(bind=engine)
    MetaData.reflect(meta_data)
    table = meta_data.tables["ratings_table"]
    return table


def test_shape_of_book_table(create_session, create_book_metadata):
    assert create_session.query(func.count(create_book_metadata.c.isbn)).scalar() == 271379


def test_book_retrieval(create_session, create_book_metadata):
    query = f"SELECT COUNT({create_book_metadata.c.isbn}) FROM {create_book_metadata} WHERE {create_book_metadata.c.book_title} == 'Into the Deep'"
    assert create_session.execute(text(query)).fetchall()[0][0] == 2


def test_shape_of_rating_table(create_session, create_rating_metadata):
    assert create_session.query(func.count(create_rating_metadata.c.isbn)).scalar() == 1149780