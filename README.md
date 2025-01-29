<p align="center">
  <img src="./Images/logo.lpeg" width="300">
</p>
<h1 align="center">Projet 2 : Système de recommandation de films</h1>

## 📜 Contexte  

Vous êtes un Data Analyst freelance. Un cinéma en perte de vitesse situé dans la Creuse vous contacte. Il a décidé de passer le cap du digital en créant un site Internet taillé pour les locaux.
Pour aller encore plus loin, il vous demande de créer un moteur de recommandations de films qui à terme, enverra des notifications aux clients via Internet.
Pour l’instant, aucun client n’a renseigné ses préférences, vous êtes dans une situation de cold start. Mais heureusement, le client vous donne une base de données de films basée sur la plateforme IMDb.
Commencez par une étude de marché sur la consommation de cinéma dans la région de la Creuse, afin de mieux comprendre les attentes et les préférences du public local. Cette étape préliminaire vous permettra de définir une orientation adaptée pour la suite de l’analyse de votre base de données.
Après cette étude, réalisez une analyse approfondie de votre base de données pour identifier des tendances et caractéristiques spécifiques. 

---

## 🎯 Objectif  

Cette analyse devrait inclure : **l’identification des acteurs les plus présents et les périodes associées**, **l’évolution de la durée moyenne des films au fil des années**, **la comparaison entre les acteurs présents au cinéma et dans les séries**, **l’âge moyen des acteurs**, ainsi que **les films les mieux notés et les caractéristiques qu’ils partagent.**
Sur la base des informations récoltées, vous pourrez affiner votre programmation en vous spécialisant par exemple sur les films des années 90 ou les genres d’action et d’aventure, afin de mieux répondre aux attentes du public identifié lors de l’étude de marché.
Après cette étape analytique, sur la fin du projet, vous utiliserez des algorithmes de machine learning pour recommander des films en fonction de films qui ont été appréciés par le spectateur.
Le client vous fournit également une base de données complémentaires venant de TMDB, contenant des données sur les pays des boîtes de production, le budget, les recettes et également un chemin vers les posters des films. 
Il vous est demandé de récupérer les images des films pour les afficher dans votre interface de recommandation.
Attention ! L’objectif n’est pas de diffuser dans le cinéma les films recommandés. L’objectif final est d’avoir une application avec d’une part des KPI et d’autre part le système de recommandation avec une zone de saisie de nom de film pour l’utilisateur. 
Cette application sera mise à disposition des clients du cinéma afin de leur proposer un service supplémentaire, en ligne, en plus du cinéma classique. 



---

## 📂 Contenu  

Ressources

Les données sont disponibles sur le site IMDb, réparties en plusieurs tables (films, acteurs, réalisateurs, notes, etc.).
1. [Documentation des colonnes et tables](https://developer.imdb.com/non-commercial-datasets/)
2. [Datasets IMDb](https://datasets.imdbws.com/)
3. [Dataset complémentaire TMDB](https://drive.google.com/file/d/1VB5_gl1fnyBDzcIOXZ5vUSbCY68VZN1v/view)


---

## 🛠️ Méthodologie  

1. [Analyse et Prétraitement des Données](./docs/recherche/notebook.ipynb)  
2. [Définition des KPI](./docs/recherche/kpis.md)  
3. [Développement d'un tableau de bord](./livrables/BC_MPR.pbix)
4. [Mise en place d'un PowerPoint de présentation](./livrables/BC_MPR.pptx)

---

## 🔢 Description du jeu de données  

- ***8048*** : Nombre de clients dans le jeu de données  
- **Description des colonnes** :  

  - **Order ID** : Identifiant unique de chaque commande  
  - **Order Date** : Date de la commande  
  - **Customer Name** : Nom du client  
  - **Country** : Pays du client avec la précision suivante :  
  - **State** : État/province  
  - **City** : Ville  
  - **Region** : Région  
  - **Segment** : Classification du client :  
    - *Home Office* : Ce segment correspond à des auto entrepreneurs ou à de petites entreprises travaillant depuis chez eux.  
    - *Consumer* : Ce segment regroupe des clients individuels achetant pour un usage personnel.  
    - *Corporate* : Ce segment englobe les entreprises ou les grandes organisations passant des commandes en gros.  
  - **Ship Mode** : Mode de livraison utilisé pour la commande  
  - **Category** : Catégorie générale du produit avec la précision suivante :  
  - **Sub-Category** : Sous-catégorie du produit  
  - **Product Name** : Nom du produit  
  - **Discount** : Valeur de la remise en $  
  - **Sales** : Revenu total généré par la transaction, avant toute remise ou marge bénéficiaire.  
  - **Profit** : Montant de l'argent gagné sur la vente  
  - **Quantity** : Quantité de produit dans la commande  
  - **Feedback?** : (Booléen) Le client a-t-il laissé un retour ?  



## 🏗️ Structure du dépôt
```
BC_MARKET_RETAIL/
├── docs/                   # Contient les documents non livrables et images
│   ├── images/             # Toutes les images utilisées dans les livrables
│   ├── recherche/          # Notebook de nettoyage et exploration des données et réflexion sur les kpis
├── donnees/                # Contient les données brutes et transformées
│   ├── brutes/             # Données brutes (non modifiées)
│   ├── nettoyees/          # Données nettoyées et modifiées
├── livrables/              # Contient tout ce qui a été demandé et qu'il faudra rendre
│   ├── dashboard/          # Dashboard powerBI
│   ├── presentation/       # owerpoint de présentation
└── README.md               # Description du projet
```

## 🏁 Conclusion

- Il faut agir rapidement sur les marchés qui ont un discount moyen trop élevé qui engendrent de lourdes pertes pour l’entreprise.
- On peut voir que des pays qui apportent un fort CA ont des taux de discount assez bas. Une bonne stratégie serait de diminuer les remises des pays ou le bénéfice est négatif pour en apporter plus aux marchés qui sont déjà porteur pour les fidéliser  définitivement et aller chercher le chiffre chez eux car ce sont eux qui portent l’entreprise.
- Se focaliser sur les produits technologiques qui apportent le plus de chiffre pour des ventes beaucoup moins importantes permettra de gonfler le chiffre.
- On sait que l’entreprise reçoit beaucoup de feedback de la part de ses clients, lui permettant d’avoir des avis représentatifs sur leur expérience qui sont très importants à exploiter.


---

## 📜 Licence
- [**MIT**](./LICENSE)
