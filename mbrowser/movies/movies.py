from datetime import date

from flask import Blueprint
from flask import request, render_template, redirect, url_for, session

from better_profanity import profanity
from flask_wtf import FlaskForm
from wtforms import TextAreaField, HiddenField, SubmitField
from wtforms.validators import DataRequired, Length, ValidationError

import mbrowser.adapters.abstract_repository as repo
import mbrowser.utilities.utilities as utilities
import mbrowser.movies.services as services

from mbrowser.authentication.authentication import login_required


# Configure Blueprint.
movies_blueprint = Blueprint(
    'movies_bp', __name__)

@movies_blueprint.route('/movies_by_title', methods=['GET'])
def movies_by_title():
    letters = ['#','A','B','C','D','E','F','G','H','I','J','K','L','M','N','O','P','Q','R','S','T','U','V','W','X','Y','Z']
    movies_per_page = 20

    # Read query parameters.
    letter = request.args.get('letter')

    cursor = request.args.get('cursor')

    # article_to_show_comments = request.args.get('view_comments_for')

    # if article_to_show_comments is None:
    #     # No view-comments query parameter, so set to a non-existent article id.
    #     article_to_show_comments = -1
    # else:
    #     # Convert article_to_show_comments from string to int.
    #     article_to_show_comments = int(article_to_show_comments)

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for articles that are tagged with tag_name.
    movie_ids = range(1,1001)

    # Retrieve the batch of articles to display on the Web page.
    all_movies = services.get_movies_by_id(movie_ids, repo.repo_instance)
    movies = list()
    for movie in all_movies:
        if movie['title'][0] == letter:
            movies.append(movie)
        elif letter == '#' and not movie['title'][0].isalpha():
            movies.append(movie)
    movies = sorted(movies, key = lambda i: (i['title'], i['release_year']))
    shown_movies = movies[cursor:cursor + movies_per_page]
    # all_movies = services.get_all_movies(repo.repo_instance)
    # movies = all_movies[cursor:cursor + movies_per_page]

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_title', letter = letter)

    if cursor + movies_per_page < len(movies):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movies) / movies_per_page)
        if len(movies) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_title', letter = letter, cursor=last_cursor)

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Browse Movies',
        movies=shown_movies,
        genre_urls=utilities.get_genres_and_urls(),
        movie_urls=utilities.get_movie_urls(),
        current_letter=letter,
        letters=letters,
        letter_urls=utilities.get_letter_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )

@movies_blueprint.route('/movies_by_rank', methods=['GET'])
def movies_by_rank():
    # return redirect(url_for('genres_bp.genres'))
    movies_per_page = 20

    # Read query parameters.
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve article ids for movies that are tagged with tag_name.
    movie_ids = range(1,1001)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding articles, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_rank')

    if cursor + movies_per_page < len(movie_ids):
        # There are further articles, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_rank', cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_rank', cursor=last_cursor)

    # Construct urls for viewing article comments and adding comments.
    # for article in articles:
    #     article['view_comment_url'] = url_for('news_bp.articles_by_tag', tag=tag_name, cursor=cursor, view_comments_for=article['id'])
    #     article['add_comment_url'] = url_for('news_bp.comment_on_article', article=article['id'])

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Movie Rankings',
        movies=movies,
        genre_urls=utilities.get_genres_and_urls(),
        movie_urls=utilities.get_movie_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )

@movies_blueprint.route('/movies_by_genre', methods=['GET'])
def movies_by_genre():
    movies_per_page = 20

    # Read query parameters.
    genre_name = request.args.get('genre')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve movie ids for movies that that have the selected genre.
    movie_ids = services.get_movie_ids_for_genre(genre_name, repo.repo_instance)

    # Retrieve the batch of movies to display on the Web page.
    movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name)

    if cursor + movies_per_page < len(movie_ids):
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(len(movie_ids) / movies_per_page)
        if len(movie_ids) % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movies_by_genre', genre=genre_name, cursor=last_cursor)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title='Showing ' + genre_name + ' Movies',
        movies=movies,
        genre_urls=utilities.get_genres_and_urls(),
        movie_urls=utilities.get_movie_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )

@movies_blueprint.route('/movie_results', methods=['GET'])
def movie_results():
    movies_per_page = 20

    # Read query parameters.
    search = request.args.get('search')
    searchType = request.args.get('searchType')
    cursor = request.args.get('cursor')

    if cursor is None:
        # No cursor query parameter, so initialise cursor to start at the beginning.
        cursor = 0
    else:
        # Convert cursor from string to int.
        cursor = int(cursor)

    # Retrieve the batch of movies to display on the Web page.
    if searchType == 'Movie':
        movies = services.search_movies(search, repo.repo_instance)
        shown_movies = movies[cursor:cursor + movies_per_page]
        numResults = len(movies)
        movies_title="Results for Movie Search: "
    elif searchType == 'Director':
        movie_ids = services.get_movie_ids_for_director(search, repo.repo_instance)
        shown_movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)
        numResults = len(movie_ids)
        movies_title="Movies directed by: "
    else:
        movie_ids = services.get_movie_ids_for_actor(search, repo.repo_instance)
        shown_movies = services.get_movies_by_id(movie_ids[cursor:cursor + movies_per_page], repo.repo_instance)
        numResults = len(movie_ids)
        movies_title="Movies Starring: "

    first_movie_url = None
    last_movie_url = None
    next_movie_url = None
    prev_movie_url = None

    if cursor > 0:
        # There are preceding movies, so generate URLs for the 'previous' and 'first' navigation buttons.
        prev_movie_url = url_for('movies_bp.movie_results', search=search, cursor=cursor - movies_per_page)
        first_movie_url = url_for('movies_bp.movie_results', search=search)

    if cursor + movies_per_page < numResults:
        # There are further movies, so generate URLs for the 'next' and 'last' navigation buttons.
        next_movie_url = url_for('movies_bp.movie_results', search=search, cursor=cursor + movies_per_page)

        last_cursor = movies_per_page * int(numResults / movies_per_page)
        if numResults % movies_per_page == 0:
            last_cursor -= movies_per_page
        last_movie_url = url_for('movies_bp.movie_results', search=search, cursor=last_cursor)

    # Generate the webpage to display the movies.
    return render_template(
        'movies/movies.html',
        title='Movies',
        movies_title=movies_title,
        movies=shown_movies,
        search=search,
        numResults=numResults,
        genre_urls=utilities.get_genres_and_urls(),
        movie_urls=utilities.get_movie_urls(),
        first_movie_url=first_movie_url,
        last_movie_url=last_movie_url,
        prev_movie_url=prev_movie_url,
        next_movie_url=next_movie_url,
    )

@movies_blueprint.route('/movie_page', methods=['GET'])
def movie_page():

    # Read query parameters.
    movie_id = request.args.get('movie_id')

    # Convert movie_id from string to int.
    movie_id = int(movie_id)

    # Retrieve movie
    movie = services.get_movie(movie_id, repo.repo_instance)

    # Construct urls for viewing movie reviews and adding reviews.
    movie['view_review_url'] = url_for('movies_bp.movie_page', movie_id=movie_id)
    movie['add_review_url'] = url_for('movies_bp.review_on_movie', movie_id=movie_id)

    # Generate the webpage to display the articles.
    return render_template(
        'movies/movie_page.html',
        title=movie['title'],
        movie=movie,
        genre_urls=utilities.get_genres_and_urls(),
        director_urls=utilities.get_directors_and_urls(),
        actor_urls=utilities.get_actors_and_urls(),
        # movie_urls=utilities.get_movie_urls(),
    )


@movies_blueprint.route('/review', methods=['GET', 'POST'])
@login_required
def review_on_movie():
    # Obtain the username of the currently logged in user.
    username = session['username']

    # Create form. The form maintains state, e.g. when this method is called with a HTTP GET request and populates
    # the form with a movie id, when subsequently called with a HTTP POST request, the movie id remains in the
    # form.
    form = ReviewForm()

    if form.validate_on_submit():
        # Successful POST, i.e. the review text has passed data validation.
        # Extract the movie id, representing the reviewed movie, from the form.
        movie_id = int(form.movie_id.data)

        # Use the service layer to store the new review.
        services.add_review(movie_id, form.review.data, username, repo.repo_instance)

        # Retrieve the movie in dict form.
        movie = services.get_movie(movie_id, repo.repo_instance)

        # Cause the web browser to display the page of all movies that have the same date as the reviewed movie,
        # and display all reviews, including the new review.
        return redirect(url_for('movies_bp.movie_page', movie_id=movie_id))

    if request.method == 'GET':
        # Request is a HTTP GET to display the form.
        # Extract the movie id, representing the movie to review, from a query parameter of the GET request.
        movie_id = int(request.args.get('movie_id'))

        # Store the movie id in the form.
        form.movie_id.data = movie_id
    else:
        # Request is a HTTP POST where form validation has failed.
        # Extract the movie id of the movie being reviewed from the form.
        movie_id = int(form.movie_id.data)

    # For a GET or an unsuccessful POST, retrieve the movie to review in dict form, and return a Web page that allows
    # the user to enter a review. The generated Web page includes a form object.
    movie = services.get_movie(movie_id, repo.repo_instance)
    return render_template(
        'movies/review_on_movie.html',
        title='Edit movie',
        movie=movie,
        form=form,
        handler_url=url_for('movies_bp.review_on_movie'),
        genre_urls=utilities.get_genres_and_urls(),
    )


class ProfanityFree:
    def __init__(self, message=None):
        if not message:
            message = u'Field must not contain profanity'
        self.message = message

    def __call__(self, form, field):
        if profanity.contains_profanity(field.data):
            raise ValidationError(self.message)


class ReviewForm(FlaskForm):
    review = TextAreaField('Review', [
        DataRequired(),
        Length(min=4, message='Your review is too short'),
        ProfanityFree(message='Your review must not contain profanity')])
    movie_id = HiddenField("Movie id")
    submit = SubmitField('Submit')