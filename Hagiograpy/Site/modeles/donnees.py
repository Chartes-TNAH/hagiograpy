from .. app import db

Jointure_Saint_Oeuvre= db.Table('Jointure_Saint_Oeuvre',
                          db.Column('Oeuvre_IdOeuvre', db.Integer, db.ForeignKey('oeuvre.IdOeuvre'), primary_key=True),
                          db.Column('Saint_IdSaint', db.Integer, db.ForeignKey('saint.IdSaint'),primary_key=True))

Jointure_Manuscrit_Realisation=db.Table('Jointure_Manuscrit_Realisation',
                                        db.Column('Manuscrit_IdManuscrit',db.Integer, db.ForeignKey('Manuscrit.IdManuscrit'),primary_key=True),
                                        db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('Realisation.IdRealisation'),primary_key=True))
Jointure_Oeuvre_Realisation=db.Table('Jointure_Oeuvre_Realisation',
                                     db.Column('Realisation_IdRealisation',db.Integer,db.ForeignKey('Realisation.IdRealisation'),primary_key=True),
                                     db.Column('Oeuvre_IdOeuvre',db.Integer,db.ForeignKey('Oeuvre.IdOeuvre'),primary_key=True))
# On crée notre modèle
class Oeuvre(db.Model):
#Création de la classe centrale oeuvre
    __tablename__="oeuvre"
    IdOeuvre = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Titre = db.Column(db.Text)
    Auteur=db.Column(db.Text)
    Langue=db.Column(db.Text)
    Incipit=db.Column(db.Text)
    Excipit=db.Column(db.Text)
    Lien_site = db.Column(db.Text)
    Folios=db.Column(db.Text)
    saints = db.relationship('Saint', secondary=Jointure_Saint_Oeuvre, backref='oeuvres')

class Saint(db.Model):
    __tablename__ = "saint"
    IdSaint = db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_saint=db.Column(db.Text)
    Biographie=db.Column(db.Text)
    oeuvre = db.relationship('Oeuvre', secondary=Jointure_Saint_Oeuvre, backref='saint')



class Institution(db.Model):
    __tablename__="institution"
    IdInstitution=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Nom_institution=db.Column(db.Text)
    Localisation_IdLocalisation= db.Column(db.Integer, db.ForeignKey('Localisation.IdLocalisation'))

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
    Institution_IdInstitution= db.Column(db.Integer, db.ForeignKey('Localisation.IdLocalisation'))

class Realisation (db.Model):
    __tablename__="realisation"
    IdRealisation=db.Column(db.Integer, unique=True, primary_key=True, autoincrement=True)
    Date_production=db.Column(db.Text)
    Lieu_production=db.Column(db.Text)
    Copiste=db.Column(db.Text)

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

"""    def ajouter(saint, titre, auteur, langue, incipit, explicit, Lien_site, Folio, Date_production, Lieu_production,
                Copiste, Cote, Titre, Nb_feuillets, Provenance, Support, Hauteur, Largeur, Institution):"""


def controle(saint, titre, langue, incipit, explicit, Folio, Date_production, Lieu_production,
                Cote, Nb_feuillets,  Support, Hauteur, Largeur, Institution):
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
        erreurs.append("Il manque la largeur du manuscri t")
    if not Institution:
        erreurs.append("Il manque l'institution")
    if len(erreurs) > 0:
        return False, erreurs