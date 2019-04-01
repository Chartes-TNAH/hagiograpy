# HagriograPY : le site des hagiographies développé en Python

## Le projet 

* Description du projet

HagiograPY est une application web permettant de donner accès à de la littérature hagiographique médiévale.

Ce site recense des <em>Vies de saints</em> issues de recueils hagiographiques. Pour chaque saint recensé, un lien donne accès au manuscrit contenant la Vie de saint ainsi que vers le <a href="https://developer.mozilla.org/fr/docs/Mozilla/Add-ons/WebExtensions/manifest.json">manifeste JSON</a> correspondant.<br/>Le visualiseur <a href="https://openseadragon.github.io/">Openseadragon</a> permet de consulter l'image numérique de la page concernée en haute résolution grâce à l'<a href="https://iiif.io/">International Image Interoperability Framework (IIIF).

HagiograPY permet ainsi de consulter des Vies de saints grâce à une recherche simple et une recherche avancée. Le site donne accès à des index :

- des vies de saints issues de recueils hagiogaphiques ;
- des biographies des saints considérés ;
- des manuscrits contenant les hagiographies ;
- des institutions conservant les manuscrits.

Les internautes sont invités à enrichir la base en ajoutant des œuvres grâce à un formulaire dédié.
Cependant, l'enrichissement de la base nécessite une inscription préalable pour laquelle vous sont demandés :
- un login ;
- votre nom ;
- votre email ;
- un mot de passe.

* À propos

Cette application web est développée dans le cadre du Master 2 <em>Technologies numériques appliquées à l'histoire</em> de l'École nationale des chartes.

* Comment fonctionne HagiograPy ?

Les différentes pages s'appuient sur les langages HTML, CSS, JavaScript et Python 3, ainsi que sur une base de données MySQL.

* Comment installer HagiograPy ?

Télécharger le dossier GitHub. Nous recommandons la création d'un environnement virtuel d'après le fichier requirements.txt. Ouvrir le premier dossier "hagiograpy" et lancer le fichier run.py.

* Contributeurs

- Clément Andrieux
- Corentin Faye
- Olivier Jacquot
- Pierre-Louis Pinault

## Les étapes de réalisation du projet

### La base de donnée

Cette application web s'adosse à une base de donnée pour laquelle il a été nécessaire de concevoir un modèle conceptuel de données avec le logiciel MySQL Workbench avant de réaliser un modèle relationnel de données. La base de données a ensuite été créée en SQlite avec le logiciel DB Browser.
Afin de donner à voir le fonctionnement du site, il a été nécessaire de peupler la base par des données réelles issues des travaux menées dans le cadres des enseignements du langage XML-TEI et notamment l'encodage de la Cantilène de Sainte Eulalie et du manuscrit Français-412 de la Bibliothèque nationale de France.

### L'application web

#### L'arborescence

L'arborescence du site était induite par les consignes concernant la navigation et les possibilités de recherche qu'il falait mettre en oeuvre. En effet, cela impliquait de créer des formulaires de recherche (simple et avancée) et des index pour accéder aux divers types de contenus. Cela a donc conduit l'équipe à créer des gabarits de pages d'index, et des pages terminales pour les différents niveaux de granularité à afficher.

#### Le graphisme

Pour le graphisme du site le parti pris a été d'employer les outils du framework Bootstrap. Un choix de couleurs sobres a été mis en oeuvre et quelques illustrations ajoutées pour donner une idée du thème du site. 

#### Le visualiseur

Sachant qu'un visualiseur IIIF était demandé pour exploiter des fichiers JSON, divers tests non concluants ont été menés avec leaflet avant d'opter pour la librairie Openseadragon. Le code garde en commentaire une façon frustre d'afficher des images mais qui permet de fournir les balises alt et title requises par les règle d'accessibilité.

#### Les formulaires de recherche

La mise en place des formulaires de recherche (simple et avancée) a nécessité une importante réflexion pour l'alimentation du fichier donnees.py et plus encore pour le fichier des routes.py.
L'objectif était d'exploiter toutes les tables, tous les champs et toutes les jointures de la base de données par le biais du langage de requête offert par SQLAlchemy.

### Modalités du développement

* Utilisation de PyCharm

L'application a été développée au sein de l'environnement de développement intégré pour le langage Python <em>PyCharm</em> dans son édition communautaire.

* Utilisation de Github

Le chantiers de développement ont été répartis entre les membres de l'équipe qui ont créé des branches dédiées au sein de leur dossier git local, régulièrement poussé sur le compte GITHUB du projet : https://github.com/Chartes-TNAH/hagiograpy. L'équipe n'a pas été exempte de devoir gérer des conflits. Dans la livraison finale, les différentes branches ayant fait l'objet d'une fusion ont été laissées dans le dépôt et non pas supprimées. Dans la phase intensive de développement, il a parfois été nécessaire de remiser des modifications, de désindexer, ou de revenir à des états antérieurs pour régler les conflits. Le site de GITHUB a été exploité pour signaler des problèmes (issues), les attribuer à l'un ou l'autre membre en ajoutant des labels. De même des "pull request" ont été ouvertes, commentées et fermées après fusion.
Pour la livrasion finale du projet, un fichier `.gitignore` a été produit grâce à l'utilitaire https://www.gitignore.io (pour PyCharm, Python, Flask).

* Déploiement sur Heroku

Afin de publier le site en ligne et ne pas rester sur un serveur local (localhost), plusieurs tentatives ont été menées pour transférer le site sur la plateforme Heroku. Malheureusement, il appert que la plateforme, même si elle peut stocker des branches d'un dépôt GIT, nécessite une branche "maître". Cela a impliqué de devoir configurer le site directement sur les données de la branche "master" de notre dépôt. 
Malgré la mise en place de tous les pré-requis fournis pas la documentation de la plateforme (création des fichiers Procfile, runtime, mise à jour du fichier requirements, etc.), il n'a pas été possible de mener à bien cette tâche. 
Grâce à la commande `heroku logs --tail` saisie dans le terminal de nombreuses erreurs ont été patiemment corrigées l'une après l'autre, comme par exemple celle concernant une version trop avancée de python et non prise en charge par Heroku, ou encore à l'absence d'indication du processus web dans le fichier Procfile (`No web processes running`), etc.
S'il a été possible de créer un espace pour acceuillir le site : https://hagiograpy-api-heroku.herokuapp.com/, qu'il a fallu de nombreux essais et de déplacements de fichiers dans notre arborescense, au final nous n'avons pu résoudre l'erreur du nom de l'app dans le fichier Procfile : ModuleNotFoundError: No module named 'app' dans la ligne : gunicorn app:app. Tous les essais pour indiquer le nom figurant dans les fichiers app, constantes, etc. ont avortés.

* Mise en place de tests

Le temps pris à répondre aux exigences émises à trois jours de la date de livraison de l'application et à tenter la publication en ligne a empêché de mettre en place des tests Travis (https://travis-ci.org/).

## Conclusion

Cet exercice a permis de mettre en pratique les enseignements du semestre consacré au langage de développement Python et au framework Flask, permettant à certais membres du groupe de mieux appréhender le développement d'une application web ex nihilo, sans le recours à des outils de gestion de contenu. Il reste que la boîte à outils SQLAlchemy sur laquelle se fonde l'application est restée complexe pour nombre des membres du groupe.