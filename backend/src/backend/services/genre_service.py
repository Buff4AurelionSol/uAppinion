from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.models.book import Genre



async def add_new_genre(db: AsyncSession, genresReceived: list[str]) -> list[Genre]:
    if not genresReceived: 
        return []

    genres_without_spaces = list(set([genre.strip().lower() for genre in genresReceived]))

    stmt = select(Genre).where(Genre.name.in_(genres_without_spaces))
    result = await db.scalars(stmt)
    existing_genres = result.all()
    
    genres_map = {genre.name: genre for genre in existing_genres}

    genres_object = []

    for name in genres_without_spaces:
        if name in genres_map:
            genres_object.append(genres_map[name])
        else: 
            new_genre = Genre(name=name)
            db.add(new_genre)
            genres_object.append(new_genre)
            
    await db.flush()
    return genres_object


async def get_all_genres(db: AsyncSession):
    stmt = select(Genre)
    result = await db.scalars(stmt)
    return result.all()