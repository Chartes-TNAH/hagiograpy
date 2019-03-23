from flask import render_template

from .app import app
from .modeles.donnees import Oeuvre, Saint, Manuscrit, Realisation, Localisation, Institution
from .modeles.utilisateurs import User
from .constantes import RESULTS_PER_PAGE
from flask_login import login_user, current_user, logout_user
from flask import flash, redirect, request
from sqlalchemy import or_


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


@app.route('/rechercheavancee')
def rechercheavancee():
    """Route permettant de créer le formulaire de recherche avancée"""
    saint = Saint.query.order_by(Saint.Nom_saint).all()
    texte = Oeuvre.query.order_by(Oeuvre.Titre).all()
    cote = Manuscrit.query.order_by(Manuscrit.Cote).all()
    institution = Institution.query.order_by(Institution.Nom_institution).all()
    ville = Localisation.query.order_by(Localisation.Ville).all()
    date_prod = Realisation.query.order_by(Realisation.Date_production).all()
    lieu_prod = Realisation.query.order_by(Realisation.Lieu_production).all()
    # Les variables ci-dessus permettent de stocker les valeurs des tables concernées,
    # ce qui nous permet par la suite de les faire apparaître dans des menus déroulants dans notre page recherche.html
    return render_template("pages/rechercheavancee.html", saint=saint, texte=texte, cote=cote, institution=institution, ville=ville, date_prod=date_prod, lieu_prod=lieu_prod)

@app.route('/resultats')
def resultats():
    """ Route permettant la recherche plein-texte
    """
    motclef = request.args.get("motclef", None)
    # On stocke dans la variable mot-clef une liste qui est destinée à contenir la valeur du mot-clé rentré par l'utilisateur dans la barre de recherche
    page = request.args.get("page", 1)
    # On stocke dans la variable page une liste qui est destinée à contenir la valeur du numéro de page

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1
    # Si le numéro de la page est une chaîne de caractères composée uniquement de chiffres
    # Alors on la recaste en integer
    # Sinon, le numéro de la page est égal à 1

    resultats = []
    # On crée une liste vide de résultats (qui restera vide par défaut si on n'a pas de mot clé)

    if motclef:
    # Si on a un mot-clé, on requête toutes les tables de notre base de données pour vérifier s'il y a des correspondances
    # Le résultat de cette requête est stocké dans la liste resultats = []
        resultats = Oeuvre.query

    return render_template("pages/resultats.html", resultats=resultats, titre=titre, motclef=motclef)
    # On retourne la page resultats.html, et on indique à quoi correspondent les variables resultats, titre et keyword,
    # qui seront appelées ensuite au sein des pages html


@app.route('/resultats_avances')
def resultats_avances():
    """ Route permettant d'effectuer une recherche dite avancée sur la base
    de données, en requêtant les champs suivants : occupation, distinction,
    pays de nationalité, domaine d'activité, titre de thèse d'école,
    ainsi que date de soutenance, de décès et de mort (il est possible de requêter
    les dates précises, ou de définir un intervalle)
    """
    # Il faut premièrement aller récupérer les valeurs entrées dans le formulaire de recherche par l'utilisateur :
    # Ces valeurs sont stockées dans des variables, auxquelles se réfère l'attribut name des éléments select ou input
    # de la page de formulaire recherche.html
    motclef = request.args.get("motclef", None)
    saint = request.args.get("saint", None)
    texte = request.args.get("texte", None)
    cote = request.args.get("cote", None)
    institution = request.args.get("institution", None)
    ville = request.args.get("ville", None)
    date_prod = request.args.get("date_prod", None)
    lieu_prod = request.args.get("lieu_prod", None)

    # Mêmes commentaires que pour la pagination effectuée pour la fonction résultats
    page = request.args.get("page", 1)

    if isinstance(page, str) and page.isdigit():
        page = int(page)
    else:
        page = 1

    message = []
    # Cette variable sert à stocker les potentiels messages d'erreurs :

    requete = Oeuvre.query
    # Déclaration d'une variable requete qui nous servira à stocker les recherches réalisées et à combiner plusieurs champs lors du requêtage.
    # ainsi qu'à alléger la syntaxe de notre code
    # Notre requete étant ensuite filtrée, nous lui attribuons la valeur initiale permettant ensuite de filter les champs de la table individu.

    # Le premier champ de la recherche avancée est en fait le même champ que celui de la recherche simple, c'est-à-dire de la fonction resultats()
    if motclef :
        requete = requete.filter(or_(
            Saint.Nom_saint.like("%{}%".format(motclef)),
            Oeuvre.Titre.like("%{}%".format(motclef)),
            Manuscrit.Cote.like("%{}%".format(motclef)),
            Realisation.Lieu_production.like("%{}%".format(motclef)),
            Realisation.Date_production.like("%{}%".format(motclef)),
            Institution.Nom_institution.like("%{}%".format(motclef)),
            Localisation.Ville.like("%{}%".format(motclef)),
            ))

    requete = requete.order_by(Oeuvre.Titre.asc()).paginate(page=page, per_page=RESULTS_PER_PAGE)

    titre = "Résultats"
    return render_template(
        "pages/resultats_avances.html",
        motclef=motclef,
        saint=saint,
        texte=texte,
        cote=cote,
        institution=institution,
        ville=ville,
        date_prod=date_prod,
        lieu_prod=lieu_prod,
    )



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