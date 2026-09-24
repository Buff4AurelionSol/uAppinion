from backend.schemas.review import ReviewCreate
from backend.models.review import Review
from backend.models.book import Book, Genre
from backend.models.author import Author
from backend.services.genre_service import add_new_genre
from sqlalchemy.orm import Session, contains_eager, Query
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import func, or_

import math


def create_review_with_book(review_in: ReviewCreate, db: Session) -> Review:
    try:
        db_book = db.query(Book).filter(Book.key == review_in.book.key).first()

        if not db_book:
            book_data = review_in.book.model_dump(exclude={"genres", "authors"})
            db_book = Book(**book_data)
            db.add(db_book)
            db.flush()

            if(hasattr(review_in.book, "genres") and review_in.book.genres):
                genre_object = add_new_genre(db, review_in.book.genres)
                db_book.genres = genre_object

            if(hasattr(review_in.book, "authors") and review_in.book.authors):
                db_book.authors = get_or_create_author(db, review_in.book.authors)

        review_data = review_in.model_dump(exclude={"book"})
        new_review = Review(**review_data, book_id=db_book.key)

        db.add(new_review)
        db.commit()
        db.refresh(new_review)
        return new_review
       
    except IntegrityError as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
          detail=f"Error de base de datos: {e.orig}"
        )

    except Exception as e:
        db.rollback()
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Ocurrió un error inesperado: {str(e)}"
        )

def get_my_library_books(db:Session, page: int = 1, limit:int = 10, search: str = None, genre_id: int = None, order_by: str = None): 

    offset = (page - 1) * limit
    query = db.query(Review).join(Review.book)

    total_pages_read = db.query(func.sum(Review.num_pages)).scalar() or 0

    if search:
        search_aux = f"%{search}%"
        query = query.filter(or_(Book.title.ilike(search_aux), Book.authors.any(Author.name.ilike(search_aux))))

    if genre_id:
        query = query.filter(Book.genres.any(Genre.id == genre_id))


    total = query.count()

    if(total < 1): return {"reviews": [], "total": 0,  "total_pages_read": total_pages_read,  "limit": limit, "pages": 0, }

    query = apply_book_order(query, order_by)

    items = (
        query
        .options(
            contains_eager(Review.book).selectinload(Book.authors),
            contains_eager(Review.book).selectinload(Book.genres)
        )
        .offset(offset)
        .limit(limit)
        .all()
    )

    pages = math.ceil(total/limit)


    return { 
        "reviews": items, 
        "total": total,
        "total_pages_read": total_pages_read, 
        "limit":limit, 
        "pages": pages
    }


def apply_book_order(query: Query, order_by: str) -> Query: 
    match order_by:
        case "title_asc":
            return query.order_by(func.lower(Book.title).asc())

        case "date":
            return query.order_by(Book.first_publish_year.desc())

        case "created_at" | _:
            return query.order_by(Review.created_at.desc())

def get_or_create_author(db:Session,author_names:list[str]) -> list[Author]:
    aux_author = []
    for name in author_names:
        author = db.query(Author).filter(Author.name == name).first()
        if not author:
            author = Author(name=name)
            db.add(author)
            db.flush()
        aux_author.append(author)
    return aux_author