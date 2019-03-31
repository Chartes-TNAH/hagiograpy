from warnings import warn
import os

RESULTS_PER_PAGE = 2
SECRET_KEY = "abfezi456efz"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)

if os.environ.get('DATABASE_URL') is None:
    class _PRODUCTION:
        SECRET_KEY = SECRET_KEY
        # On configure la base de données de production
        SQLALCHEMY_DATABASE_URI = 'sqlite:///../db_HagiograPY'
        SQLALCHEMY_TRACK_MODIFICATIONS = False
else:
    class _PRODUCTION:
        SECRET_KEY = SECRET_KEY
        # On configure la base de données de production
        SQLALCHEMY_DATABASE_URI = os.environ['DATABASE_URL']
        SQLALCHEMY_TRACK_MODIFICATIONS = False


CONFIG = {
        "production": _PRODUCTION
    }
