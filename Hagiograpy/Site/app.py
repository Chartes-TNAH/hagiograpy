from flask import Flask
from flask_sqlalchemy import SQLAlchemy

import os
import os.path

chemin_actuel = os.path.dirname(os.path.abspath(__file__))
templates = os.path.join(chemin_actuel, "templates")
statics = os.path.join(chemin_actuel, "static")

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)

# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db_HagiograPY'
# On initie l'extension
db = SQLAlchemy(app)

from .routes import oeuvre, accueil

if __name__ == "__main__":
    app.run(debug=True)



