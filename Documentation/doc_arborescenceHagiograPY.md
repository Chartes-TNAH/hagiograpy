__Documentation de l'arborescence du projet HagiograPY__ :

```
Documenation    Documentation du site
–– doc_arborescenceHagiograPY.md
–– HagiograPY_ModeleRelationnel.mwb
–– Schéma base de donnée.png

README.md       Fichier Lisez-moi
requirements.txt Fichier des logiciels requis et leur version

Hagiograpy
–– db_HagiograPY   Base de données de HagiograPY, gérée avec le logiciel DB Browser (SGBD embarqué SQLite)
–– path.py
–– run.py		   Appel de l'application pour son lancement


Site/			Package application
–– __init__.py			Fichier initialisant le dossier en package
–– app.py			    Module principal de l'application (initialisation et configuration)             
–– constantes.py		Définition des constantes utilisées dans l'application
–– routes.py    		Définition des url et des fonctions définissant le contenu des pages associées utilisées dans l'application

–– modeles/		    	Fichiers relatif à la base de données
–––––– __init__.py		Fichier initialisant le dossier en package
–––––– donnees.py		Mise en place des classes de la base de données
–––––– utilisateurs.py	Mise en place de lasse User de la base de données + fonctionnalités de création et identification

–– static/		Fichiers statiques
–––––– css/				Fichiers css (bootstrap, font-awesome)
–––––– fonts/			Fichiers de police de caractères
–––––– img/				Fichiers images (banner, footer, etc.)
–––––– js/				Fichiers javascript (bootstrap, jquery, popper)
–––––– openseadragon/   Fichiers openseadragon (relatif au visualiseur IIIF implémenté) 
––––––––––– images      Fichiers images employés par openseadragon
––––––––––– scripts     FIchiers javascript employés par openseadragon

–– templates/			Templates des différentes pages de l'application
–––––– conteneur.html	Page avec les éléments de base
–––––– pages/			Pages html de HagiograpPY
––––––––––– a-propos.html
––––––––––– accueil.html
––––––––––– cgu.html
––––––––––– connexion.html
––––––––––– formulaire.html
––––––––––– inscription.html
––––––––––– recherche.html
––––––––––– vie.html
–––––– partials/			Blocs à intégrer aux pages html de HagiograPY
––––––––––– css.html		balise lien vers les fichiers bootstrap
––––––––––– metadata.html	balises <meta> détaillant les métadonnées
```
