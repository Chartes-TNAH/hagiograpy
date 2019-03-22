from flask import Flask
from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD

import os
import os.path
=======
from flask_login import LoginManager
import os
from .constantes import SECRET_KEY


>>>>>>> dev_comptes_utilisateurs

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

# On configure la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///./db_HagiograPY'
app.secret_key='test'
# On initie l'extension
db = SQLAlchemy(app)

<<<<<<< HEAD
from .routes import oeuvre, accueil

if __name__ == "__main__":
    app.run(debug=True)

=======
# On met en place la gestion d'utilisateur-rice-s
login = LoginManager(app)
>>>>>>> dev_comptes_utilisateurs

from .routes import accueil, oeuvre, inscription, connexion, deconnexion

