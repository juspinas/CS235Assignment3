from flask import Blueprint, request, render_template, redirect, url_for, session

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.services as services


# Configure Blueprint.
utilities_blueprint = Blueprint(
    'utilities_bp', __name__)


def get_directors_and_urls():
    director_full_names = services.get_director_full_names(repo.repo_instance)
    director_urls = dict()
    for director_full_name in director_full_names:
        director_urls[director_full_name] = url_for('movies_bp.movie_results', searchType="Director", search=director_full_name)

    return director_urls

def get_actors_and_urls():
    actor_full_names = services.get_actor_full_names(repo.repo_instance)
    actor_urls = dict()
    for actor_full_name in actor_full_names:
        actor_urls[actor_full_name] = url_for('movies_bp.movie_results', searchType="Actor", search=actor_full_name)

    return actor_urls

def get_genres_and_urls():
    genre_names = services.get_genre_names(repo.repo_instance)
    genre_urls = dict()
    for genre_name in genre_names:
        genre_urls[genre_name] = url_for('movies_bp.movies_by_genre', genre=genre_name)

    return genre_urls

def get_movie_urls():
    movie_ids = range(1,1001)
    movie_urls = dict()
    for movie_id in movie_ids:
        movie_urls[movie_id] = url_for('movies_bp.movie_page', movie_id= str(movie_id))

    return movie_urls

def get_letter_urls():
    letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    letter_urls = dict()
    for letter in letters:
        letter_urls[letter] = url_for('movies_bp.movies_by_title', letter=letter)

    return letter_urls


def get_selected_movies(quantity=3):
    movies = services.get_random_movies(quantity, repo.repo_instance)

    # for movie in movies:
    #     movie['hyperlink'] = url_for('movies_bp.movies_by_rank', date=article['date'].isoformat())
    return movies