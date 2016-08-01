# URL Shortener
Simple URL Shortener

This app lets you enter a URL and create a shortened URL that redirects to the original.

## Installation

You will need to install the following. These instructions assume you're on a Mac.
* [homebrew](http://brew.sh)
* Download Python3; this app uses version 3.4
  * download version 3.4 from https://www.python.org/downloads/mac-osx/
* pip
    * Download [get-pip.py](https://bootstrap.pypa.io/get-pip.py)
    * `python get-pip.py`
* [postgres](http://postgresapp.com)
* Also install postgres in the terminal with `brew install postgres`

Clone this repo, and run `pip install -r requirements.txt` in it to install Python libaries.

* Make sure postgres is running locally on port 5432
* `psql`
* Create role:
    * `CREATE ROLE url_shortener with CREATEDB LOGIN SUPERUSER;`
* Create database:
    * `CREATE DATABASE url_shortener;`

* `python manage.py migrate`
* `python manage.py createsuperuser` to be able to use the admin page.

## Run

* `python manage.py runserver 5000`
* Open [localhost:5000](localhost:5000)

## Endpoints

- `GET /`: Get the homepage.
- `POST /`: With key `url` in the body, create a code that maps to the URL and display it.
- `GET /somecode`, where `somecode` is a code created by the `POST /` endpoint. Redirects to the code's original URL.

There is also a basic JSON API with the same functionality.
Note that the end slash is necessary with these endpoints.
- `GET /api/redirect_code/somecode/`, where `somecode` is a code created by the `POST /` endpoint. Displays info about the code, such as its original URL.
- `POST /api/redirect_code/`, create a code with the same logic as the `POST /` endpoint and return some info about it.

## Admin

There is also an admin page at `/admin/` that lets you view and create RedirectCode objects.
