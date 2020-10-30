from sqlalchemy import (
    Table, MetaData, Column, Integer, String, Date, DateTime,
    ForeignKey
)
from sqlalchemy.orm import mapper, relationship

from mbrowser.domain import model

metadata = MetaData()

users = Table(
    'users', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('username', String(255), unique=True, nullable=False),
    Column('password', String(255), nullable=False)
)

reviews = Table(
    'reviews', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.id')),
    Column('movie_id', ForeignKey('movies.id')),
    Column('review', String(1024), nullable=False),
    Column('timestamp', DateTime, nullable=False)
)

movies = Table(
    'movies', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('release_year', String(255), nullable=False),
    Column('title', String(255), nullable=False),
    Column('description', String(1024), nullable=False)
)

genres = Table(
    'genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

directors = Table(
    'directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

actors = Table(
    'actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('name', String(64), nullable=False)
)

movie_genres = Table(
    'movie_genres', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('genre_id', ForeignKey('genres.id')),
)

movie_directors = Table(
    'movie_directors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('director_id', ForeignKey('directors.id')),
)

movie_actors = Table(
    'movie_actors', metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('movie_id', ForeignKey('movies.id')),
    Column('actor_id', ForeignKey('actors.id')),
)


def map_model_to_tables():
    mapper(model.User, users, properties={
        '_username': users.c.username,
        '_password': users.c.password,
        '_reviews': relationship(model.Review, backref='_user')
    })
    mapper(model.Review, reviews, properties={
        '_review': reviews.c.review,
        '_timestamp': reviews.c.timestamp
    })
    movies_mapper = mapper(model.Movie, movies, properties={
        '_id': movies.c.id,
        '_release_year': movies.c.release_year,
        '_title': movies.c.title,
        '_description': movies.c.description,
        '_reviews': relationship(model.Review, backref='_movie'),
    })
    mapper(model.Genre, genres, properties={
        '_genre_name': genres.c.name,
        '_genre_movies': relationship(
            movies_mapper,
            secondary=movie_genres,
            backref="_genres"
        )
    })
    mapper(model.Director, directors, properties={
        '_director_full_name': directors.c.name,
        '_director_movies': relationship(
            movies_mapper,
            secondary=movie_directors,
            backref="_directors"
        )
    })
    mapper(model.Actor, actors, properties={
        '_actor_name': actors.c.name,
        '_actor_movies': relationship(
            movies_mapper,
            secondary=movie_actors,
            backref="_actors"
        )
    })