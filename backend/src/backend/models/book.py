from backend.config.db import Base
from sqlalchemy import String,  Integer
from sqlalchemy.orm import Mapped, mapped_column

class Book(Base): 
    __tablename__ = "books"
    key: Mapped[str] = mapped_column(primary_key=True, unique=True, index=True)
    title: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    first_publish_year: Mapped[int| None] = mapped_column(Integer, nullable=True)
    cover_i: Mapped[int | None] = mapped_column(Integer, nullable=True)
    