from flask import Blueprint, render_template
from flask import request, render_template, redirect, url_for, session

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.movies.services as services


actors_blueprint = Blueprint(
    'actors_bp', __name__)


@actors_blueprint.route('/actors', methods=['GET'])
def actors():
    actors_per_page = 30

    search = request.args.get('search')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    actors = services.search_actors(search, repo.repo_instance)
    shown_actors = actors[cursor:cursor + actors_per_page]

    numResults = len(actors)

    first_actor_url = None
    last_actor_url = None
    next_actor_url = None
    prev_actor_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_actor_url = url_for('actors_bp.actors', search=search, cursor=cursor - actors_per_page)
        first_actor_url = url_for('actors_bp.actors', search=search)

    if cursor + actors_per_page < len(actors):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_actor_url = url_for('actors_bp.actors', search=search, cursor=cursor + actors_per_page)

        last_cursor = actors_per_page * int(len(actors) / actors_per_page)
        if len(actors) % actors_per_page == 0:
            last_cursor -= actors_per_page
        last_actor_url = url_for('actors_bp.actors', search=search, cursor=last_cursor)


    return render_template(
        'actors/actors.html',
        search=search,
        actors=shown_actors,
        numResults=numResults,
        # all_genres=services.get_genre_names(repo.repo_instance),
        actor_urls=utilities.get_actors_and_urls(),
        first_actor_url=first_actor_url,
        last_actor_url=last_actor_url,
        prev_actor_url=prev_actor_url,
        next_actor_url=next_actor_url,
    )