import os

from flask import Flask

import mbrowser.adapters.abstract_repository as repo
from mbrowser.adapters.memory_repository import MemoryRepository, populate

def create_app(test_config=None):
    app = Flask(__name__)
    # ...
    app.config.from_object('config.Config')
    data_path = os.path.join('mbrowser', 'adapters', 'data')

    if test_config is not None:
        # Load test configuration, and override any configuration settings.
        app.config.from_mapping(test_config)
        data_path = app.config['TEST_DATA_PATH']

    # Create the MemoryRepository implementation for a memory-based repository.
    repo.repo_instance = MemoryRepository()
    populate(data_path, repo.repo_instance)

    with app.app_context():
        # Register blueprints.
        from .home import home
        app.register_blueprint(home.home_blueprint)

        from .search import search
        app.register_blueprint(search.search_blueprint)

        from .movies import movies
        app.register_blueprint(movies.movies_blueprint)

        from .genres import genres
        app.register_blueprint(genres.genres_blueprint)

        from .directors import directors
        app.register_blueprint(directors.directors_blueprint)

        from .actors import actors
        app.register_blueprint(actors.actors_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        from .utilities import utilities
        app.register_blueprint(utilities.utilities_blueprint)

    # @app.route('/')
    # def index():
    #     return 'Index page'

    # @app.route('/hello')
    # def hello():
    #     return 'Hello World!'
    return app