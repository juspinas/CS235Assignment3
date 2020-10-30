from datetime import date

import pytest

from mbrowser.authentication.services import AuthenticationException
from mbrowser.movies import services as movies_services
from mbrowser.authentication import services as auth_services
from mbrowser.movies.services import NonExistentMovieException


def test_can_add_user(in_memory_repo):
    new_username = 'jz'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    user_as_dict = auth_services.get_user(new_username, in_memory_repo)
    assert user_as_dict['username'] == new_username

    # Check that password has been encrypted.
    assert user_as_dict['password'].startswith('pbkdf2:sha256:')


def test_cannot_add_user_with_existing_name(in_memory_repo):
    username = 'thorke'
    password = 'abcd1A23'

    with pytest.raises(auth_services.NameNotUniqueException):
        auth_services.add_user(username, password, in_memory_repo)


def test_authentication_with_valid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    try:
        auth_services.authenticate_user(new_username, new_password, in_memory_repo)
    except AuthenticationException:
        assert False


def test_authentication_with_invalid_credentials(in_memory_repo):
    new_username = 'pmccartney'
    new_password = 'abcd1A23'

    auth_services.add_user(new_username, new_password, in_memory_repo)

    with pytest.raises(auth_services.AuthenticationException):
        auth_services.authenticate_user(new_username, '0987654321', in_memory_repo)


def test_can_add_review(in_memory_repo):
    movie_id = 4
    review_text = 'Dayum, that elephant can sing!!'
    username = 'fmercury'

    # Call the service layer to add the review.
    movies_services.add_review(movie_id, review_text, username, in_memory_repo)

    # Retrieve the reviews for the movie from the repository.
    reviews_as_dict = movies_services.get_reviews_for_movie(movie_id, in_memory_repo)

    # Check that the reviews include a review with the new review text.
    assert next(
        (dictionary['review_text'] for dictionary in reviews_as_dict if dictionary['review_text'] == review_text),
        None) is not None


def test_cannot_add_review_for_non_existent_movie(in_memory_repo):
    movie_id = 1001
    review_text = "Pretty decent, but wouldn't watch again."
    username = 'fmercury'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_cannot_add_review_by_unknown_user(in_memory_repo):
    movie_id = 4
    review_text = 'Dayum, that elephant can sing!!'
    username = 'gmichael'

    # Call the service layer to attempt to add the review.
    with pytest.raises(movies_services.UnknownUserException):
        movies_services.add_review(movie_id, review_text, username, in_memory_repo)


def test_can_get_movie(in_memory_repo):
    movie_id = 4

    movie_as_dict = movies_services.get_movie(movie_id, in_memory_repo)

    assert movie_as_dict['movie_id'] == movie_id
    assert movie_as_dict['title'] == "Sing"
    assert movie_as_dict['release_year'] == 2016

    director_full_names = [dictionary['name'] for dictionary in movie_as_dict['directors']]
    assert 'Christophe Lourdelet' in director_full_names
    # print(len(movie_as_dict['actors']))
    actor_full_names = [dictionary['name'] for dictionary in movie_as_dict['actors']]
    assert 'Matthew McConaughey' in actor_full_names
    assert 'Reese Witherspoon' in actor_full_names
    assert 'Seth MacFarlane' in actor_full_names
    assert 'Scarlett Johansson' in actor_full_names

    genre_names = [dictionary['name'] for dictionary in movie_as_dict['genres']]
    assert 'Animation' in genre_names
    assert 'Comedy' in genre_names
    assert 'Family' in genre_names

    assert len(movie_as_dict['reviews']) == 0


def test_cannot_get_movie_with_non_existent_id(in_memory_repo):
    movie_id = 1001

    # Call the service layer to attempt to retrieve the Movie.
    with pytest.raises(movies_services.NonExistentMovieException):
        movies_services.get_movie(movie_id, in_memory_repo)


def test_get_first_movie(in_memory_repo):
    movie_as_dict = movies_services.get_first_movie(in_memory_repo)

    assert movie_as_dict['movie_id'] == 1


def test_get_last_movie(in_memory_repo):
    movie_as_dict = movies_services.get_last_movie(in_memory_repo)

    assert movie_as_dict['movie_id'] == 1000

def test_get_movies_by_release_year(in_memory_repo):
    target_year = 2006

    movies_as_dict = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    # Check that there are 44 movies release in 2006.
    assert len(movies_as_dict) == 44

def test_get_movies_ids_for_director(in_memory_repo):
    target_director = 'Christopher Nolan'

    movie_ids = movies_services.get_movie_ids_for_director(target_director, in_memory_repo)

    assert len(movie_ids) == 5

    assert movie_ids[0] == 37
    assert movie_ids[1] == 55
    assert movie_ids[2] == 65
    assert movie_ids[3] == 81
    assert movie_ids[4] == 125

def test_get_movies_ids_for_actor(in_memory_repo):
    target_actor = 'Scarlett Johansson'

    movie_ids = movies_services.get_movie_ids_for_actor(target_actor, in_memory_repo)

    assert len(movie_ids) == 12
    assert movie_ids[0] == 4
    assert movie_ids[1] == 36
    assert movie_ids[2] == 65
    assert movie_ids[3] == 77
    assert movie_ids[4] == 174
    assert movie_ids[5] == 217
    assert movie_ids[6] == 495
    assert movie_ids[7] == 534
    assert movie_ids[8] == 615
    assert movie_ids[9] == 762
    assert movie_ids[10] == 854
    assert movie_ids[11] == 963

def test_get_movies_ids_for_genre(in_memory_repo):
    target_genre = 'Musical'

    movie_ids = movies_services.get_movie_ids_for_genre(target_genre, in_memory_repo)

    assert len(movie_ids) == 5

    assert movie_ids[0] == 129
    assert movie_ids[1] == 246
    assert movie_ids[2] == 651
    assert movie_ids[3] == 973
    assert movie_ids[4] == 983

def test_get_movies_by_release_year_with_non_existent_release_year(in_memory_repo):
    target_year = 2005

    movies_as_dict = movies_services.get_movies_by_release_year(target_year, in_memory_repo)

    # Check that there are no movies released in 2005.
    assert len(movies_as_dict) == 0


def test_get_movies_by_id(in_memory_repo):
    target_movie_ids = [22, 596, 0, 1001]
    movies_as_dict = movies_services.get_movies_by_id(target_movie_ids, in_memory_repo)

    # Check that 2 movies were returned from the query.
    assert len(movies_as_dict) == 2

    # Check that the movie ids returned were 22 and 596.
    movie_ids = [movie['movie_id'] for movie in movies_as_dict]
    assert set([22, 596]).issubset(movie_ids)

def test_movie_search(in_memory_repo):
    search = "Pirates of the Caribbean"
    movies_as_dict = movies_services.search_movies(search, in_memory_repo)
    assert len(movies_as_dict) == 3
    # print(movies_as_dict)
    assert movies_as_dict[0]['movie_id'] == 46
    assert movies_as_dict[1]['movie_id'] == 76
    assert movies_as_dict[2]['movie_id'] == 79

def test_director_search(in_memory_repo):
    search = "Christopher Nolan"
    directors_as_dict = movies_services.search_directors(search, in_memory_repo)
    assert len(directors_as_dict) == 1
    # print(movies_as_dict)
    assert directors_as_dict[0]['name'] == "Christopher Nolan"

def test_actor_search(in_memory_repo):
    search = "Matthew McConaughey"
    actors_as_dict = movies_services.search_actors(search, in_memory_repo)
    assert len(actors_as_dict) == 1
    # print(movies_as_dict)
    assert actors_as_dict[0]['name'] == "Matthew McConaughey"

def test_get_reviews_for_movie(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(1, in_memory_repo)

    # Check that 2 reviews were returned for movie with id 1.
    assert len(reviews_as_dict) == 2

    # Check that the reviews relate to the article whose id is 1.
    movie_ids = [review['movie_id'] for review in reviews_as_dict]
    movie_ids = set(movie_ids)
    assert 1 in movie_ids and len(movie_ids) == 1


def test_get_reviews_for_non_existent_movie(in_memory_repo):
    with pytest.raises(NonExistentMovieException):
        reviews_as_dict = movies_services.get_reviews_for_movie(1001, in_memory_repo)


def test_get_reviews_for_movie_without_reviews(in_memory_repo):
    reviews_as_dict = movies_services.get_reviews_for_movie(2, in_memory_repo)
    assert len(reviews_as_dict) == 0