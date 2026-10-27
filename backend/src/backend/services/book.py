from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.schemas.book import BookCreate
from backend.models.book import Book
from backend.models.author import Author
from backend.services.genre_service import add_new_genre



async def get_or_create_book(book_data: BookCreate, db: AsyncSession):
    stmt = select(Book).where(Book.key == book_data.key)
    book = await db.scalar(stmt)

    if not book:
        book_dict = book_data.model_dump(exclude={"genres", "authors"})
        book = Book(**book_dict)
        db.add(book)
        await db.flush()

        if book_data.genres:
            genre_objects = await add_new_genre(db, book_data.genres)
            book.genres = genre_objects

        if book_data.authors:
            author_objects = await get_or_create_author(db, book_data.authors)
            book.authors = author_objects
            
    return book


    
async def get_or_create_author(db: AsyncSession, author_names: list[str]) -> list[Author]:
    aux_author = []
    for name in author_names:

        stmt = select(Author).where(Author.name == name)
        result = await db.execute(stmt)
        author = result.scalars().first()

        if not author:
            author = Author(name=name)
            db.add(author)
            await db.flush() 
            
        aux_author.append(author)
        
    return aux_author