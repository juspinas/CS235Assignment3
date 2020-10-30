from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

# from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.movies.services as services

home_blueprint = Blueprint(
    'home_bp', __name__)

# @@@@@@@@@@@@@@@@@@@@@@@@@ NEED TTO FIGURE OUT HOE TO CHECK SEARCH TYPE
@home_blueprint.route('/', methods=['GET'])
def home():

    form = SearchForm()
    searchType = form.searchType.data
    search = form.search.data
    handler_url = url_for('search_bp.search', searchType=searchType, search=search)
    # handler_url = url_for('movies_bp.movies_by_rank')
    
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the search, representing the search text, from the form.
        # if searchType == 'Movie+Title':
        # Cause the web browser to display the page of all movies that contain the search text.
    # if searchType == 'Movie':
    #     handler_url = url_for('movies_bp.movie_results')


    return render_template(
        'home/home.html',
        form=form,
        handler_url= handler_url,
    )

class SearchForm(FlaskForm):
    searchType = SelectField('Search Type', choices=[('Movie', 'Movie'), ('Director', 'Director'), ('Actor', 'Actor')])
    search = StringField('Search', [DataRequired()])
    submit = SubmitField('')