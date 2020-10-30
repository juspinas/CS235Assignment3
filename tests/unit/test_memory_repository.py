from datetime import date, datetime
from typing import List

import pytest

from mbrowser.domain.model import Director, Genre, Actor, Movie, User, Review, make_genre_association, make_review
from mbrowser.adapters.abstract_repository import RepositoryException


def test_repository_can_add_a_user(in_memory_repo):
    user = User('Dave', '123456789')
    in_memory_repo.add_user(user)

    assert in_memory_repo.get_user('Dave') is user


def test_repository_can_retrieve_a_user(in_memory_repo):
    user = in_memory_repo.get_user('fmercury')
    assert user == User('fmercury', 'mvNNbc1eLA$i')


def test_repository_does_not_retrieve_a_non_existent_user(in_memory_repo):
    user = in_memory_repo.get_user('prince')
    assert user is None


def test_repository_can_retrieve_movie_count(in_memory_repo):
    number_of_movies = in_memory_repo.get_number_of_movies()

    # Check that the query returned 1000 Movies.
    assert number_of_movies == 1000


def test_repository_can_add_movie(in_memory_repo):
    movie = Movie("Sing", "2016", 1001,'')
    in_memory_repo.add_movie(movie)
    assert in_memory_repo.get_movie(1001) is movie


def test_repository_can_retrieve_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(4)

    # Check that the Movie has the expected title.
    assert movie.title == 'Sing'
    assert movie.release_year == 2016
    assert movie.movie_id == 4
    assert movie.has_director(Director('Christophe Lourdelet'))

    # Check that the Movie has expected actors.
    assert movie.has_actor(Actor('Matthew McConaughey'))
    assert movie.has_actor(Actor('Reese Witherspoon'))
    assert movie.has_actor(Actor('Seth MacFarlane'))
    assert movie.has_actor(Actor('Scarlett Johansson'))

    # Check that the Movie has expected genres.
    assert movie.has_genre(Genre('Animation'))
    assert movie.has_genre(Genre('Comedy'))
    assert movie.has_genre(Genre('Family'))

def test_repository_does_not_retrieve_a_non_existent_movie(in_memory_repo):
    movie = in_memory_repo.get_movie(1001)
    assert movie is None


def test_repository_can_retrieve_movies_by_release_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_release_year(2006)

    # Check that the query returned 44 Movies.
    assert len(movies) == 44


def test_repository_does_not_retrieve_a_movie_when_there_are_no_movies_for_a_given_release_year(in_memory_repo):
    movies = in_memory_repo.get_movies_by_release_year(2005)
    assert len(movies) == 0

def test_repository_can_retrieve_directors(in_memory_repo):
    directors: List[Director] = in_memory_repo.get_directors()
    assert len(directors) == 644

    director1 = [director for director in directors if director.director_full_name == 'Anthony Russo'][0]
    director2 = [director for director in directors if director.director_full_name == 'Christopher Nolan'][0]

    assert director1.number_of_director_movies == 2
    assert director2.number_of_director_movies == 5

def test_repository_can_retrieve_actors(in_memory_repo):
    actors: List[Actor] = in_memory_repo.get_actors()
    assert len(actors) == 1985

    actor1 = [actor for actor in actors if actor.actor_full_name == 'Will Smith'][0]
    actor2 = [actor for actor in actors if actor.actor_full_name == 'Scarlett Johansson'][0]

    assert actor1.number_of_actor_movies == 10
    assert actor2.number_of_actor_movies == 12

def test_repository_can_retrieve_genres(in_memory_repo):
    genres: List[Genre] = in_memory_repo.get_genres()
    assert len(genres) == 20

    genre1 = [genre for genre in genres if genre.genre_name == 'Sci-Fi'][0]
    genre2 = [genre for genre in genres if genre.genre_name == 'Sport'][0]

    assert genre1.number_of_genre_movies == 120
    assert genre2.number_of_genre_movies == 18



def test_repository_can_get_first_movie(in_memory_repo):
    movie = in_memory_repo.get_first_movie()
    assert movie.title == 'Guardians of the Galaxy'


def test_repository_can_get_last_movie(in_memory_repo):
    movie = in_memory_repo.get_last_movie()
    assert movie.title == 'Nine Lives'



def test_repository_can_get_movies_by_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([4, 92, 487])

    assert len(movies) == 3
    assert movies[0].title == 'Sing'
    assert movies[1].title == "Warcraft"
    assert movies[2].title == 'Hairspray'


def test_repository_does_not_retrieve_movie_for_non_existent_id(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([4, 1001])

    assert len(movies) == 1
    assert movies[0].title == 'Sing'


def test_repository_returns_an_empty_list_for_non_existent_ids(in_memory_repo):
    movies = in_memory_repo.get_movies_by_id([0, 1001])

    assert len(movies) == 0


def test_repository_returns_movie_ids_for_existing_genre(in_memory_repo):
    genre_ids = in_memory_repo.get_movie_ids_for_genre('Sport')

    assert genre_ids == [195,311,338,368,378,382,494,549,575,585,587,594,597,831,850,897,936,975]


def test_repository_returns_an_empty_list_for_non_existent_genre(in_memory_repo):
    genre_ids = in_memory_repo.get_movie_ids_for_genre('Anime')

    assert len(genre_ids) == 0

def test_repository_can_add_a_director(in_memory_repo):
    director = Director('Tori Kelly')
    in_memory_repo.add_director(director)

    assert director in in_memory_repo.get_directors()

def test_repository_can_add_an_actor(in_memory_repo):
    actor = Actor('Tori Kelly')
    in_memory_repo.add_actor(actor)

    assert actor in in_memory_repo.get_actors()

def test_repository_can_add_a_genre(in_memory_repo):
    genre = Genre('Anime')
    in_memory_repo.add_genre(genre)

    assert genre in in_memory_repo.get_genres()


def test_repository_can_add_a_review(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(4)
    review = make_review("That elephant can SING!!", user, movie)

    in_memory_repo.add_review(review)

    assert review in in_memory_repo.get_reviews()


def test_repository_does_not_add_a_review_without_a_user(in_memory_repo):
    movie = in_memory_repo.get_movie(4)
    review = Review(None, movie, "That elephant can SING!!", datetime.today())

    with pytest.raises(RepositoryException):
        in_memory_repo.add_review(review)


def test_repository_does_not_add_a_review_without_a_movie_properly_attached(in_memory_repo):
    user = in_memory_repo.get_user('thorke')
    movie = in_memory_repo.get_movie(4)
    review = Review(None, movie, "That elephant can SING!!", datetime.today())

    user.add_review(review)

    with pytest.raises(RepositoryException):
        # Exception expected because the Movie doesn't refer to the Review.
        in_memory_repo.add_review(review)


def test_repository_can_retrieve_reviews(in_memory_repo):
    assert len(in_memory_repo.get_reviews()) == 2