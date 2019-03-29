from .. app import db


Jointure_Saint_Oeuvre= db.Table('Jointure_Saint_Oeuvre',
                          db.Column('Oeuvre_IdOeuvre', db.Integer, db.ForeignKey('oeuvre.IdOeuvre'), primary_key=True),
                          db.Column('Saint_IdSaint', db.Integer, db.ForeignKey('saint.IdSaint'),primary_key=True))

Jointure_Manuscrit_Realisation=db.Table('Jointure_Manuscrit_Realisation',
                                        db.Column('Manuscrit_IdManuscrit',db.Integer, db.ForeignKey('manuscrit.IdManuscrit'),primary_key=True),
                                        db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('realisation.IdRealisation'),primary_key=True))
Jointure_Oeuvre_Realisation=db.Table('Jointure_Oeuvre_Realisation',
                                     db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('realisation.IdRealisation'),primary_key=True),
                                     db.Column('Oeuvre_IdOeuvre',db.Integer,db.ForeignKey('oeuvre.IdOeuvre'),primary_key=True))
# On crée notre modèle
class Oeuvre(db.Model):
#Création de la classe centrale oeuvre
    __tablename__="oeuvre"
    IdOeuvre = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Titre = db.Column(db.Text)
    Auteur=db.Column(db.Text)
    Langue=db.Column(db.Text)
    Incipit=db.Column(db.Text)
    Explicit=db.Column(db.Text)
    URL=db.Column(db.Text)
    IIIF = db.Column(db.Text)
    Folios = db.Column(db.Text)
    saint = db.relationship('Saint', secondary=Jointure_Saint_Oeuvre, backref='oeuvre')
    realisations= db.relationship('Realisation', secondary=Jointure_Oeuvre_Realisation, backref='oeuvre')

    @staticmethod
    def ajouter(titre, auteur, langue, incipit, excipit,folios, lien_site,iiif):
        """

        :param titre: Titre de l'oeuvre ajouter dans formulaire.html
        :param auteur: Auteur de l'oeuvre ajouter dans formulaire.html
        :param langue: Langue de l'oeuvre ajouter dans formulaire.html
        :param incipit: Incipit de l'oeuvre ajouter dans formulaire.html
        :param excipit: Excipit de l'oeuvre ajouter dans formulaire.html
        :param folios: Folio de l'oeuvre ajouter dans formulaire.html
        :param lien_site: Lien du site ajouter dans formulaire.html
        :param iiif: Lien du manifeste JSON ajouter dans formulaire.html
        :return: Récupère l'id de l'oeuvre rajouter ou présent dans la base
        """
        test=Oeuvre.query.filter(Oeuvre.Titre==titre).filter(Oeuvre.Auteur==auteur). filter(Oeuvre.Langue==langue).filter(Oeuvre.Incipit==incipit).filter(Oeuvre.Explicit==excipit).filter(Oeuvre.Folios==folios).filter(Oeuvre.URL==lien_site).filter(Oeuvre.IIIF==iiif).scalar()

        if test is None:
            ajout_oeuvre=Oeuvre(Titre=titre,Auteur=auteur,Langue=langue,Incipit=incipit,Explicit=excipit,URL=lien_site,IIIF=iiif,Folios=folios)
            db.session.add(ajout_oeuvre)
            db.session.commit()
            recup=Oeuvre.query.filter(Oeuvre.Titre == titre).filter(Oeuvre.Auteur == auteur).filter(
                Oeuvre.Langue == langue).filter(Oeuvre.Incipit == incipit).filter(Oeuvre.Explicit == excipit).filter(
                Oeuvre.Folios == folios).filter(Oeuvre.URL == lien_site).filter(Oeuvre.IIIF==iiif).first()
            return recup.IdOeuvre
        else:
            recup = Oeuvre.query.filter(Oeuvre.Titre == titre).filter(Oeuvre.Auteur == auteur).filter(
                Oeuvre.Langue == langue).filter(Oeuvre.Incipit == incipit).filter(Oeuvre.Explicit == excipit).filter(
                Oeuvre.Folios == folios).filter(Oeuvre.URL== lien_site).filter(Oeuvre.IIIF==iiif).first()
            return recup.IdOeuvre



class Saint(db.Model):
    __tablename__ = "saint"
    IdSaint = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_saint=db.Column(db.Text)
    Biographie=db.Column(db.Text)
    oeuvres = db.relationship('Oeuvre', secondary=Jointure_Saint_Oeuvre, backref='saints')
    @staticmethod
    def ajouter(nom_saint):
        """ Ajout du saint dans la base de données

        :param nom_saint: nom du saint et de la sainte
        :return: Récupère l'id du saint rajouté ou déjà présent dans la base
        """
        all_Nom_saint=Saint.query.with_entities(Saint.Nom_saint)
        all_Nom_saint=[nsaint[0]for nsaint in all_Nom_saint.all()]

        if nom_saint not in all_Nom_saint:
            noms=Saint(Nom_saint=nom_saint)
            db.session.add(noms)
            db.session.commit()
            recup=Saint.query.filter(Saint.Nom_saint==nom_saint).first()
            return recup.IdSaint
        else:
            recup = Saint.query.filter(Saint.Nom_saint == nom_saint).first()
            return recup.IdSaint

    @staticmethod
    def association_Oeuvre_Saint(saintid,oeuvreid):
        """Associer les lignes de la table Saint et de la table Oeuvre

        :param saintid: identifiant du saint qu'on veut relier avec une Oeuvre
        :param oeuvreid: identifiant de l'oeuvre qu'on relier avec un saint

        """
        saintassoc=Saint.query.filter(Saint.IdSaint==saintid).first()
        oeuvreassoc=Oeuvre.query.filter(Oeuvre.IdOeuvre==oeuvreid).first()

        oeuvreassoc.saint.append(saintassoc)

        db.session.add(oeuvreassoc)
        db.session.commit()


class Institution(db.Model):
    __tablename__="institution"
    IdInstitution=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_institution=db.Column(db.Text)
    Localisation_IdLocalisation= db.Column(db.Integer, db.ForeignKey('localisation.IdLocalisation'))
    ManuscritInstitution=db.relationship('Manuscrit',backref="institution")
    LocalisationInstitution=db.relationship('Localisation',backref="institution")

    @staticmethod
    def ajouter(nominstitution, localisation):
        test=Institution.query.filter(Institution.Nom_institution==nominstitution,Institution.Localisation_IdLocalisation==localisation).scalar()
        if test is None:
            ajout_institution=Institution(Nom_institution=nominstitution,Localisation_IdLocalisation=localisation)
            db.session.add(ajout_institution)
            db.session.commit()
            recup=Institution.query.filter(Institution.Nom_institution==nominstitution,Institution.Localisation_IdLocalisation==localisation).first()
            return recup.IdInstitution
        else:
            recup=Institution.query.filter(Institution.Nom_institution==nominstitution,Institution.Localisation_IdLocalisation==localisation).first()
            return recup.IdInstitution




class Manuscrit(db.Model):
    __tablename__="manuscrit"
    IdManuscrit=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Cote=db.Column(db.Text)
    Titre=db.Column(db.Text)
    Nb_feuillets=db.Column(db.Integer)
    Provenance=db.Column(db.Text)
    Support=db.Column(db.Text)
    Hauteur=db.Column(db.Text)
    Largeur=db.Column(db.Text)
    Institution_IdInstitution= db.Column(db.Integer, db.ForeignKey('institution.IdInstitution'))
    realisations = db.relationship('Realisation', secondary=Jointure_Manuscrit_Realisation, backref='manuscrit')
    InstitutionManuscrit=db.relationship('Institution',backref="manuscrit")

    @staticmethod
    def ajouter(cote,titre,nb_feuillets,provenance,support,hauteur,largeur,institution_idinstitution):
        test=Manuscrit.query.filter(Manuscrit.Cote==cote).filter(Manuscrit.Titre==titre).filter(Manuscrit.Nb_feuillets==nb_feuillets).filter(Manuscrit.Provenance==provenance).filter(Manuscrit.Support==support).filter(Manuscrit.Hauteur==hauteur).filter(Manuscrit.Largeur==largeur).filter(Manuscrit.Institution_IdInstitution==institution_idinstitution).scalar()

        if test is None:
            ajout_manuscrit=Manuscrit(Cote=cote,Titre=titre,Nb_feuillets=nb_feuillets,Provenance=provenance,Support=support,Hauteur=hauteur,Largeur=largeur,Institution_IdInstitution=institution_idinstitution)
            db.session.add(ajout_manuscrit)
            db.session.commit()
            recup=Manuscrit.query.filter(Manuscrit.Cote==cote).filter(Manuscrit.Titre==titre).filter(Manuscrit.Nb_feuillets==nb_feuillets).filter(Manuscrit.Provenance==provenance).filter(Manuscrit.Support==support).filter(Manuscrit.Hauteur==hauteur).filter(Manuscrit.Largeur==largeur).filter(Manuscrit.Institution_IdInstitution==institution_idinstitution).first()
            return recup.IdManuscrit
        else:
            recup = Manuscrit.query.filter(Manuscrit.Cote == cote).filter(Manuscrit.Titre == titre).filter(
                Manuscrit.Nb_feuillets == nb_feuillets).filter(Manuscrit.Provenance == provenance).filter(
                Manuscrit.Support == support).filter(Manuscrit.Hauteur == hauteur).filter(
                Manuscrit.Largeur == largeur).filter(Manuscrit.Institution_IdInstitution==institution_idinstitution).first()
            return recup.IdManuscrit
    @staticmethod
    def association_manuscrit_realisation(manuscritid,realisationid):
        realisationassoc=Realisation.query.filter(Realisation.IdRealisation==realisationid).first()
        manuscritassoc=Manuscrit.query.filter(Manuscrit.IdManuscrit==manuscritid).first()

        manuscritassoc.manuscrits.append(realisationassoc)
        db.session.add(manuscritassoc)
        db.session.commit()




class Realisation (db.Model):
    __tablename__="realisation"
    IdRealisation=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Date_production=db.Column(db.Text)
    Lieu_production=db.Column(db.Text)
    Copiste=db.Column(db.Text)
    oeuvres = db.relationship('Oeuvre', secondary=Jointure_Oeuvre_Realisation, backref='realisation')
    manuscrits=db.relationship('Manuscrit', secondary=Jointure_Manuscrit_Realisation, backref='realisation')

    @staticmethod
    def ajouter(date_production,lieu_production,copiste):

        test=Realisation.query.filter(Realisation.Date_production==date_production).filter(Realisation.Lieu_production==lieu_production).filter(Realisation.Copiste==copiste).scalar()

        if test is None:
            ajout_realisation=Realisation(Date_production=date_production,Lieu_production=lieu_production,Copiste=copiste)
            db.session.add(ajout_realisation)
            db.session.commit()
            recup=Realisation.query.filter(Realisation.Date_production==date_production).filter(Realisation.Lieu_production==lieu_production).filter(Realisation.Copiste==copiste).first()
            return recup.IdRealisation
        else:
            recup = Realisation.query.filter(Realisation.Date_production == date_production).filter(
                Realisation.Lieu_production == lieu_production).filter(Realisation.Copiste == copiste).first()
            return recup.IdRealisation

    @staticmethod
    def association_Oeuvre_Realisation(oeuvreid,realisationid):
        """
        Fonction qui doit permettre de faire la jointure entre les deux tables
        :param oeuvreid: id de l'oeuvre
        :param realisationid: id de la réalisation

        """
        realisationassoc=Realisation.query.filter(Realisation.IdRealisation==realisationid).first()
        oeuvreassoc=Oeuvre.query.filter(Oeuvre.IdOeuvre==oeuvreid).first()

        realisationassoc.oeuvres.append(oeuvreassoc)
        db.session.add(realisationassoc)
        db.session.commit()

class Images_numeriques (db.Model):
    _tablename__="images_numeriques"
    IdImage=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Lien_ark_gallica=db.Column(db.TEXT)
    Legende_image=db.Column(db.TEXT)
    IdOeuvre=db.Column(db.Integer, db.ForeignKey('Oeuvre.IdOeuvre'))

class Localisation (db.Model):
    __tablename="localisation"
    IdLocalisation=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Ville=db.Column(db.TEXT)
    InstitutionLocalisation = db.relationship('Institution', backref="localisation")

    @staticmethod
    def ajouter(localisation):
        test=Localisation.query.filter(Localisation.Ville==localisation).scalar()
        if test is None:
            ajout_localisation=Localisation(Ville=localisation)
            db.session.add(ajout_localisation)
            db.session.commit()
            recup=Localisation.query.filter(Localisation.Ville==localisation).first()
            return recup.IdLocalisation
        else:
            recup=Localisation.query.filter(Localisation.Ville==localisation).first()
            return recup.IdLocalisation


def controle(saint, titre, langue, incipit, explicit, Folio, Date_production, Lieu_production,
                Cote, Nb_feuillets,  Support, Hauteur, Largeur, Institution,Localisation,IIIF):
    """
    Controle la présence des mentions obligatoires pour l'ajout de formulaire
    :param saint: texte d'entrée de Saint
    :param titre: texte d'entrée de Titre
    :param langue: texte d'entrée dans langue
    :param incipit: Texte d'entrée dans incipit
    :param explicit: texte d'entrée dans explicit
    :param Folio: texte d'entrée dans Folio
    :param Date_production: texte d'entrée dans Date production
    :param Lieu_production: texte d'entrée dans la page formulaire dans Lieu production
    :param Cote: texte d'entrée dans la page formulaire dans Cote
    :param Nb_feuillets: texte d'entrée dans la page formulaire dans Nb_feuillets
    :param Support: texte d'entrée dans la page formulaire dans Support
    :param Hauteur: texte d'entrée dans la page formulaire dans Hauteur
    :param Largeur: texte d'entrée dans la page formulaire dans Largeur
    :param Institution: texte d'entrée dans la page formulaire dans Institution
    :param Institution: texte d'entrée dans la page formulaire de Localisation
    :return: erreurs qui contient les différentes cases vides précisées.
    """
    erreurs = []
    if not saint:
        erreurs.append("Il manque le nom du Saint ")
    if not titre:
        erreurs.append("Il manque le titre de l'oeuvre ")
    if not langue:
        erreurs.append("Il manque la langue ")
    if not incipit:
        erreurs.append("Il manque l'incipit ")
    if not explicit:
        erreurs.append("Il manque l'explicit ")
    if not Folio:
        erreurs.append("Il manque les folios ")
    if not Date_production:
        erreurs.append("Il manque la date de production ")
    if not Lieu_production:
        erreurs.append("Il manque le lieu de production ")
    if not Cote:
        erreurs.append("Il manque la cote ")
    if not Nb_feuillets:
        erreurs.append("Il manque le nombre de feuillet ")
    if not Support:
        erreurs.append("Il manque le support du manuscrit ")
    if not Hauteur:
        erreurs.append("Il manque la hauteur du mansucrit ")
    if not Largeur:
        erreurs.append("Il manque la largeur du manuscrit")
    if not Institution:
        erreurs.append("Il manque l'institution")
    if not Localisation:
        erreurs.append("Il manque la localisation")
    if not IIIF:
        erreurs.append("Il manque le manifeste IIIF")
    if len(erreurs) > 0:
        return False, erreurs
    if len(erreurs)==0:
        return True,erreurs
