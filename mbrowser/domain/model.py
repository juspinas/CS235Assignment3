from datetime import date, datetime
from typing import List, Iterable

class User:
    def __init__(
            self, username: str, password: str
    ):
        self._username: str = username
        self._password: str = password
        self._reviews: List[Review] = list()

    @property
    def username(self) -> str:
        return self._username

    @property
    def password(self) -> str:
        return self._password

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    def add_review(self, review: 'Review'):
        self._reviews.append(review)

    def __repr__(self) -> str:
        return f'<User {self._username}>'

    def __eq__(self, other) -> bool:
        if not isinstance(other, User):
            return False
        return other._username == self._username

class Review:
    def __init__(
            self, user: User, movie: 'Movie', review: str, timestamp: datetime
    ):
        self._user: User = user
        self._movie: Movie = movie
        self._review: Review = review
        self._timestamp: datetime = timestamp

    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def review(self) -> str:
        return self._review

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other._user == self._user and other._movie == self._movie and other._review == self._review and other._timestamp == self._timestamp

class ModelException(Exception):
    pass

# ________________________________________________________________________________________________________________________
class Movie:
    def __init__(self, title: str, release_year: int, movie_id: int, description: str):
        if title == None or type(title) is not str:
            self.__title = None
        else:
            self.__title = title.strip()
        if type(release_year) is str or type(release_year) is int:
            try:
                release_year = int(release_year)
                if release_year < 1900:
                    self.__release_year = None
                else:
                    self.__release_year = int(release_year)
            except ValueError:
                release_year = None

        if type(movie_id) is not int:
            self.__movie_id = None
        else:
            self.__movie_id = movie_id

        if description == None or type(description) is not str:
            self.__description = ""
        else:
            self.__description = description.strip()
        self.__directors: List[Director] = list()
        self.__actors: List[Actor] = list()
        self.__genres: List[Genre] = list()
        self._reviews: List[Review] = list()
        self.__runtime_minutes = 0
    
    @property
    def title(self) -> str:
        return self.__title
    @title.setter
    def title(self, title):
        self.__title = title

    @property
    def release_year(self) -> int:
        return self.__release_year

    @property
    def movie_id(self) -> int:
        return self.__movie_id

    @property
    def description(self) -> str:
        return self.__description
    @description.setter
    def description(self, description):
        if description == "" or type(description) is not str:
            self.__description = None
        else:
            self.__description = description.strip()
     
    @property
    def directors(self) -> Iterable['Director']:
        return iter(self.__directors)

    def has_director(self, director: 'Director'):
        return director in self.__directors

    @property
    def actors(self) -> Iterable['Actor']:
        return iter(self.__actors)

    def has_actor(self, actor: 'Actor'):
        return actor in self.__actors

    @property
    def genres(self) -> Iterable['Genre']:
        return iter(self.__genres)

    def has_genre(self, genre: 'Genre'):
        return genre in self.__genres

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    @property
    def number_of_reviews(self) -> int:
        return len(self._reviews)

    @property
    def runtime_minutes(self) -> int:
        return self.__runtime_minutes
    @runtime_minutes.setter
    def runtime_minutes(self, runtime_minutes):
        if type(runtime_minutes) is not int:
            raise ValueError
        else:
            if runtime_minutes > 0:
                self.__runtime_minutes = runtime_minutes
            else:
                raise ValueError

    def __repr__(self):
        return f"<Movie {self.__title}, {self.__release_year}>"

    def __eq__(self, other):
        if self.__title == other.title and self.__release_year == other.release_year:
            return True
        else:
            return False

    def __lt__(self, other):
        # if self.title == other.title:
        #     return self.release_year < other.release_year
        # return self.title < other.title
        return self.movie_id < other.movie_id
    
    def __hash__(self):
        combinedStr = self.__title + str(self.__release_year)
        return hash(combinedStr)

    def add_director(self,director):
        if type(director) is Director and director not in self.__directors:
            self.__directors.append(director)

    def remove_director(self,director):
        if type(director) is Director:
            if director in self.__directors:
                self.__directors.remove(director)
    
    def add_actor(self,actor):
        if type(actor) is Actor and actor not in self.__actors:
            self.__actors.append(actor)
    
    def remove_actor(self,actor):
        if type(actor) is Actor:
            if actor in self.__actors:
                self.__actors.remove(actor)

    def add_genre(self,genre):
        if type(genre) is Genre and genre not in self.__genres:
            self.__genres.append(genre)

    def remove_genre(self,genre):
        if type(genre) is Genre:
            if genre in self.__genres:
                self.__genres.remove(genre)

    def add_review(self, review: Review):
        self._reviews.append(review)

class Director:
    def __init__(self, director_full_name: str):
        if director_full_name == "" or type(director_full_name) is not str:
            self.__director_full_name = None
        else:
            self.__director_full_name = director_full_name.strip()
        self.__director_movies: List[Movie] = list()
    
    @property
    def director_full_name(self) -> str:
        return self.__director_full_name

    @property
    def director_movies(self) -> Iterable[Movie]:
        return iter(self.__director_movies)
    
    @property
    def number_of_director_movies(self) -> int:
        return len(self.__director_movies)
    
    def is_director_of(self, movie: Movie) -> bool:
        return movie in self.__director_movies
    
    def add_movie(self, movie: Movie):
        self.__director_movies.append(movie)

    def __repr__(self):
        return f"<Director {self.__director_full_name}>"

    def __eq__(self, other):
        if self.__director_full_name == other.director_full_name:
            return True
        else:
            return False

    def __lt__(self, other):
        unsortedOrder = [self.__director_full_name, other.director_full_name]
        sortedOrder = [self.__director_full_name, other.director_full_name]
        sortedOrder.sort()
        if (unsortedOrder == sortedOrder):
            return True
        else:
            return False

    def __hash__(self):
        return hash(self.__director_full_name)

class Actor:
    def __init__(self, actor_full_name: str):
        if actor_full_name == "" or type(actor_full_name) is not str:
            self.__actor_full_name = None
        else:
            self.__actor_full_name = actor_full_name.strip()
        self.__actor_movies: List[Movie] = list()
        self.__colleagues = set()
    
    @property
    def actor_full_name(self) -> str:
        return self.__actor_full_name

    @property
    def actor_movies(self) -> Iterable[Movie]:
        return iter(self.__actor_movies)
    
    @property
    def number_of_actor_movies(self) -> int:
        return len(self.__actor_movies)
    
    def is_actor_in(self, movie: Movie) -> bool:
        return movie in self.__actor_movies
    
    def add_movie(self, movie: Movie):
        self.__actor_movies.append(movie)

    def __repr__(self):
        return f"<Actor {self.__actor_full_name}>"

    # def __eq__(self, other):
    #     if not isinstance(other, self.__class__):
    #         return False
    #     return other.actor_full_name == self.__actor_full_name

    def __eq__(self, other):
        if self.__actor_full_name == other.actor_full_name:
            return True
        else:
            return False

    def __lt__(self, other):
        return self.__actor_full_name < other.actor_full_name

    def __hash__(self):
        return hash(self.__actor_full_name)

    def add_actor_colleague(self, colleague):
        if isinstance(colleague, self.__class__):
            self.__colleagues.add(colleague)
    
    def check_if_this_actor_worked_with(self, colleague):
        return colleague in self.__colleagues

class Genre:
    def __init__(self, genre_name: str):
        self.__genre_name = genre_name
        if genre_name == "" or type(genre_name) is not str:
            self.__genre_name = None
        else:
            self.__genre_name = genre_name.strip()
        self.__genre_movies: List[Movie] = list()
            
    @property
    def genre_name(self) -> str:
        return self.__genre_name

    @property
    def genre_movies(self) -> Iterable[Movie]:
        return iter(self.__genre_movies)

    @property
    def number_of_genre_movies(self) -> int:
        return len(self.__genre_movies)

    def is_genre_of(self, movie: Movie) -> bool:
        return movie in self.__genre_movies

    def add_movie(self, movie: Movie):
        self.__genre_movies.append(movie)

    def __repr__(self):
        return f"<Genre {self.__genre_name}>"

    def __eq__(self, other):
        if self.__genre_name == other.genre_name:
            return True
        else:
            return False


    def __lt__(self, other):
        unsortedOrder = [self.__genre_name, other.genre_name]
        sortedOrder = [self.__genre_name, other.genre_name]
        sortedOrder.sort()
        if (unsortedOrder == sortedOrder):
            return True
        else:
            return False


    def __hash__(self):
        return hash(self.__genre_name)

class Review:
    def __init__(self, user: User, movie: Movie, review: str, timestamp: datetime):
        self._user: User = user
        self._movie: Movie = movie
        self._review: Review = review
        self._timestamp: datetime = timestamp
            
    @property
    def user(self) -> User:
        return self._user

    @property
    def movie(self) -> 'Movie':
        return self._movie

    @property
    def review(self) -> str:
        return self._review

    @property
    def timestamp(self) -> datetime:
        return self._timestamp

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        return other._user == self._user and other._movie == self._movie and other._review == self._review and other._timestamp == self._timestamp

def make_review(review_text: str, user: User, movie: Movie, timestamp: datetime = datetime.today()):
    review = Review(user, movie, review_text, timestamp)
    user.add_review(review)
    movie.add_review(review)

    return review

def make_director_association(movie: Movie, director: Director):
    if director.is_director_of(movie):
        raise ModelException(f'Director {director.director_full_name} already applied to Movie "{movie.title}"')
    else:
        movie.add_director(director)
        director.add_movie(movie)

def make_actor_association(movie: Movie, actor: Actor):
    if actor.is_actor_in(movie):
        raise ModelException(f'Actor {actor.actor_full_name} already applied to Movie "{movie.title}"')
    else:
        movie.add_actor(actor)
        actor.add_movie(movie)

def make_genre_association(movie: Movie, genre: Genre):
    if genre.is_genre_of(movie):
        raise ModelException(f'Genre {genre.genre_name} already applied to Movie "{movie.title}"')
    else:
        movie.add_genre(genre)
        genre.add_movie(movie)