from flask import render_template, request, flash, redirect

from .app import app
from sqlalchemy import or_
from .modeles.utilisateurs import User
from .constantes import RESULTS_PER_PAGE
from flask_login import login_user, current_user, logout_user
from flask import flash, redirect, request
from .modeles.donnees import Oeuvre, Saint, controle, Jointure_Saint_Oeuvre, Realisation, Jointure_Oeuvre_Realisation, Manuscrit, Jointure_Manuscrit_Realisation, Institution, Localisation


@app.route("/")
def accueil():
    oeuvres = Oeuvre.query.all()
    return render_template("pages/accueil.html", nom="Site", oeuvres=oeuvres)

@app.route("/oeuvre/<int:vie_id>")
def oeuvre(vie_id):

    """Création d'une page pour une vie de Saint
    :param vie_id: Id de la vie clé primaire de la table oeuvre dans la base de données
    :type vie_id: texte
    :returns: création de page
    :rtype: page HTML de la vie souhaitée"""

    unique_vie=Oeuvre.query.filter(Oeuvre.IdOeuvre==vie_id).first()
    # On fait la requête sur la table Saint mais on l'a filtre en récupérant dans la base à travers la relation oeuvres
    # n'importe qu'elle valeur dont Oeuvre.idOeuvre correspond à la valeur d'entrée
    saint_vie1 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    saint_vie2 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).all()
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
        iiif=request.form.get("IIIF",None)
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


        statut, donnees=controle(nomSaint,titreReal,langue,incipit,explicit,folios,dateprod,lieuprod,cote,nbfeuillet,support,hauteur,largeur,institution,localisation,iiif)


        if statut is True:

            id_localisation=Localisation.ajouter(localisation)
            id_institution=Institution.ajouter(institution, id_localisation)
            id_saint = Saint.ajouter(nomSaint)
            id_oeuvre = Oeuvre.ajouter(titreReal, auteur,
                                       langue, incipit,
                                       explicit,folios,liensite,iiif)
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


@app.route("/register", methods=["GET", "POST"])
def inscription():
    """ Route gérant les inscriptions
    """
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        statut, donnees = User.creer(
            login=request.form.get("login", None),
            email=request.form.get("email", None),
            nom=request.form.get("nom", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if statut is True:
            flash("Enregistrement effectué. Identifiez-vous maintenant", "success")
            return redirect("/")
        else:
            flash("Les erreurs suivantes ont été rencontrées : " + ",".join(donnees), "error")
            return render_template("pages/inscription.html")
    else:
        return render_template("pages/inscription.html")
      

@app.route("/connexion", methods=["POST", "GET"])
def connexion():
    """ Route gérant les connexions
    """
    if current_user.is_authenticated is True:
        flash("Vous êtes déjà connecté-e", "info")
        return redirect("/")
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect("/")
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("pages/connexion.html")
  

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect("/")
  

@app.route('/about')
def about():
    return render_template("pages/a-propos.html", nom="Site")
  

@app.route("/recherche")
def recherche():

    motclef = request.args.get("keyword", None)
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    resultats = []

    titre = "Recherche"
    if motclef:
        resultats = Oeuvre.query.filter(or_(
            Oeuvre.saint.any(Saint.Nom_saint.like("%{}%".format(motclef))),
            Oeuvre.Titre.like("%{}%".format(motclef)),
            Oeuvre.Auteur.like("%{}%".format(motclef)),
            Oeuvre.Langue.like("%{}%".format(motclef)),
            Oeuvre.Incipit.like("%{}%".format(motclef)),
            Oeuvre.Explicit.like("%{}%".format(motclef)),
            Oeuvre.Langue.like("%{}%".format(motclef)),
            Oeuvre.realisations.any(Realisation.Lieu_production.like("%{}%".format(motclef))),
            Oeuvre.realisations.any(Realisation.Copiste.like("%{}%".format(motclef))),
            Oeuvre.realisations.any(Realisation.Date_production.like("%{}%".format(motclef))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Titre.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Cote.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Nb_feuillets.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Support.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Hauteur.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Largeur.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Provenance.like("%{}%".format(motclef)))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.InstitutionManuscrit.has(Institution.Nom_institution.like("%{}%".format(motclef))))),
            Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.InstitutionManuscrit.has(Institution.LocalisationInstitution.has(Localisation.Ville.like("%{}%".format(motclef))))))

        )
        ).paginate(page=page)

        titre = "Résultat pour la recherche `" + motclef + "`"

    return render_template(
        "pages/recherche.html",
        resultats=resultats,
        titre=titre,
        keyword=motclef
    )
  

@app.route('/cgu')
def cgu():
    return render_template("pages/cgu.html", nom="Site")