from fastapi import HTTPException, status
from sqlalchemy import select, or_ 
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.exc import IntegrityError
from backend.models.book import Book
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
        status= userBookData.status,
        num_pages=userBookData.num_pages,
        start_date=userBookData.start_date,
        finish_date=userBookData.finish_date,
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

        userBookPayload = UserBookCreate(
            id=userBookData.id,
            book_id=book.key,
            status=userBookData.status,
            num_pages=userBookData.num_pages,
            start_date=userBookData.start_date,
            finish_date=userBookData.finish_date
        )

        user_book = await create_user_book(userBookPayload, user_id, db)

        if userBookData.review and userBookData.review.text_review and userBookData.review.text_review.strip():
            userBookData.review.book_id = book.key
            await create_review(userBookData.review, user_id, db)

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
    
    