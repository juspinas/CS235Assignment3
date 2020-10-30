# python -m pytest

from datetime import date

from mbrowser.domain.model import Director, Genre, Actor, Movie, User

import pytest

@pytest.fixture()
def director():
    return Director("Peter Jackson")

@pytest.fixture()
def empty_director():
    return Director("")

@pytest.fixture()
def genre():
    return Genre("Horror")

@pytest.fixture()
def empty_genre():
    return Genre("")

@pytest.fixture()
def actor():
    return Actor("Angelina Jolie")

@pytest.fixture()
def empty_actor():
    return Actor("")

@pytest.fixture()
def movie():
    return Movie("Moana", 2016, 1, '')

@pytest.fixture()
def user():
    return User('dbowie', '1234567890')

def test_director_construction(director):
    assert director.director_full_name == 'Peter Jackson'

def test_empty_director_construction(empty_director):
    assert empty_director.director_full_name == None

def test_genre_construction(genre):
    assert genre.genre_name == 'Horror'

def test_empty_genre_construction(empty_genre):
    assert empty_genre.genre_name == None

def test_actor_construction(actor):
    assert actor.actor_full_name == 'Angelina Jolie'

def test_empty_actore_construction(empty_actor):
    assert empty_actor.actor_full_name == None

def test_movie_construction(movie):
    assert movie.title == 'Moana'
    assert movie.release_year == 2016
    assert movie.movie_id == 1
    assert movie.description == ""
    assert movie.number_of_reviews == 0
    assert movie.runtime_minutes == 0

def test_user_construction(user):
    assert user.username == 'dbowie'
    assert user.password == '1234567890'
    assert repr(user) == '<User dbowie>'

    for review in user.reviews:
        # User should have an empty list of Comments after construction.
        assert False
