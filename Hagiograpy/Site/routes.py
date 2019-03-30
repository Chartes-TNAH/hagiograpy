from flask import render_template, request, flash, redirect

from .app import app
from sqlalchemy import or_
from .modeles.utilisateurs import User
from .constantes import RESULTS_PER_PAGE
from flask_login import login_user, current_user, logout_user
from flask import flash, redirect, request
from .modeles.donnees import Oeuvre, Saint, controle, Jointure_Saint_Oeuvre, Realisation, Jointure_Oeuvre_Realisation, Manuscrit, Jointure_Manuscrit_Realisation, Institution, Localisation

#Route de la page d'accueil

@app.route("/")
def accueil():
    return render_template("pages/accueil.html", nom="Site")

#Routes pour les pages d'index

@app.route("/index_vies")
def index_vies():
    oeuvres = Oeuvre.query.all()
    return render_template("pages/index_vies.html", nom="Site", oeuvres=oeuvres)

@app.route("/index_saints")
def index_saints():
    saints = Saint.query.all()
    return render_template("pages/index_saints.html", nom="Site", saints=saints)

@app.route("/index_mss")
def index_mss():
    manuscrits = Manuscrit.query.all()
    return render_template("pages/index_mss.html", nom="Site", manuscrits=manuscrits)

@app.route("/index_bib")
def index_bib():
    bibliotheques = Institution.query.all()
    return render_template("pages/index_bib.html", nom="Site", bibliotheques=bibliotheques)

#Routes des pages de contenu

@app.route("/oeuvre/<int:vie_id>")
def oeuvre(vie_id):

    """Création d'une page pour une vie de Saint
    :param vie_id: Id de la clé primaire de la table Oeuvre dans la base de données
    :type vie_id: texte
    :returns: création de page
    :rtype: page HTML de la vie souhaitée"""

    unique_vie=Oeuvre.query.filter(Oeuvre.IdOeuvre==vie_id).first()
    # On fait la requête sur la table Saint mais on la filtre en récupérant dans la base à travers la relation oeuvres
    # n'importe qu'elle valeur dont Oeuvre.idOeuvre correspond à la valeur d'entrée
    saint_vie1 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    saint_vie2 = Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).all()
    realisation_oeuv = Realisation.query.filter(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    manuscrit_oeuv = Manuscrit.query.filter(Manuscrit.realisations.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id))).first()
    localisation_oeuv = Localisation.query.filter(Localisation.InstitutionLocalisation.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id))).first()
    lieu_oeuv = Institution.query.filter(Localisation.InstitutionLocalisation.any(Oeuvre.IdOeuvre == vie_id)).first()
    return render_template("pages/vie.html", nom="Site", oeuvre=unique_vie, realisation=realisation_oeuv, conservation=manuscrit_oeuv, localisation=localisation_oeuv, institution=lieu_oeuv, saint=saint_vie1)

@app.route("/manuscrit/<int:mss_id>")
def manuscrit(mss_id):

    """Création d'une page pour un manuscrit dépouillé
    :param mss_id: Id de la clé primaire de la table Manuscrit dans la base de données
    :type mss_id: texte
    :returns: création de page
    :rtype: page HTML du manuscrit souhaité"""

    unique_mss=Manuscrit.query.filter(Manuscrit.IdManuscrit==mss_id).first()
    return render_template("pages/manuscrit.html", nom="Site", manuscrit=unique_mss)

@app.route("/institution/<int:bib_id>")
def institution(bib_id):

    """Création d'une page pour une institution conservatrice
    :param bib_id: Id de la clé primaire de la table Institution dans la base de données
    :type bib_id: texte
    :returns: création de page
    :rtype: page HTML de l'institution souhaitée"""

    unique_bib=Institution.query.filter(Institution.IdInstitution==bib_id).first()
    return render_template("pages/institution.html", nom="Site", institution=unique_bib)

@app.route("/saint/<int:st_id>")
def saint(st_id):

    """Création d'une page pour une biographie de Saint
    :param st_id: Id de la clé primaire de la table Saint dans la base de données
    :type st_id: texte
    :returns: création de page
    :rtype: page HTML de la biographie souhaitée"""

    unique_bio=Saint.query.filter(Saint.IdSaint==st_id).first()
    #st_biogr=Saint.query.filter(Saint.oeuvres.any(Oeuvre.IdOeuvre == st_id)).first()
    return render_template("pages/saint.html", nom="Site", saint=unique_bio)

#Routes des pages dynamiques (get, post)

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

#Routes des pages annexes

@app.route('/about')
def about():
    return render_template("pages/a-propos.html", nom="Site")

@app.route('/cgu')
def cgu():
    return render_template("pages/cgu.html", nom="Site")