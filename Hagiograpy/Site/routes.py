from flask import render_template

from .app import app
from .modeles.donnees import Oeuvre, Saint


# IIIF Web Service
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


@app.route("/")
def accueil():
    oeuvres = Oeuvre.query.all()
    return render_template("pages/accueil.html", nom="Site", oeuvres=oeuvres)

@app.route("/oeuvre/<int:vie_id>")
def oeuvre(vie_id):
    """ Création d'une page pour une vie de Saint

    :param vie_id: Id de la vie clé primaire de la table oeuvre dans la base de données
    :type vie_id: texte
    :returns: création de page
    :rtype: page HTML de la vie souhaité
    """
    unique_vie=Oeuvre.query.filter(Oeuvre.IdOeuvre==vie_id).first()
    #On fait la requête sur la table Saint mais on l'a filtre en récupérant dans la base à travers la relation oeuvres
    # n'importe qu'elle valeur dont Oeuvre.idOeuvre correspond à la valeur d'entrée
    saint_vie1=Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre==vie_id)).first()
    saint_vie2=Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre==vie_id)).all()

    return render_template("pages/vie.html", nom="Site", oeuvre=unique_vie, saints=saint_vie2, saint=saint_vie1)

