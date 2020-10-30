from flask import Blueprint, render_template

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.utilities.services as services


genres_blueprint = Blueprint(
    'genres_bp', __name__)


@genres_blueprint.route('/genres', methods=['GET'])
def genres():
    return render_template(
        'genres/genres.html',
        # selected_articles=utilities.get_selected_articles(),
        all_genres=services.get_genre_names(repo.repo_instance),
        genre_urls=utilities.get_genres_and_urls(),
    )