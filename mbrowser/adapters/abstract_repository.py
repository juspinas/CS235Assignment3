import abc
from typing import List
from datetime import date

from mbrowser.domain.model import Director, Genre, Actor, Movie, User, Review

repo_instance = None

class RepositoryException(Exception):

    def __init__(self, message=None):
        pass


class AbstractRepository(abc.ABC):

    @abc.abstractmethod
    def add_user(self, user: User):
        """" Adds a User to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_user(self, username) -> User:
        """ Returns the User named username from the repository.
        If there is no User with the given username, this method returns None.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_movie(self, movie: Movie):
        """ Adds a Movie to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie(self, id: int) -> Movie:
        """ Returns Movie with id from the repository.
        If there is no Movie with the given id, this method returns None.
        """
        raise NotImplementedError

    def get_movies(self) -> List[Movie]:
        """ Returns the full list of Movies.
        If there are no Movies, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_release_year(self, target_year: int) -> List[Movie]:
        """ Returns a list of Movies that were released on target_year.
        If there are no Movies released on the given year, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_number_of_movies(self):
        """ Returns the number of Movies in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_first_movie(self) -> Movie:
        """ Returns the first Movie, ordered by release_year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_last_movie(self) -> Movie:
        """ Returns the last Movie, ordered by release_year, from the repository.
        Returns None if the repository is empty.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movies_by_id(self, id_list):
        """ Returns a list of Movies, whose ids match those in id_list, from the repository.
        If there are no matches, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_director(self, director_full_name: str):
        """ Returns a list of ids representing Movies that are tagged by director_full_name.
        If there are no movies that are tagged by director_full_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_actor(self, actor_full_name: str):
        """ Returns a list of ids representing Movies that are tagged by actor_full_name.
        If there are no movies that are tagged by actor_full_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def get_movie_ids_for_genre(self, genre_name: str):
        """ Returns a list of ids representing Movies that are tagged by genre_name.
        If there are no movies that are tagged by genre_name, this method returns an empty list.
        """
        raise NotImplementedError

    @abc.abstractmethod
    def add_director(self, director: Director):
        """ Adds a Director to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_directors(self) -> List[Director]:
        """ Returns the Directors stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_actor(self, actor: Actor):
        """ Adds a Actor to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_actors(self) -> List[Actor]:
        """ Returns the Actors stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_genre(self, genre: Genre):
        """ Adds a Genre to the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def get_genres(self) -> List[Genre]:
        """ Returns the Genres stored in the repository. """
        raise NotImplementedError

    @abc.abstractmethod
    def add_review(self, review: Review):
        """ Adds a Comment to the repository.
        If the Comment doesn't have bidirectional links with an Article and a User, this method raises a
        RepositoryException and doesn't update the repository.
        """
        if review.user is None or review not in review.user.reviews:
            raise RepositoryException('Review not correctly attached to a User')
        if review.movie is None or review not in review.movie.reviews:
            raise RepositoryException('Review not correctly attached to a Movie')

    @abc.abstractmethod
    def get_reviews(self):
        """ Returns the Reviews stored in the repository. """
        raise NotImplementedError