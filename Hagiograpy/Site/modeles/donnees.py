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
    def ajouter(titre, auteur, langue, incipit, excipit, folios, lien_site,iiif):
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
            ajout_oeuvre=Oeuvre(Titre=titre,Auteur=auteur,Langue=langue,Incipit=incipit,Explicit=excipit,Folios=folios,URL=lien_site,IIIF=iiif)
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
    def ajouter(nom_saint, BioSaint):
        """ Ajout du saint dans la base de données
        :param nom_saint: nom du saint et de la sainte
        :return: Récupère l'id du saint rajouté ou déjà présent dans la base
        """


        test= Saint.query.filter(Saint.Nom_saint==nom_saint).filter(Saint.Biographie==BioSaint).scalar()

        if test is None:
            noms=Saint(Nom_saint=nom_saint,Biographie=BioSaint)
            db.session.add(noms)
            db.session.commit()
            recup=Saint.query.filter(Saint.Nom_saint==nom_saint).filter(Saint.Biographie==BioSaint).first()
            return recup.IdSaint
        else:
            recup = Saint.query.filter(Saint.Nom_saint == nom_saint).filter(Saint.Biographie==BioSaint).first()
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
        """

        :param nominstitution: renvoie le nom de l'institution
        :param localisation: Id de la localisation
        :return: renvoie l'id de l'institution pour faire des ajouts
        """
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
        """

        :param cote: Valeur cote d'un formulaire d'ajout
        :param titre: Valeur titre d'un formulaire d'ajout
        :param nb_feuillets: Valeur nombre de feuillet d'un formulaire d'ajout
        :param provenance: Valeur provenance d'un formulaire d'ajout
        :param support: Valeur provenance d'un formulaire d'ajout
        :param hauteur: Valeur hauteur d'un formulaire d'ajout
        :param largeur: Valeur largeur d'un formulaire d'ajout
        :param institution_idinstitution: l'Id de l'institution d'un formulaire d'ajout
        :return: return l'id du manuscrit ajouter ou correspondant dans la base
        """

        #Test si les valeurs permettent de trouver quelques choses dans la base
        test=Manuscrit.query.filter(Manuscrit.Cote==cote).filter(Manuscrit.Titre==titre).filter(Manuscrit.Nb_feuillets==nb_feuillets).filter(Manuscrit.Provenance==provenance).filter(Manuscrit.Support==support).filter(Manuscrit.Hauteur==hauteur).filter(Manuscrit.Largeur==largeur).filter(Manuscrit.Institution_IdInstitution==institution_idinstitution).scalar()

        #Si le test est échoué on ajoute les nouvelles entrées dans la base mais dans les deux cas on renvoie les id pour pouvoir faire les associations entre différentes tables
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
        """

        :param manuscritid: récupération de l'id manuscrit
        :param realisationid: récupération de l'id réalisation
        :return:
        """
        realisationassoc=Realisation.query.filter(Realisation.IdRealisation==realisationid).first()
        manuscritassoc=Manuscrit.query.filter(Manuscrit.IdManuscrit==manuscritid).first()
        #mise en place de l'association pour la rajouter dans la base de données au niveau de la jointure manuscrit réalisation
        manuscritassoc.realisations.append(realisationassoc)
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
        """

        :param date_production: recupère la date des formulaires
        :param lieu_production: recupère le lieu de production
        :param copiste: récupère le copiste
        :return: return l'id de la Realisation ajouter ou correspondant dans la base
        """
        # Test si les valeurs permettent de trouver quelques choses dans la base
        test=Realisation.query.filter(Realisation.Date_production==date_production).filter(Realisation.Lieu_production==lieu_production).filter(Realisation.Copiste==copiste).scalar()

        # Si le test est échoué on ajoute les nouvelles entrées dans la base mais dans les deux cas on renvoie les id pour pouvoir faire les associations entre différentes tables
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
        """

        :param localisation:
        :return: return l'id du localisation ajouter ou correspondant dans la base
        """
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

