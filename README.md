# 235-movie-browser
##

A Web application that demonstrates use of Python's Flask framework. The application makes use of libraries such as the Jinja templating library. Architectural design patterns and principles including Repository, Dependency Inversion and Single Responsibility have been used to design the application. The application uses Flask Blueprints to maintain a separation of concerns between application functions. Testing includes unit and end-to-end testing using the pytest tool. 

## Installation

**Installation via requirements.txt**

```shell
$ cd movie-browser
$ py -3 -m venv venv
$ venv\Scripts\activate
$ pip install -r requirements.txt
```

**Running the application**

From the *movie-browser* directory, and within the activated virtual environment (see *venv\Scripts\activate* above):

````shell
$ flask run
```` 

## Configuration

The *COMPSCI-235/.env* file contains variable settings. They are set with appropriate values.

* `FLASK_APP`: Entry point of the application (should always be `wsgi.py`).
* `FLASK_ENV`: The environment in which to run the application (either `development` or `production`).
* `SECRET_KEY`: Secret key used to encrypt session data.
* `TESTING`: Set to False for running the application. Overridden and set to True automatically when testing the application.
* `WTF_CSRF_SECRET_KEY`: Secret key used by the WTForm library.

## Testing

Testing requires that file *movie-browser/tests/conftest.py* be edited to set the value of `TEST_DATA_PATH`. You should set this to the absolute path of the *COMPSCI-235/tests/data* directory. 

E.g. 

`C:\\Users\\justi\\Desktop\\git-projects\\movie-browser\\tests\\data`