# HagiograPY
Ce repository contient l'ensemble des éléments nécessaires à la création d'un catalogue de vie de saints. Cette application web est développée dans le cadre du cours Python du Master 2 "Technologies numériques appliquées à l'histoire" de l'École nationale des chartes, selon les consignes suivantes :

## Consignes 
> En groupe de 3/4 personnes maximum, vous choisirez un sujet au choix parmi la liste proposée. Des limitations différentes peuvent être indiquées pour certains projets. Rendu le 1er avril 2019.  
>  
> **Consignes globales**  
> - Les rendus se feront via git et github en particulier sur des dépôts de https://github.com/Chartes-TNAH.
> - Une documentation pour la mise en place du projet sera mise à disposition. Le README de ce dépôt peut être utilisé comme référence.
> - Des données de tests seront fournies afin d'utiliser l'application.
> - (Optionnel) Des tests unitaires seront fournis. 
>
> **Consignes pour le projet HagiograPY**
> - Navigation à partir de saint, manuscrits ou texte suivant un modèle de données Saint <-n-n-> Oeuvre <-n-n-> Réalisation <-n-n-> Manuscrit. Une table auteur pourra être ajoutée en lien avec Oeuvre).
> - Il doit être possible d'ajouter des données pour chacune de ces tables via un formulaire et donc de lier des données entre elles.
> - Il doit être possible de chercher des données via leurs métadonnées
> - Il faut pouvoir avoir un visualiseur IIIF si un manifeste est fourni au niveau de la réalisation ou du manuscrit, ou d'avoir des liens vers le texte en ligne s’il est disponible.
> - Consignes habituelles sur la documentation
> - Bonus : - Mise en ligne sur Heroku
>           - Tests

## Description du projet
HagiograPY est une application web permettant de donner accès à de la littérature hagiographique médiévale.

HagiograPY permet ainsi de consulter des Vies de saints par :
    nom de saint ;
    titre d'oeuvre ;
    auteur de l'oeuvre.

## Comment fonctionne HagiograPy
Les différentes pages s'appuient sur les langages HTML, CSS, JavaScript et Python 3, ainsi que sur une base de données MySQL.

## Comment installer HagiograPy
Télécharger le dossier GitHub.
Nous recommandons la création d'un environnement virtuel d'après le fichier requirements.txt.
Ouvrir le premier dossier "hagiograpy" et lancer le fichier run.py.

## Contributeurs
- Clément Andrieux
- Corentin Faye
- Olivier Jacquot
- Pierre-Louis Pinault