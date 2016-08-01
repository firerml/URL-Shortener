# URL Shortener
Simple URL Shortener

This app lets you enter a URL and create a shortened URL that redirects to the original.

## Endpoints

- `GET /`: Get the homepage.
- `POST /`: With key `url` in the body, create a code that maps to the URL and display it.
- `GET /somecode`, where `somecode` is a code created by the `POST /` endpoint. Redirects to the code's original URL.

There is also a basic JSON API with the same functionality.
Note that the end slash is necessary with these endpoints.
- `GET /api/redirect_code/somecode/`, where `somecode` is a code created by the `POST /` endpoint. Displays info about the code, such as its original URL.
- `POST /api/redirect_code/`, create a code with the same logic as the `POST /` endpoint and return some info about it.
