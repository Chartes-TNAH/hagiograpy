web: gunicorn run:app
init: FLASK_APP=run.py flask db init
release: python manage.py db upgrade