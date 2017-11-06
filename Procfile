web: bin/start-pgbouncer-stunnel pipenv run gunicorn app:app --log-file -
worker: bin/start-pgbouncer-stunnel pipenv run dramatiq app -p4