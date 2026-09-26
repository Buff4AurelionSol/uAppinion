from backend.schemas.review import ReviewCreate
from backend.models.review import Review
from backend.models.book import Book, Genre
from backend.models.author import Author
from backend.services.genre_service import add_new_genre
from sqlalchemy.orm import Session, contains_eager, Query
from fastapi import HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select, func, or_, desc
from backend.const.consts import statusesValues
from datetime import date

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

def get_my_metrics_books(
    db:Session, 
    status: str ="read",  
    year: int| None = None, 
    start_date:date| None = None, 
    end_date: date| None = None
):
    
    base_filter = build_status_filter_to_review(
     status=status, 
     year=year,
     start_date=start_date, 
     end_date=end_date
    )

    group_by_month = True if year or (start_date and end_date and start_date.year == end_date.year) else False
    time_format = "YYYY-MM" if group_by_month else "YYYY"
    time_bucket = func.to_char(Review.finish_date, time_format)
    
    total_books_read, total_pages_read, average_pages_read = db.query(
        func.count(Review.id),
        func.sum(Review.num_pages),
        func.avg(Review.num_pages)
        ).filter(*base_filter).first()


    books_per_period_query = db.query(
        time_bucket.label("period"), 
        func.count(Review.id).label("total"),
        func.sum(Review.num_pages).label("total_pages")
    ).filter(
        *base_filter,
        Review.finish_date.isnot(None)
    ) .group_by(time_bucket).order_by(time_bucket.desc()).all()

    books_per_period = [{"period": row.period, "total": row.total} for row in books_per_period_query]
    pages_per_period = [{"period": row.period, "total_pages": row.total_pages or 0} for row in books_per_period_query]
    
    top_genres = get_top_genres(db, base_filter)
    top_authors = get_top_authors(db, base_filter)

    return {
        "total_books_read": total_books_read or 0,
        "total_pages_read": total_pages_read or 0,
        "average_pages_read": round(float(average_pages_read), 2) if average_pages_read else 0,
        "books_per_period": books_per_period,
        "pages_per_period": pages_per_period,
        "top_genres": top_genres,
        "top_authors": top_authors
    }
    

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

def get_top_genres(db:Session, base_filters: list):

    top_genres_query = db.query(
        Genre.name.label("genre_name"),
        func.count(Review.id).label("total_books")
    ).join(Book, Review.book_id == Book.key)\
    .join(Book.genres)\
    .filter(*base_filters)\
    .group_by(Genre.id, Genre.name)\
    .order_by(desc("total_books"))\
    .limit(10).all()

    return [{"name": row.genre_name, "books": row.total_books} for row in top_genres_query]

def get_top_authors(db:Session, base_filters: list):

    stm = (
        select(
            Author.name.label("author_name"),
            func.count(Review.id).label("total_books"),
            func.sum(Review.num_pages).label("total_pages")
    )
    .join(Book, Review.book_id == Book.key)
    .join(Book.authors)
    .where(*base_filters)
    .group_by(Author.id, Author.name)
    .order_by(desc("total_books"))
    .limit(10))

    top_authors = db.execute(stm).all()

    return [{"name": row.author_name, "total_books": row.total_books, "total_pages": row.total_pages} for row in top_authors]

def apply_book_order(query: Query, order_by: str) -> Query: 
    match order_by:
        case "title_asc":
            return query.order_by(func.lower(Book.title).asc())

        case "date":
            return query.order_by(Book.first_publish_year.desc())

        case "created_at" | _:
            return query.order_by(Review.created_at.desc())


def build_status_filter_to_review(
    status: str | None = None, 
    year: int | None = None, 
    start_date: date | None = None,
    end_date: date | None = None
) -> list:
    
    base_filters = []
    if status and status in statusesValues:
        base_filters.append(Review.status == status)
    if start_date:
        base_filters.append(Review.start_date >= start_date)
    if end_date:
        base_filters.append(Review.finish_date <= end_date)
    elif year: 
        base_filters.append(Review.start_date >= date(year, 1,1))
        base_filters.append(Review.finish_date <= date(year,12,31))

    return base_filters
    