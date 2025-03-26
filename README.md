<p align="center">
  <img src="./Images/alicine_logo.jpeg" width="300">
</p>
<h1 align="center">Projet : Système de recommandation de films</h1>

## 🎥 Contexte  

Vous êtes un **Data Analyst freelance**. Un cinéma en perte de vitesse situé dans la Creuse vous contacte. Il a décidé de passer le cap du digital en créant un **site Internet taillé pour les locaux**.

Pour aller encore plus loin, il vous demande de créer un **moteur de recommandations de films** qui à terme, enverra des notifications aux clients via Internet.
Pour l’instant, aucun client n’a renseigné ses préférences, vous êtes dans une **situation de cold start**. Mais heureusement, le client vous donne une **base de données de films basée sur la plateforme IMDb**.

Commencez par une **étude de marché sur la consommation de cinéma dans la région de la Creuse**, afin de mieux comprendre les attentes et les préférences du public local. Cette étape préliminaire vous permettra de définir une orientation adaptée pour la suite de l’analyse de votre base de données.

Après cette étude, réalisez une **analyse approfondie de votre base de données** pour identifier des tendances et caractéristiques spécifiques. 

---

## 🎯 Objectif  

Cette analyse devrait inclure : 
- **l’identification des acteurs les plus présents et les périodes associées**
- **l’évolution de la durée moyenne des films au fil des années**
- **la comparaison entre les acteurs présents au cinéma et dans les séries**
- **l’âge moyen des acteurs**
- **les films les mieux notés et les caractéristiques qu’ils partagent.**

Après cette étape analytique, sur la fin du projet, vous utiliserez des **algorithmes de machine learning pour recommander des films** en fonction de films qui ont été appréciés par le spectateur.

Le client vous fournit également une **base de données complémentaires venant de TMDB**, contenant des données sur les pays des boîtes de production, le budget, les recettes et également un chemin vers les posters des films. 
Il vous est demandé de **récupérer les images des films** pour les afficher dans votre interface de recommandation.
Attention ! L’objectif n’est pas de diffuser dans le cinéma les films recommandés. L’objectif final est d’avoir une **application avec d’une part des KPI et d’autre part le système de recommandation** avec une zone de saisie de nom de film pour l’utilisateur. 

Cette application sera mise à disposition des clients du cinéma afin de leur proposer un service supplémentaire, en ligne, en plus du cinéma classique. 

Ce projet constitue également une **première expérience avec GitHub**. Il permet de découvrir son utilisation tout en adoptant les bonnes pratiques de gestion de version et de collaboration.



---

## 📂 Contenu  

Ressources

Les données sont disponibles sur le site IMDb, réparties en plusieurs tables (films, acteurs, réalisateurs, notes, etc.).
1. [Datasets IMDb](https://datasets.imdbws.com/)
2. [Dataset complémentaire TMDB](https://drive.google.com/file/d/1VB5_gl1fnyBDzcIOXZ5vUSbCY68VZN1v/view)
3. [Documentation des colonnes et tables](https://developer.imdb.com/non-commercial-datasets/)


---

## 🛠️ Méthodologie  

1. [Analyse et Prétraitement des Données](./notebook/Premier_nettoyage.ipynb)  
2. [Traitement des données pour répondre aux KPI](./notebook/df_powerBI.ipynb)  
3. [Développement d'un tableau de bord](./Dashboard_Aliciné.pdf)
4. [Mise en place d'une application streamlit](./pages_streamlit_AliCine.pdf)
5. [Mise en ligne de l'application](https://alicine.streamlit.app/)
5. [Mise en place d'un PowerPoint de présentation](./Le cinéma dans la Creuse.pdf)

---



## 🏗️ Structure du dépôt
```
Alicine/
├── .streamlit/             # Contient le fichier config.toml qui contient le thème su streamlit
├── BD_streamlit/           # Les bases de données transformées utilisées dans le streamlit
├── images/                 # Contient toutes les images du projet
├── notebook/               # Contient les notebook de travail sur les différents nettoyages de données et de 
│                             mise en place du modèle de machine learning
├── visualisation/          # Les bases de données brutes et nettoyées avec explication des colonnes
├── .gitignore              # Les fichiers à ignorer dans github (notamment les bases de données brutes très lourdes)
├── Alicine.py              # Le script Python streamlit
├── requirements.txt        # Fichier requirements pour la mise en ligne
└── README.md               # Description du projet

```

## 🎬 Conclusion

Ce **projet de recommandation de films** marque une étape clé dans notre apprentissage, étant notre première expérience avec de **grandes bases de données**. Nous avons mené une étude approfondie du marché, réalisé un nettoyage de données à grande échelle, conçu un dashboard interactif, développé un modèle de machine learning et une application Streamlit, le tout regroupé dans notre **premier repository GitHub**.

Travailler en équipe de trois, avec des profils complémentaires, nous a permis d’exploiter nos forces respectives et d’optimiser notre collaboration. Cependant, **la compréhension du fonctionnement de GitHub n’a pas été immédiate**, et nous avons réalisé trop tard l'importance d’une bonne gestion des commits. Cela explique un **historique peu structuré**, mais cette expérience nous a offert une précieuse leçon pour nos futurs projets collaboratifs.

Ce projet fut une belle opportunité d’apprentissage, et **nous sommes fiers du chemin parcouru** ! 


---

## 📜 Licence
- [**MIT**](./LICENSE)
