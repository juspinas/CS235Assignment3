import csv
import os

from datetime import date
from typing import List

from sqlalchemy import desc, asc
from sqlalchemy.engine import Engine
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from werkzeug.security import generate_password_hash

from sqlalchemy.orm import scoped_session
from flask import _app_ctx_stack

from mbrowser.domain.model import Director, Genre, Actor, Movie, User, Review
from mbrowser.adapters.abstract_repository import AbstractRepository

directors = None
actors = None
genres = None


class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory, scopefunc=_app_ctx_stack.__ident_func__)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    def add_user(self, user: User):
        with self._session_cm as scm:
            scm.session.add(user)
            scm.commit()

    def get_user(self, username) -> User:
        user = None
        try:
            user = self._session_cm.session.query(User).filter_by(_username=username).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return user

    def add_movie(self, movie: Movie):
        with self._session_cm as scm:
            scm.session.add(movie)
            scm.commit()

    def get_movie(self, id: int) -> Movie:
        movie = None
        try:
            movie = self._session_cm.session.query(Movie).filter(Movie._id == id).one()
        except NoResultFound:
            # Ignore any exception and return None.
            pass

        return movie

    def get_movies(self) -> List[Movie]:
        id_list = list(range(1, 1000)) 
        movies = self._session_cm.session.query(Movie).filter(Movie._id.in_(id_list)).all()
        return movies

    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        if target_year is None:
            movies = self._session_cm.session.query(Movie).all()
            return movies
        else:
            # Return movies matching target_year; return an empty list if there are no matches.
            movies = self._session_cm.session.query(Movie).filter(Movie._release_year == target_year).all()
            return movies

    def get_number_of_movies(self):
        number_of_movies = self._session_cm.session.query(Movie).count()
        return number_of_movies

    def get_first_movie(self):
        movie = self._session_cm.session.query(Movie).first()
        return movie

    def get_last_movie(self):
        movie = self._session_cm.session.query(Movie).order_by(desc(Movie._id)).first()
        return movie

    def get_movies_by_id(self, id_list):
        movies = self._session_cm.session.query(Movie).filter(Movie._id.in_(id_list)).all()
        return movies

    def get_movie_ids_for_genre(self, genre_name: str):
        movie_ids = []

        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table.
        row = self._session_cm.session.execute('SELECT id FROM genres WHERE name = :genre_name', {'genre_name': genre_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movie_ids = list()
        else:
            genre_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_genres WHERE genre_id = :genre_id ORDER BY movie_id ASC',
                    {'genre_id': genre_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_movie_ids_for_director(self, director_full_name: str):
        movie_ids = []

        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table.
        row = self._session_cm.session.execute('SELECT id FROM directors WHERE name = :director_full_name', {'director_full_name': director_full_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movie_ids = list()
        else:
            director_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_directors WHERE director_id = :director_id ORDER BY movie_id ASC',
                    {'director_id': director_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_movie_ids_for_actor(self, actor_full_name: str):
        movie_ids = []

        # Use native SQL to retrieve movie ids, since there is no mapped class for the movie_genres table.
        row = self._session_cm.session.execute('SELECT id FROM actors WHERE name = :actor_full_name', {'actor_full_name': actor_full_name}).fetchone()

        if row is None:
            # No tag with the name tag_name - create an empty list.
            movie_ids = list()
        else:
            actor_id = row[0]

            # Retrieve article ids of articles associated with the tag.
            movie_ids = self._session_cm.session.execute(
                    'SELECT movie_id FROM movie_actors WHERE actor_id = :actor_id ORDER BY movie_id ASC',
                    {'actor_id': actor_id}
            ).fetchall()
            movie_ids = [id[0] for id in movie_ids]

        return movie_ids

    def get_genres(self) -> List[Genre]:
        genres = self._session_cm.session.query(Genre).all()
        return genres

    def add_genre(self, genre: Genre):
        with self._session_cm as scm:
            scm.session.add(genre)
            scm.commit()

    def get_directors(self) -> List[Director]:
        directors = self._session_cm.session.query(Director).all()
        return directors

    def add_director(self, director: Director):
        with self._session_cm as scm:
            scm.session.add(director)
            scm.commit()

    def get_actors(self) -> List[Actor]:
        actors = self._session_cm.session.query(Actor).all()
        return actors

    def add_actor(self, actor: Actor):
        with self._session_cm as scm:
            scm.session.add(actor)
            scm.commit()

    def get_reviews(self) -> List[Review]:
        reviews = self._session_cm.session.query(Review).all()
        return reviews

    def add_review(self, review: Review):
        super().add_review(review)
        with self._session_cm as scm:
            scm.session.add(review)
            scm.commit()

def movie_record_generator(filename: str):
    with open(filename, mode='r', encoding='utf-8-sig') as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        headers = next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:

            movie_data = row
            movie_key = movie_data[0]

            # Strip any leading/trailing white space from data read.
            movie_data = [item.strip() for item in movie_data]
            director = movie_data[4]
            movie_actors = movie_data[5].split(",")
            movie_genres = movie_data[2].split(",")
            number_of_genres = len(movie_genres)

            if director not in directors.keys():
                directors[director] = list()
            directors[director].append(movie_key)

            for actor in movie_actors:
                actor = actor.strip()
                if actor not in actors.keys():
                    actors[actor] = list()
                actors[actor].append(movie_key)

            # Add any new tags; associate the current article with tags.
            for genre in movie_genres:
                if genre not in genres.keys():
                    genres[genre] = list()
                genres[genre].append(movie_key)

            yield movie_data

def get_director_records():
    director_records = list()
    director_key = 0

    for director in director.keys():
        director_key = director_key + 1
        director_records.append((director_key, director))
    return director_records

def get_actor_records():
    actor_records = list()
    actor_key = 0

    for actor in actor.keys():
        actor_key = actor_key + 1
        actor_records.append((actor_key, actor))
    return actor_records

def get_genre_records():
    genre_records = list()
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        genre_records.append((genre_key, genre))
    return genre_records

def movie_directors_generator():
    movie_directors_key = 0
    director_key = 0

    for director in directors.keys():
        director_key = director_key + 1
        for movie_key in directors[director]:
            movie_directors_key = movie_directors_key + 1
            yield movie_directors_key, movie_key, director_key

def movie_actors_generator():
    movie_actors_key = 0
    actor_key = 0

    for actor in actors.keys():
        actor_key = actor_key + 1
        for movie_key in actors[actor]:
            movie_actors_key = movie_actors_key + 1
            yield movie_actors_key, movie_key, actor_key

def movie_genres_generator():
    movie_genres_key = 0
    genre_key = 0

    for genre in genres.keys():
        genre_key = genre_key + 1
        for movie_key in genres[genre]:
            movie_genres_key = movie_genres_key + 1
            yield movie_genres_key, movie_key, genre_key


def generic_generator(filename, post_process=None):
    with open(filename) as infile:
        reader = csv.reader(infile)

        # Read first line of the CSV file.
        next(reader)

        # Read remaining rows from the CSV file.
        for row in reader:
            # Strip any leading/trailing white space from data read.
            row = [item.strip() for item in row]

            if post_process is not None:
                row = post_process(row)
            yield row


def process_user(user_row):
    user_row[2] = generate_password_hash(user_row[2])
    return user_row


def populate(engine: Engine, data_path: str):
    conn = engine.raw_connection()
    cursor = conn.cursor()

    global genres
    global actors
    global directors

    genres = dict()
    actors = dict()
    directors = dict()

    insert_movies = """
        INSERT INTO movies (
        id, title, genre, description, director, actors, year, runtime, rating, votes, revenue, metascore)
        VALUES (?, ?, ?, ?, ?, ?. ?, ?, ?, ?, ?, ?)"""
    cursor.executemany(insert_movies, movie_record_generator(os.path.join(data_path, 'Data1000Movies.csv')))

    insert_directors = """
        INSERT INTO directors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_directors, get_director_records())

    insert_actors = """
        INSERT INTO actors (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_actors, get_actor_records())

    insert_genres = """
        INSERT INTO genres (
        id, name)
        VALUES (?, ?)"""
    cursor.executemany(insert_genres, get_genre_records())

    insert_movie_directors = """
        INSERT INTO movie_directors (
        id, movie_id, director_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_directors, movie_directors_generator())

    insert_movie_actors = """
        INSERT INTO movie_actors (
        id, movie_id, actor_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_actors, movie_actors_generator())

    insert_movie_genres = """
        INSERT INTO movie_genres (
        id, movie_id, genre_id)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_movie_genres, movie_genres_generator())

    insert_users = """
        INSERT INTO users (
        id, username, password)
        VALUES (?, ?, ?)"""
    cursor.executemany(insert_users, generic_generator(os.path.join(data_path, 'users.csv'), process_user))

    insert_reviews = """
        INSERT INTO reviews (
        id, user_id, movie_id, review, timestamp)
        VALUES (?, ?, ?, ?, ?)"""
    cursor.executemany(insert_reviews, generic_generator(os.path.join(data_path, 'reviews.csv')))

    conn.commit()
    conn.close()