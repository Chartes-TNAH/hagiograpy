from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os
import os.path
from .constantes import SECRET_KEY


chemin_actuel = os.path.dirname(os.path.abspath(__file__))
# on stocke le chemin du fichier courant
templates = os.path.join(chemin_actuel, "templates")
# on stocke le chemin vers les templates
statics = os.path.join(chemin_actuel, "static")
# on stocke le chemin vers les statics

app = Flask(
    "Application",
    template_folder=templates,
    static_folder=statics
)
# On configure le secret
app.config['SECRET_KEY'] = SECRET_KEY
# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db_HagiograPY'

# On initie l'extension
db = SQLAlchemy(app)


# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)

from .routes import accueil, oeuvre, inscription, connexion, deconnexion, formulaire, cgu

if __name__ == "__main__":
    app.run(debug=True)
