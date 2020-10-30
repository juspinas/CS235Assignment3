from flask import Blueprint, render_template
from flask import request, render_template, redirect, url_for, session

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.movies.services as services


directors_blueprint = Blueprint(
    'directors_bp', __name__)


@directors_blueprint.route('/directors', methods=['GET'])
def directors():
    directors_per_page = 30

    search = request.args.get('search')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    directors = services.search_directors(search, repo.repo_instance)
    shown_directors = directors[cursor:cursor + directors_per_page]

    numResults = len(directors)

    first_director_url = None
    last_director_url = None
    next_director_url = None
    prev_director_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_director_url = url_for('directors_bp.directors', search=search, cursor=cursor - directors_per_page)
        first_director_url = url_for('directors_bp.directors', search=search)

    if cursor + directors_per_page < len(directors):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_director_url = url_for('directors_bp.directors', search=search, cursor=cursor + directors_per_page)

        last_cursor = directors_per_page * int(len(directors) / directors_per_page)
        if len(directors) % directors_per_page == 0:
            last_cursor -= directors_per_page
        last_director_url = url_for('directors_bp.directors', search=search, cursor=last_cursor)


    return render_template(
        'directors/directors.html',
        search=search,
        directors=shown_directors,
        numResults=numResults,
        # all_genres=services.get_genre_names(repo.repo_instance),
        director_urls=utilities.get_directors_and_urls(),
        first_director_url=first_director_url,
        last_director_url=last_director_url,
        prev_director_url=prev_director_url,
        next_director_url=next_director_url,
    )