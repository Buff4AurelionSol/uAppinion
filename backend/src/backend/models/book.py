from backend.config.db import Base
from sqlalchemy import String,  Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .associations import book_genre_association

class Book(Base): 
    __tablename__ = "books"
    key: Mapped[str] = mapped_column(primary_key=True, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_publish_year: Mapped[int| None] = mapped_column(Integer, nullable=True)
    cover_i: Mapped[int | None] = mapped_column(Integer, nullable=True)

    genres: Mapped[list["Genre"]] = relationship(
        secondary=book_genre_association, 
        back_populates="books"
    )


class Genre(Base): 
    __tablename__ = "genres"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(unique=True, nullable=False)

    books: Mapped[list["Book"]] = relationship(
        secondary=book_genre_association, 
        back_populates="genres"
    )