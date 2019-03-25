from flask import render_template, request, flash, redirect


from .app import app
from .modeles.donnees import Oeuvre, Saint, controle, Jointure_Saint_Oeuvre, Realisation, Jointure_Oeuvre_Realisation, Manuscrit, Jointure_Manuscrit_Realisation, Institution, Localisation


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
        #Saint
        nomSaint=request.form.get("Saint", None)
        #Oeuvre
        titreReal=request.form.get("Titre", None)
        auteur=request.form.get("Auteur",None)
        langue=request.form.get("Langue", None)
        incipit=request.form.get("Incipit", None)
        explicit=request.form.get("Explicit",None)
        folios=request.form.get("Folios",None)
        liensite=request.form.get("Lien_site", None)
        #Realisation
        copiste=request.form.get("Copiste", None)
        dateprod=request.form.get("Date_production", None)
        lieuprod=request.form.get("Lieu_production",None)
        #Manuscrit
        cote=request.form.get("Cote",None)
        titre_manuscrit=request.form.get("Titre_Manuscrit", None)
        nbfeuillet=request.form.get("Nb_feuillets",None)
        provenance=request.form.get("Provenance", None)
        support=request.form.get("Support",None)
        hauteur=request.form.get("Hauteur",None)
        largeur=request.form.get("Largeur",None)
        institution=request.form.get("Institution",None)
        localisation=request.form.get("Localisation",None)


        statut, donnees=controle(nomSaint,titreReal,langue,incipit,explicit,folios,dateprod,lieuprod,cote,nbfeuillet,support,hauteur,largeur,institution,localisation)


        if statut is True:

            id_localisation=Localisation.ajouter(localisation)
            id_institution=Institution.ajouter(institution, id_localisation)
            id_saint = Saint.ajouter(nomSaint)
            id_oeuvre = Oeuvre.ajouter(titreReal, auteur,
                                       langue, incipit,
                                       explicit,folios,liensite)
            id_realisation = Realisation.ajouter(dateprod,
                                                 lieuprod,
                                                 copiste)
            id_manuscrit = Manuscrit.ajouter(cote,titre_manuscrit ,
                                             nbfeuillet,
                                             provenance, support,
                                             hauteur, largeur,id_institution)
            Saint.association_Oeuvre_Saint(id_saint, id_oeuvre)
            Realisation.association_Oeuvre_Realisation(id_oeuvre, id_realisation)
            Manuscrit.association_manuscrit_realisation(id_manuscrit, id_realisation)
            flash("Ajout réussi", "success")
            return render_template("pages/formulaire.html")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/formulaire.html")

    return render_template("pages/formulaire.html", nom="Site")

