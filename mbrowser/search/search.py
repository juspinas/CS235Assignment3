from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.utilities.services as services


search_blueprint = Blueprint(
    'search_bp', __name__)


@search_blueprint.route('/search', methods=['GET'])
def search():

    searchType = request.args.get('searchType')
    search = request.args.get('search')
    print("HEY IM Here")
    if searchType == 'Movie':
        return redirect(url_for('movies_bp.movie_results', searchType=searchType, search=search))
    elif searchType == 'Director':
        return redirect(url_for('directors_bp.directors', search=search))
    else:
        return redirect(url_for('actors_bp.actors', search=search))


    return render_template(
        'search/search.html',
    )