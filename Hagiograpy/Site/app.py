from flask import Flask, request, jsonify, send_file
from flask_sqlalchemy import SQLAlchemy
from iiif2 import IIIF, web

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


#IIIF Web Service
@app.route('/<identifier>/info.json')
def info(identifier):
      return jsonify(web.info(request.url_root, identifier))
      

@app.route('/<identifier>/<region>/<size>/<rotation>/<quality>.<fmt>')
def iiif(**kwargs):
    params = web.Parse.params(**kwargs)
    path = resolve(params.get('identifier'))
    with IIIF.render(path, **params) as tile:
        return send_file(tile, mimetype=tile.mime)

def resolve(identifier):
    """Résolveur d'identifiant iiif vers le chemin de la ressource sur le disque.
    Cette méthode est spécifique à l'architecture de ce serveur.
    """
    return os.path.join(chemin_actuel, 'images', '%s.jpg' % identifier)

if __name__ == "__main__":
    app.run(debug=True)



