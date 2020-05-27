# Flask-Demo

Contents:

app.py: root flask app
db.sqlite3: local sqlite db
run-app.sh: in linux terminal, run ./run-app.sh PORT_NUMBER to set up environment and launch the Flask server for the API. If no port is specified, default is 3000.

Scalability and Design Considerations:

In this case, we have used a local database -- sqlite, but this is not scalable (as it is a local db). Scaling would require the use of a server-connecting SQL database (Postgres/MySQL/other) for the API to have larger scope. With this, we would also likely need to host the API on a more public server as opposed to a localhost. This opens doors to potential issues with multiple concurrent requests to the API, and we may need to make our app threadsafe to prevent race conditions/specification violations. We may also add more tables/routes/functionality in a situation like this to make the API more useful.