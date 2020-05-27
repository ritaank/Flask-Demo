# Flask-Demo

Scalability and Design Considerations:

In this case, we have used a local database -- sqlite, but this is not scalable (a local db). Scaling up would require the use of a server-connecting SQL database (Postgres/MySQL/other) for the API to have larger scope. With this, we would also likely need to host the API on a more public server as opposed to a localhost. This opens doors to potential issues with multiple concurrent requests to the API, and we may need to make our app threadsafe to prevent race conditions/specification violations. We may also add more tables/routes/functionality in a situation like this to make the API more useful.

When running the shell script run-app.sh, you may encounter "Permission denied" or a similar error.
Running " chmod +x run-app.sh " will give the script permission to execute, and solve problem.