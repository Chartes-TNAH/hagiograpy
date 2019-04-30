from flask import render_template, request, flash, redirect, url_for

from .app import app
from sqlalchemy import or_, and_
from .modeles.utilisateurs import User
from .constantes import RESULTS_PER_PAGE
from flask_login import login_user, current_user, logout_user
from flask import flash, redirect, request
from .modeles.donnees import Oeuvre, Saint, Jointure_Saint_Oeuvre, Realisation, Jointure_Oeuvre_Realisation, Manuscrit, Jointure_Manuscrit_Realisation, Institution, Localisation

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
    realisation_oeuv = Realisation.query.filter(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id)).first()
    manuscrit_oeuv = Manuscrit.query.filter(Manuscrit.realisations.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id))).first()
    localisation_oeuv = Localisation.query.filter(Localisation.InstitutionLocalisation.any(Institution.ManuscritInstitution.any(Manuscrit.realisations.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id))))).first()
    lieu_oeuv = Institution.query.filter(Institution.ManuscritInstitution.any(Manuscrit.realisations.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == vie_id)))).first()
    return render_template("pages/vie.html", nom="Site", oeuvre=unique_vie, realisation=realisation_oeuv, conservation=manuscrit_oeuv, localisation=localisation_oeuv, institution=lieu_oeuv, saint=saint_vie1)

@app.route("/manuscrit/<int:mss_id>")
def manuscrit(mss_id):

    """Création d'une page pour un manuscrit dépouillé
    :param mss_id: Id de la clé primaire de la table Manuscrit dans la base de données
    :type mss_id: texte
    :returns: création de page
    :rtype: page HTML du manuscrit souhaité"""

    unique_mss=Manuscrit.query.filter(Manuscrit.IdManuscrit==mss_id).first()
    realisation_oeuv = Realisation.query.filter(Realisation.oeuvres.any(Oeuvre.IdOeuvre == mss_id)).first()
    manuscrit_oeuv = Manuscrit.query.filter(Manuscrit.realisations.any(Realisation.oeuvres.any(Oeuvre.IdOeuvre == mss_id))).first()
    localisation_oeuv = Localisation.query.filter(Localisation.InstitutionLocalisation.any(Institution.ManuscritInstitution.any(Manuscrit.IdManuscrit==mss_id))).first()
    lieu_oeuv = Institution.query.filter(Institution.ManuscritInstitution.any(Manuscrit.IdManuscrit==mss_id)).first()
    return render_template("pages/manuscrit.html", nom="Site", manuscrit=unique_mss, realisation=realisation_oeuv, conservation=manuscrit_oeuv, localisation=localisation_oeuv, institution=lieu_oeuv)

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
    return render_template("pages/saint.html", nom="Site", saint=unique_bio)

#Routes des pages dynamiques (get, post)

@app.route("/formulaire", methods=["GET", "POST"])
def formulaire():
    listenomsaint = Saint.query.with_entities(Saint.Nom_saint).distinct()
    listecopiste=Realisation.query.with_entities(Realisation.Copiste).distinct()
    listedateprod=Realisation.query.with_entities(Realisation.Date_production).distinct()
    listelieuprod=Realisation.query.with_entities(Realisation.Lieu_production).distinct()
    listecote=Manuscrit.query.with_entities(Manuscrit.Cote).distinct()
    listetitre_manuscrit=Manuscrit.query.with_entities(Manuscrit.Titre).distinct()
    listenbfeuillet=Manuscrit.query.with_entities(Manuscrit.Nb_feuillets).distinct()
    listeprovenance=Manuscrit.query.with_entities(Manuscrit.Provenance).distinct()
    listesupport=Manuscrit.query.with_entities(Manuscrit.Support).distinct()
    listehauteur=Manuscrit.query.with_entities(Manuscrit.Hauteur).distinct()
    listelargeur=Manuscrit.query.with_entities(Manuscrit.Largeur).distinct()
    listeinstitution=Institution.query.with_entities(Institution.Nom_institution).distinct()
    listelocalisation=Localisation.query.with_entities(Localisation.Ville).distinct()
    listetitrereal=Oeuvre.query.with_entities(Oeuvre.Titre).distinct()
    listeauteur=Oeuvre.query.with_entities(Oeuvre.Auteur).distinct()
    listelangue=Oeuvre.query.with_entities(Oeuvre.Langue).distinct()
    listeincipit=Oeuvre.query.with_entities(Oeuvre.Incipit).distinct()
    listeexplicit=Oeuvre.query.with_entities(Oeuvre.Explicit).distinct()
    listefolios=Oeuvre.query.with_entities(Oeuvre.Folios).distinct()
    listeliensite=Oeuvre.query.with_entities(Oeuvre.URL).distinct()
    listeiiif=Oeuvre.query.with_entities(Oeuvre.IIIF).distinct()

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


    return render_template("pages/formulaire.html", nom="Site",Listenomsaint=listenomsaint,Listecopiste=listecopiste,Listedateprod=listedateprod,
                           Listelieuprod=listelieuprod,Listecote=listecote,Listetitremanuscrit=listetitre_manuscrit,Listenbfeuillet=listenbfeuillet,
                           Listeprovenance=listeprovenance,Listesupport=listesupport,Listehauteur=listehauteur, Listelargeur=listelargeur
                           , Listeinstitution=listeinstitution, Listelocalisation=listelocalisation, Listetitrereal=listetitrereal,
                           Listeauteur=listeauteur,Listelangue=listelangue,Listeincipit=listeincipit,Listeexplicit=listeexplicit,
                                   Listefolios=listefolios,ListeURL=listeliensite,Listeiiif=listeiiif)


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
            return redirect(url_for("accueil"))
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
        return redirect(url_for("accueil"))
    # Si on est en POST, cela veut dire que le formulaire a été envoyé
    if request.method == "POST":
        utilisateur = User.identification(
            login=request.form.get("login", None),
            motdepasse=request.form.get("motdepasse", None)
        )
        if utilisateur:
            flash("Connexion effectuée", "success")
            login_user(utilisateur)
            return redirect(url_for("accueil"))
        else:
            flash("Les identifiants n'ont pas été reconnus", "error")
    return render_template("pages/connexion.html")
  

@app.route("/deconnexion", methods=["POST", "GET"])
def deconnexion():
    if current_user.is_authenticated is True:
        logout_user()
    flash("Vous êtes déconnecté-e", "info")
    return redirect(url_for("accueil"))
  

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
            Oeuvre.Folios.like("%{}%".format(motclef)),
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


@app.route('/rechercheavancee', methods=["POST", "GET"])
def rechercheavancee ():
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    if request.method == "POST":

        resultats = []

        titre = "Recherche"

        keyword="test"
        question=Oeuvre.query

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

        if nomSaint:
            question=question.filter(Oeuvre.saint.any(Saint.Nom_saint.like("%{}%".format(nomSaint))))
        if titreReal:
            question=question.filter(Oeuvre.Titre.like("%{}%".format(titreReal)))
        if auteur:
            question=question.filter(Oeuvre.Auteur.like("%{}%".format(auteur)))
        if langue:
            question=question.filter(Oeuvre.Langue.like("%{}%".format(langue)))
        if incipit:
            question=question.filter( Oeuvre.Incipit.like("%{}%".format(incipit)))
        if explicit:
            question=question.filter(Oeuvre.Explicit.like("%{}%".format(explicit)))
        if folios:
            question=question.filter(Oeuvre.Folios.like("%{}%".format(folios)))
        if liensite:
            question=question.filter(Oeuvre.URL.like("%{}%".format(liensite)))
        if iiif:
            question=question.filter(Oeuvre.IIIF.like("%{}%".format(iiif)))
        if copiste:
            question=question.filter(Oeuvre.realisations.any(Realisation.Copiste.like("%{}%".format(copiste))))
        if dateprod:
            question=question.filter(Oeuvre.realisations.any(Realisation.Date_production.like("%{}%".format(dateprod))))
        if lieuprod:
            question = question.filter(Oeuvre.realisations.any(Realisation.Lieu_production.like("%{}%".format(lieuprod))))
        if cote:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Cote.like("%{}%".format(cote)))))
        if titre_manuscrit:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Titre.like("%{}%".format(titre_manuscrit)))))
        if nbfeuillet:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Nb_feuillets.like("%{}%".format(nbfeuillet)))))
        if provenance:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Provenance.like("%{}%".format(provenance)))))
        if support:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Support.like("%{}%".format(support)))))
        if hauteur:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Hauteur.like("%{}%".format(hauteur)))))
        if largeur:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.Largeur.like("%{}%".format(largeur)))))
        if institution:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.InstitutionManuscrit.has(Institution.Nom_institution.like("%{}%".format(institution))))))
        if localisation:
            question = question.filter(Oeuvre.realisations.any(Realisation.manuscrits.any(Manuscrit.InstitutionManuscrit.has(Institution.LocalisationInstitution.has(Localisation.Ville.like("%{}%".format(localisation)))))))
        question=question.paginate(page=page)

        return render_template(
            "pages/recherche.html",
            resultats=question,
            titre=titre,
            keyword=keyword
        )


    return render_template("pages/rechercheavancee.html",nom="Site")

@app.route('/formulairemanuscrit', methods=["GET", "POST"])
def formulaire_manuscrit():

    listemanuscrit=Manuscrit.query.all()
    listeinstitution=Institution.query.all()

    if request.method == "POST":
        cote=request.form.get("Cote",None)
        titre_manuscrit=request.form.get("Titre_Manuscrit", None)
        nbfeuillet=request.form.get("Nb_feuillets",None)
        provenance=request.form.get("Provenance", None)
        support=request.form.get("Support",None)
        hauteur=request.form.get("Hauteur",None)
        largeur=request.form.get("Largeur",None)
        institution=request.form.get("Institution",None)
        recup = Institution.query.filter(Institution.Nom_institution == institution).first()

        Manuscrit.ajouter(cote, titre_manuscrit,
                                         nbfeuillet,
                                         provenance, support,
                                         hauteur, largeur, recup.IdInstitution)
        flash("Ajout réussi", "success")
        return render_template('pages/formulaire_manuscrit.html', nom="Site", Listemanuscrit=listemanuscrit,
                               Listeinstitution=listeinstitution)

    return render_template('pages/formulaire_manuscrit.html', nom="Site",Listemanuscrit=listemanuscrit,Listeinstitution=listeinstitution)

@app.route('/formulaire_realisation', methods=["GET", "POST"])
def formulaire_realisation():
    listecopiste=Realisation.query.order_by(Realisation.Copiste).all()
    listedateprod=Realisation.query.order_by(Realisation.Date_production).all()
    listelieuprod=Realisation.query.order_by(Realisation.Lieu_production).all()

    if request.method=="POST":
        copiste=request.form.get("Copiste", None)
        dateprod=request.form.get("Date_production", None)
        lieuprod=request.form.get("Lieu_production",None)
        Realisation.ajouter(dateprod,
                                             lieuprod,
                                             copiste)
        flash("Ajout réussi", "success")
        return render_template('pages/formulaire_realisation.html', nom="Site", Listecopiste=listecopiste,
                               Listedateprod=listedateprod, Listelieuprod=listelieuprod)

    return render_template('pages/formulaire_realisation.html', nom="Site",Listecopiste=listecopiste,Listedateprod=listedateprod,Listelieuprod=listelieuprod)

@app.route('/formulaire_saint', methods=["GET", "POST"])
def formulaire_saint():
    listesaint = Saint.query.order_by(Saint.Nom_saint).all()
    listebiosaint=Saint.query.order_by(Saint.Biographie).all()

    if request.method=="POST":
        nomSaint = request.form.get("Saint", None)
        bioSaint = request.form.get("BioSaint",None)
        Saint.ajouter(nomSaint,bioSaint)

        flash("Ajout réussi", "success")
        return render_template("pages/formulaire_saint.html", Listenomsaint=listesaint,Listebiosaint=listebiosaint)


    return render_template('pages/formulaire_saint.html', Listenomsaint=listesaint,Listebiosaint=listebiosaint)

@app.route('/formulaire_institution', methods=["GET", "POST"])
def formulaire_institution():
    listeinstitution=Institution.query.all()
    listelocalisation=Localisation.query.all()

    if request.method=="POST":

        institution=request.form.get("Institution",None)
        localisation=request.form.get("Localisation",None)
        id_localisation = Localisation.ajouter(localisation)
        Institution.ajouter(institution, id_localisation)
        flash("Ajout réussi", "success")
        return render_template('pages/formulaire_institution.html', nom="Site", Listeinstitution=listeinstitution,
                               Listelocalisation=listelocalisation)


    return render_template('pages/formulaire_institution.html', nom="Site",Listeinstitution=listeinstitution,Listelocalisation=listelocalisation)

@app.route('/formulaire_oeuvre', methods=["GET", "POST"])
def formulaire_oeuvre():
    listeOeuvre=Oeuvre.query.all()
    if request.method == "POST":
        titreReal=request.form.get("Titre", None)
        auteur=request.form.get("Auteur",None)
        langue=request.form.get("Langue", None)
        incipit=request.form.get("Incipit", None)
        explicit=request.form.get("Explicit",None)
        folios=request.form.get("Folios",None)
        liensite=request.form.get("Lien_site", None)
        iiif=request.form.get("IIIF",None)

        Oeuvre.ajouter(titreReal,auteur,langue,incipit,explicit,folios,liensite,iiif)
        flash("Ajout réussi", "success")
        return render_template('pages/formulaire_oeuvre.html', nom="Site")

    return render_template('pages/formulaire_oeuvre.html', nom="Site")

#Routes des pages annexes

@app.route('/about')
def about():
    return render_template("pages/a-propos.html", nom="Site")

@app.route('/cgu')
def cgu():
    return render_template("pages/cgu.html", nom="Site")