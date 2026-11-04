import math
from fastapi import HTTPException, status
from sqlalchemy import select, or_, func 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload
from backend.models.book import Book, Genre
from backend.models.author import Author
from backend.models.user_book import UserBook
from backend.schemas.user_book import UserBookCreate, UserBookWithReview, UserBookUpdate
from backend.schemas.review import ReviewCreate
from backend.services.review_service import create_review
from backend.services.book import get_or_create_book

async def create_user_book(
        userBookData: UserBookCreate, 
        user_id: str,  
        db: AsyncSession
):
    new_user_book = UserBook(
        id=userBookData.id,
        user_id=user_id,
        book_id= userBookData.book_id,
        format=userBookData.format,
        status= userBookData.status,
        num_pages=userBookData.num_pages,
        start_date=userBookData.start_date,
        finish_date=userBookData.finish_date,
        is_reread=userBookData.is_reread
    )

    db.add(new_user_book)
    await db.flush()
    return new_user_book

async def create_user_book_with_review(
        userBookData: UserBookWithReview,
        user_id: str, 
        db: AsyncSession
):
    try:
        book = await get_or_create_book(userBookData.book, db)

        existing_read_stmt = select(UserBook).where(
            UserBook.user_id == user_id,
            UserBook.book_id == book.key
        )

        existings_read = await db.scalars(existing_read_stmt)
        has_previous_reads = existings_read.first() is not None
        is_read_value = True if has_previous_reads else userBookData.is_reread

        userBookPayload = UserBookCreate(
            id=userBookData.id,
            book_id=book.key,
            status=userBookData.status,
            format=userBookData.format,
            num_pages=userBookData.num_pages,
            start_date=userBookData.start_date,
            finish_date=userBookData.finish_date,
            is_reread=is_read_value
        )

        user_book = await create_user_book(userBookPayload, user_id, db)

        if userBookData.review and userBookData.review.text_review and userBookData.review.text_review.strip():
            userBookData.review.user_book_id = user_book.id
            await create_review(userBookData.review, db)

        await db.commit()
        await db.refresh(user_book)
  
        return user_book    
    
    except IntegrityError as e:
        await db.rollback()
        raise ValueError("Este libro ya se encuentra registrado en tu biblioteca")

    except Exception as e:
        await db.rollback()
        print(f"ERROR : {type(e).__name__} -> {str(e)}")
        raise e

async def get_my_library(
        user_id: str, 
        db: AsyncSession,
        page: int = 1,
        limit: int = 10,
        search: str = None, 
        genre_id: int = None, 
        order_by: str = None
):
    stmt_library = (
        select(UserBook).
        join(Book).
        options(joinedload(UserBook.book)).
        where(UserBook.user_id == user_id)
    )

    offset = (page - 1) * limit

    if search: 
        search_aux = f"%{search}%"
        stmt_library  = stmt_library.where(
            or_(
                Book.title.ilike(search_aux),
                Book.authors.any(Author.name.ilike(search_aux))
            )
        )

    if genre_id:
        stmt_library = stmt_library.where(Book.genres.any(Genre.id == genre_id))

    match order_by:
        case "title_asc":
             stmt_library = stmt_library.order_by(func.lower(Book.title).asc())

        case "date":
            stmt_library = stmt_library.order_by(Book.first_publish_year.desc())

        case "created_at":
            stmt_library = stmt_library.order_by(UserBook.created_at.desc())
    
    stmt  = stmt_library.offset(offset).limit(limit)
    
    subquery = stmt_library.subquery()
    
    books_basic_metrics = select(
        func.count(),
        func.coalesce(func.sum(subquery.columns.num_pages), 0)
    )

    metrics_result = await db.execute(books_basic_metrics)
    total, total_pages = metrics_result.first()

    if total < 1: 
        return {
            "library": [], 
            "total": 0, 
            "total_pages": total_pages, 
            "limit": limit, 
            "pages": 0
        }

    items = await db.scalars(stmt)
    library_items = items.all()
    pages = math.ceil(total/limit)

    return {
        "library": library_items,
        "total": total,
        "total_pages_books": total_pages,
        "limit": limit,
        "pages": pages
    }


async def update_user_book(
        user_id: str, 
        user_book_id: str,
        user_book_update: UserBookUpdate,
        db: AsyncSession
): 
    stmt = select(UserBook).where(
        UserBook.id == user_book_id,
        UserBook.user_id == user_id  
    )
    user_book = await db.scalar(stmt)

    if not user_book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="No se encuentró el libro en su biblioteca"
        )
    update_dict = user_book_update.model_dump(exclude_unset=True)

    for key, value in update_dict.items():
        setattr(user_book, key, value)

    await db.commit()
    await db.refresh(user_book)
    return user_book


async def delete_user_book(
        user_id: str,
        user_book_id: str,
        db: AsyncSession
):
        try: 
            stmt = select(UserBook).where(
                UserBook.id == user_book_id,
                UserBook.user_id == user_id
            )
        
            user_book = await db.scalar(stmt)
        
            if not user_book: 
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No se encontró el libro en su biblioteca"
                )
    
            await db.delete(user_book)
            await db.commit()

            return {"message": "Libro eliminado de la biblioteca"}
        
        except HTTPException as e:
            raise e

        except Exception as e: 
            await db.rollback()
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Ocurrió un error al intentar eliminar el registro"
            )
