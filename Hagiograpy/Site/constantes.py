from warnings import warn

RESULTS_PER_PAGE = 2
SECRET_KEY = "JE SUIS UN SECRET !"

if SECRET_KEY == "JE SUIS UN SECRET !":
    warn("Le secret par défaut n'a pas été changé, vous devriez le faire", Warning)
