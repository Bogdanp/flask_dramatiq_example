# flask_dramatiq_example

[![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy)

An example app demonstrating how you can use [Dramatiq][dramatiq] with [Flask][flask].

**:warning: A full-featured [Flask-Dramatiq](https://flask-dramatiq.rtfd.io) extension is now available! :cake:**


## Setup

1. Clone the repo, then run `pipenv install`.
1. Run [Postgres][postgres], then run `psql -c "create database flask_dramatiq_example;" -U postgres`.
1. Run [RabbitMQ][rabbitmq].
1. Run `pipenv run python -c 'from app import Model, database; Model.metadata.create_all(database)'` to create the database.
1. Run the web server: `pipenv run flask run --reload`.
1. Run the workers: `pipenv run dramatiq app`.


## License

flask_dramatiq_example is licensed under Apache 2.0.  Please see
[LICENSE][license] for licensing details.


[dramatiq]: https://dramatiq.io/
[flask]: http://flask.pocoo.org/
[postgres]: https://www.postgresql.org/
[rabbitmq]: https://www.rabbitmq.com/
[license]: https://github.com/Bogdanp/flask_dramatiq_example/blob/master/LICENSE
