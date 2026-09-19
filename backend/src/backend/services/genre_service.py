from sqlalchemy.orm import Session
from backend.models.book import Genre


def add_new_genre(db:Session, genresReceived: list[str]):
    if not genresReceived: 
        return []

    genres_without_spaces = list(set([genre.strip().lower() for genre in genresReceived]))
    existing_genres = db.query(Genre).filter(Genre.name.in_(genres_without_spaces)).all()
    genres_map = {genre.name : genre for genre in existing_genres}

    genres_object = []

    for name in genres_without_spaces:
        if  name in genres_map:
            genres_object.append(genres_map[name])
        else: 
            new_genre = Genre(name = name)
            db.add(new_genre)
            genres_object.append(new_genre)
    db.flush()
    return genres_object

def get_all_genres(db:Session):
    all_genres = db.query(Genre).all()
    return all_genres