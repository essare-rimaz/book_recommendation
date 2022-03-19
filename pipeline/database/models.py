from sqlalchemy import Column, String
from pipeline.database.database import Base


class Book(Base):
    __tablename__ = "Book"
    isbn = Column(String, primary_key=True)
    book_title = Column(String(200))
    book_author = Column(String(100))
    year_of_publication = Column(String(100))
    publisher = Column(String(100))
    image_url_s = Column(String(200))
    image_url_m = Column(String(200))
    image_url_l = Column(String(200))

    def __init__(self):
        isbn = self.isbn
