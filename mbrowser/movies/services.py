from typing import List, Iterable

from mbrowser.adapters.abstract_repository import AbstractRepository
from mbrowser.domain.model import Director, Genre, Actor, Movie, User, Review, make_review


class NonExistentMovieException(Exception):
    pass


class UnknownUserException(Exception):
    pass


def add_review(movie_id: int, review_text: str, username: str, repo: AbstractRepository):
    # Check that the movie exists.
    movie = repo.get_movie(movie_id)
    if movie is None:
        raise NonExistentMovieException

    user = repo.get_user(username)
    if user is None:
        raise UnknownUserException

    # Create review.
    review = make_review(review_text, user, movie)

    # Update the repository.
    repo.add_review(review)


def get_movie(movie_id: int, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return movie_to_dict(movie)

# def get_all_movies(repo: AbstractRepository):
#     return repo.get_all_movies()


def get_first_movie(repo: AbstractRepository):

    movie = repo.get_first_movie()

    return movie_to_dict(movie)


def get_last_movie(repo: AbstractRepository):

    movie = repo.get_last_movie()
    return movie_to_dict(movie)


def get_movies_by_release_year(year, repo: AbstractRepository):
    # Returns articles for the target date (empty if no matches), the date of the previous article (might be null), the date of the next article (might be null)

    movies = repo.get_movies_by_release_year(target_year=year)

    movies_dto = list()
    # prev_date = next_date = None

    if len(movies) > 0:

        # Convert Movies to dictionary form.
        movies_dto = movies_to_dict(movies)

    return movies_dto

def get_movie_ids_for_director(director_full_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_director(director_full_name)

    return movie_ids

def get_movie_ids_for_actor(actor_full_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_actor(actor_full_name)

    return movie_ids

def get_movie_ids_for_genre(genre_name, repo: AbstractRepository):
    movie_ids = repo.get_movie_ids_for_genre(genre_name)

    return movie_ids


def get_movies_by_id(id_list, repo: AbstractRepository):
    movies = repo.get_movies_by_id(id_list)

    # Convert movies to dictionary form.
    movies_as_dict = movies_to_dict(movies)

    return movies_as_dict


def get_reviews_for_movie(movie_id, repo: AbstractRepository):
    movie = repo.get_movie(movie_id)

    if movie is None:
        raise NonExistentMovieException

    return reviews_to_dict(movie.reviews)

def search_movies(search: str, repo: AbstractRepository):
    movies = repo.get_movies()
    movies_as_dict = []
    for movie in movies:
        if search.lower() in movie.title.lower():
            movies_as_dict += [movie_to_dict(movie)]
    return movies_as_dict

def search_directors(search: str, repo: AbstractRepository):
    directors = repo.get_directors()
    directors_as_dict = []
    for director in directors:
        if search.lower() in director.director_full_name.lower():
            directors_as_dict += [director_to_dict(director)]
    return directors_as_dict

def search_actors(search: str, repo: AbstractRepository):
    actors = repo.get_actors()
    actors_as_dict = []
    for actor in actors:
        if search.lower() in actor.actor_full_name.lower():
            actors_as_dict += [actor_to_dict(actor)]
    return actors_as_dict

# ============================================
# Functions to convert model entities to dicts
# ============================================

def movie_to_dict(movie: Movie):
    movie_dict = {
        'movie_id': movie.movie_id,
        'title': movie.title,
        'release_year': movie.release_year,
        'description' : movie.description,
        'directors' : directors_to_dict(movie.directors),
        'actors' : actors_to_dict(movie.actors),
        'genres' : genres_to_dict(movie.genres),
        'reviews' : reviews_to_dict(movie.reviews),
        'runtime_minutes' : movie.runtime_minutes,
    }
    return movie_dict


def movies_to_dict(movies: Iterable[Movie]):
    return [movie_to_dict(movie) for movie in movies]


def review_to_dict(review: Review):
    review_dict = {
        'username': review.user.username,
        'movie_id': review.movie.movie_id,
        'review_text': review.review,
        'timestamp': review.timestamp
    }
    return review_dict


def reviews_to_dict(reviews: Iterable[Review]):
    return [review_to_dict(review) for review in reviews]


def director_to_dict(director: Director):
    director_dict = {
        'name': director.director_full_name,
        'director_movies': [movie.movie_id for movie in director.director_movies]
    }
    return director_dict

def directors_to_dict(directors: Iterable[Director]):
    return [director_to_dict(director) for director in directors]

def actor_to_dict(actor: Actor):
    actor_dict = {
        'name': actor.actor_full_name,
        'actor_movies': [movie.movie_id for movie in actor.actor_movies]
    }
    return actor_dict

def actors_to_dict(actors: Iterable[Actor]):
    return [actor_to_dict(actor) for actor in actors]

def genre_to_dict(genre: Genre):
    genre_dict = {
        'name': genre.genre_name,
        'genre_movies': [movie.movie_id for movie in genre.genre_movies]
    }
    return genre_dict


def genres_to_dict(genres: Iterable[Genre]):
    return [genre_to_dict(genre) for genre in genres]


# ============================================
# Functions to convert dicts to model entities
# ============================================

# def dict_to_movie(dict):
#     movie = Movie(dict.title, dict.release_year, dict.id, dict.directors, dict.actors, dict.genres)
#     # Note there's no comments or tags.
#     return article