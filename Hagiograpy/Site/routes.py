from flask import render_template, request, flash, redirect


from .app import app
from .modeles.donnees import Oeuvre, Saint, controle


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
    saint_vie1 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    saint_vie2=Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre==vie_id)).all()

    return render_template("pages/vie.html", nom="Site", oeuvre=unique_vie, saints=saint_vie2,saint=saint_vie1)

@app.route("/formulaire", methods=["GET", "POST"])
def formulaire():
    if request.method=="POST":

        statut, donnees=controle(request.form.get("Saint", None)
        ,request.form.get("Titre",None),
        request.form.get("Langue",None),
        request.form.get("Incipit",None),
        request.form.get("Explicit",None),
        request.form.get("Folios",None),
        request.form.get("Date_production",None),
        request.form.get("Lieu_production",None),
        request.form.get("Cote",None),
        request.form.get("Nb_feuillets",None),
        request.form.get("Support",None),
        request.form.get("Hauteur",None),
        request.form.get("Largeur",None),
        request.form.get("Institution",None))

        if statut is True:
            flash("Ajout réussi", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/formulaire.html")

    return render_template("pages/formulaire.html", nom="Site")

