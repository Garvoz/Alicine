import ast
import base64
import pandas as pd
import pickle
import requests
from sklearn.neighbors import NearestNeighbors
import streamlit as st
from streamlit_option_menu import option_menu
import warnings
warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=FutureWarning)

# マトリックス = "matrix" pour frimer pendant la démo


#Utilisation de toute la largeur de la page:
st.set_page_config( layout="wide", page_title = "AliCiné", page_icon= "./Images/Logo.jpeg")


#Import des 2 df et des listes en cache:
@st.cache_data
def load_final():
    df_final = pd.read_csv("./BD_streamlit/df_final.csv")
    df_final['Genres'] = df_final['Genres'].apply(ast.literal_eval)#Les listes se load en str, on les remets en liste direct à l'import
    df_final['Liste acteurs'] = df_final['Liste acteurs'].apply(ast.literal_eval)
    df_final['Réalisateurs'] = df_final['Réalisateurs'].apply(ast.literal_eval)
    return df_final

df_final = load_final()

@st.cache_data
def load_movies():# Movies correspon dau df filtré sur les colonnes du ML avec les données normalisées
    movies = pd.read_csv("./BD_streamlit/movies.csv")
    return movies

movies = load_movies()

@st.cache_data
def pickl():
    with open('./BD_streamlit/mes_listes.pkl', 'rb') as f: #Ces listes sont les élément uniques de chaque catégorie pour le menu déroulant des st.selectbox
        acteurs = pickle.load(f)
        reals = pickle.load(f)
        genres = pickle.load(f)
        decennie = pickle.load(f)
    return acteurs, reals, genres, decennie

acteurs, reals, genres, decennie = pickl()



#Fonctions pour récupérer les données des APIs en cache:
BASE_URL = 'https://api.themoviedb.org/3/'
API_KEY = '3bca9c26909e582a5584220844dc20e1'

# 1- Fonction qui permet de récupérer les films populaires à jour API TMDB:
@st.cache_data
def films_populaire():
    url = f'{BASE_URL}movie/popular?api_key={API_KEY}&language=fr-FR&page=1'
    response = requests.get(url)
    data = response.json()
    return data['results']

# 2- Fonction pour récupérer les détails d'un film grace à un ID depuis API TMDB:
@st.cache_data
def details_films(movie_id):
    url = f'{BASE_URL}movie/{movie_id}?api_key={API_KEY}&language=fr-FR'
    response = requests.get(url)
    return response.json()
  
# 3- Fonction qui permet de récupérer les bandes annonce grace à un ID depuis API TMDB:: 
@st.cache_data
def video_films(movie_id):
      url = f'{BASE_URL}movie/{movie_id}/videos?api_key={API_KEY}&language=fr-FR'
      response = requests.get(url)
      video = response.json()
      return video["results"]



#Définition du code Machine learning en cache:
@st.cache_resource
def mes_recommendations(movie_title, nb_films=5):
    
    features = movies.drop(columns=['ID','Titre','Langue Originale'])
    features['Décénnie'] *= 2.5
    features['Score de popularité'] *= 2
    features['Note moyenne'] *= 1.5
    features['Durée (minutes)'] *= 1

    knn = NearestNeighbors(n_neighbors=nb_films+1, metric='cosine')
    knn.fit(features)

    movie_index = movies[movies['Titre'] == movie_title].index[0]
    distances, indices = knn.kneighbors(features.iloc[movie_index].values.reshape(1, -1))
    recommended_movie_ids = movies.iloc[indices[0][1:]]['ID'].values

    french_movies = movies[movies['Langue Originale'] == 'fr']
    filtered_movies = french_movies[~french_movies['ID'].isin(recommended_movie_ids)]

    filtered_features = filtered_movies.drop(columns=[ 'ID','Titre','Langue Originale'])
    features['Décénnie'] *= 2.5
    features['Score de popularité'] *= 2
    features['Note moyenne'] *= 1.5
    features['Durée (minutes)'] *= 1

    knn_filtered = NearestNeighbors(n_neighbors=nb_films, metric='cosine')
    knn_filtered.fit(filtered_features)
    
    french_distances, french_indices = knn_filtered.kneighbors(features.iloc[movie_index].values.reshape(1, -1))
    recommended_french_movie_ids = filtered_movies.iloc[french_indices[0]]['ID'].values

    return {
        "Recommandations générales" : list(recommended_movie_ids),
        "Recommandations en français" : list(recommended_french_movie_ids)
    }

#Encode base64 de l'image de fond sidebar en cache:
def popcorn():
    with open('./Images/falling_popcorn.jpeg', "rb") as f2:
        encoded_image = base64.b64encode(f2.read()).decode()
    return encoded_image

# encoded_image = popcorn()

# Mise en place de la sidebar:
with st.sidebar:
    st.sidebar.image('./Images/alicine_logo.jpeg', use_container_width=True)
    
    # Vérification si l'image encodée existe
    
    st.markdown(
        """
        <style> 
        [data-testid="stSidebar"] > div:first-child {
            background-image: url('https://i.ibb.co/x29K7Nc/falling-popcorn.jpg');
            background-size: cover;
            background-position: center;
            height: 100%;
        }
        </style>
        """,
        unsafe_allow_html=True
    )
    #Mise en place de l'image de fond avec du css
    
    page = option_menu(menu_title=None, options = ["Accueil", "Mieux nous connaitre", "Recherche personnalisée", "Films à l'affiche",  "Statistiques"])#Menu déroulant pour la navigation
        
    st.sidebar.markdown(
        """
        <p style='background-color: #0E1117; color: white; padding: 10px; border-radius: 5px;'>
            Besoin de nous contacter? <br><br>
            contact@cine-creusois.com <br><br>
            +33 5 55 25 25 25 (prix d'un appel local) <br><br>
            Avenue d'auvergne, 23000 Gueret, France
        </p>
        """,
        unsafe_allow_html=True)#Section contact avec css pour fond noir
    # Pour avoir un lien cliquable : st.sidebar.markdown("[contact@cine-creusois.com](mailto:contact@cine-creusois.com)")

#Mise en place page d'accueil:
if page == "Accueil":
    st.markdown("<h1 style='text-align: center;'>Bienvenue dans l'univers AliCiné !</h1>", unsafe_allow_html=True)#Code HTML et CSS pour centrer un texte, sera utilisé souvent
    col1, col2, col3 = st.columns([2, 10, 2])#Code pour donner du poid à une colonne plus qu'aux autres
    with col2:
        st.image("./Images/accueil.jpeg",  use_container_width=True)
    st.subheader("Votre cinéma se modernise et entre dans l'ère numérique !") 
    st.write("""          
           Nous sommes heureux de vous offrir une sélection de films variée et de qualité, dans un cadre convivial et chaleureux. 
           """)
    st.write("""          
           Grâce à cette application, venez découvrir notre système de recommandation de films, 
           """)
    st.write("mais aussi les films à l'affiche et les statistiques intéressantes. ")
    st.write("Et surtout bonne navigation!")



#Mise en place de la page "mieux nous connaitre":
if page == "Mieux nous connaitre":
    
    col1, col2, col3 = st.columns([2, 10, 2])
    with col2:
        st.image("./Images/connaitre.jpg",  use_container_width=True)
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.subheader("Nos Missions:")
            st.write("""
                    - Diversité cinématographique : Nous vous proposons une programmation diversifiée, alliant cinéma francophone et anglophone ceci pour répondre aux besoin de tous nos spéctateurs.
                    - Accessibilité : des projections proposeées pour répondre à tous les gouts et tous les âges. Nous vous proposons des séances aux familles, aux jeunes et aux cinéphiles agéris (confirmés).
                    - Événements spéciaux : Nous organisons des avant-premières, des projections cultes. Et grâce à notre étroite collaboration avec 'Ecole et Cinéma' nous nous nous investissons dans la promotion des films Film Art et Essai et organisons aussi des 'Ciné-débats' et invitons des intervenants de qualité ")
                    """)
    with col2:
      st.subheader("Nos engagements:")
      st.write("""
                Le cinéma est bien plus qu'un divertissement, c'est un art qui rassemble, qui éveille les consciences et anime l'imagination. 
                Nous sommes engagés à proposer une programation riche et variée, ceci en respectant nos engagements qui nous animent:
                - Diversité culturelle : Nous nous engageons à offrir à nos spéctateurs une programmation éclectique qui couvre une large gamme de genre cinématographiques, tout en mettant en avant la production française, mais aussi des productions indépendantes.
                - Accessibilté à la culture pour tous :  Le cinéma doit être accessible à tous, quel que soit l'age, la situation sociale ou l'handicape:                   
                    - Nos salles ont été aménagées pour offrir l'accées pour les personnes à mobilité réduite,
                    - Nous organisons des séances avec sous titrage pour les malentendants, et en audiodescription pour les malvoyants
                    - Nous appliquons des tarifs réduits pour les jeunes, les familles (n'oubliez pas de présenter votre carte famille nombreuse lors ed votre passage à la caisse) et personnes à revenus modestes.
                - Soutien aux films indépendants : Nous soutenons activement les productions indépendantes et les jeunes talents. 
                Nous croyons en la richesse des films qui sont issus de petite production mais qui portent des messages forts et créatifs.
                Nous organisons des projections spéciales et des rencontres avec des réalisateurs. 
                Les jeunes cinéphiles participent également aux différents débats dans un espace conviviale est réservé dans ce sens.          
                """) 




#Gros de l'appli: mise en place de la recherche personnalisée:
if page == "Recherche personnalisée":
    st.markdown("<h1 style='text-align: center;'>Qu'est-ce qu'on regarde ce soir ?</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 10, 2])#Code pour donner du poid à une colonne plus qu'aux autres
    with col2:
        st.image("./Images/recherche.jpg",  use_container_width=True)

    # Moteur de recherche :
    st.markdown("<h2 style='text-align: center;'>Cherchez un film qui vous a plus, on vous recommandera un film similaire qui pourrait vous plaire !</h2>", unsafe_allow_html=True)
    search_titre = st.text_input('Recherche par titre :', '')
    col1, col2 = st.columns(2)
    with col1:
        search_acteur = st.selectbox('Recherche par acteur :', acteurs, index=None, placeholder="Choisissez un acteur...")
        search_real = st.selectbox('Recherche par réalisateur :', reals, index=None, placeholder="Choisissez un réalisateur...")
        search_fr = st.checkbox("Recherche dans  les films Français uniquement", key="fr")
    with col2:
        search_genre = st.selectbox('Recherche par genre', genres, index=None, placeholder="Choisissez un genre...")
        search_decennie = st.selectbox('Recherche par décénnie', decennie, index=None, placeholder="Choisissez une décénnie...")


  # Code qui filtre la base de données en fonction de la recherche : 
    df_reponse = df_final.copy()

    if search_titre != '':
         # La colonne 'Titres possibles' contient des listes mais avec read_csv ces listes sont traitées en string, on les laisse comme ça pour pouvoir faire un str.contains sur la recherche 
         df_reponse = df_reponse[df_reponse['Titres possibles'].str.contains(search_titre, case=False)]#case = False  ==> ignore la casse
    if search_acteur != None:
        df_reponse = df_reponse[df_reponse['Liste acteurs'].apply(lambda x: search_acteur in x)]
    if search_real != None:
        df_reponse = df_reponse[df_reponse['Réalisateurs'].apply(lambda x: search_real in x)] 
    if search_genre != None:
        df_reponse = df_reponse[df_reponse['Genres'].apply(lambda x: search_genre in x)]
    if search_decennie != None:
        df_reponse = df_reponse[df_reponse['Décénnie'] == search_decennie]
    if search_fr == True:
        df_reponse = df_reponse[df_reponse['Langue Originale'] == 'fr']

    #df_reponse ne contient plus que les films filtrés par les recherches, on ne prends que les 5 meilleures notes:
    df_reponse = df_reponse.sort_values(by=['Note moyenne', 'Nb de votes'] , ascending=False).head().reset_index()

    #Ajout d'une condition pour que la suite ne soit affichée que si une recherche à été entrée:
    if (search_titre != '') or (search_acteur != None) or (search_real != None) or (search_genre != None) or (search_decennie != None) or (search_fr == True):
        st.markdown("<h2 style='text-align: center;'>Films les mieux notés selon votre recherche :</h2>", unsafe_allow_html=True)
  
        # Affichage des résultats filtrés : 
        col21, col22, col23, col24, col25 = st.columns(5)

        with col21:
            if len(df_reponse) == 0:
                st.markdown('<p><b>Aucun film ne correspond à votre recherche !:</b> ')
            elif len(df_reponse) > 0:
                id1 = df_reponse.loc[0, 'ID']
                film_titre = df_reponse.loc[0, 'Titre']  # On récupère directement le titre
                infos = details_films(id1)
                videos = video_films(id1)             
        

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco1 = st.checkbox("**Voir les meilleurs films similaires recommandés:**", key=21)
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key = str(id1)):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reponse.loc[0, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reponse.loc[0, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")


        with col22:
            if len(df_reponse) > 1:
                id2 = df_reponse.loc[1, 'ID']
                film_titre = df_reponse.loc[1, 'Titre']  # On récupère directement le titre
                infos = details_films(id2)
                videos = video_films(id2)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco2 = st.checkbox("**Voir les meilleurs films similaires recommandés:**", key=22)

                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id2)):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reponse.loc[1, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reponse.loc[1, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")
                        
        with col23:
            if len(df_reponse) > 2:
                id3 = df_reponse.loc[2, 'ID']
                film_titre = df_reponse.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id3)
                videos = video_films(id3)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco3 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=23)

                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id3)):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reponse.loc[2, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reponse.loc[2, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")  

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")          

        with col24:
            if len(df_reponse) > 3:
                id4 = df_reponse.loc[3, 'ID']
                film_titre = df_reponse.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id4)
                videos = video_films(id4)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco4 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=24)

                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id4)):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reponse.loc[3, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reponse.loc[3, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

        with col25:
            if len(df_reponse) > 4:
                id5 = df_reponse.loc[4, 'ID']
                film_titre = df_reponse.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id5)
                videos = video_films(id5)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco5 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=25)
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id5)):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reponse.loc[4, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reponse.loc[4, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")
  
        dico = {}
        
        if len(df_reponse) > 0:
            if reco1 == True:
                titre_reco1 = df_reponse.loc[0, 'Titre']
                dico = mes_recommendations(titre_reco1)
            elif len(df_reponse) > 1:
                if reco2 == True:
                    titre_reco2 = df_reponse.loc[1, 'Titre']
                    dico = mes_recommendations(titre_reco2)
                elif len(df_reponse) > 2:
                    if reco3 == True:
                        titre_reco3 = df_reponse.loc[2, 'Titre']
                        dico = mes_recommendations(titre_reco3)
                    elif len(df_reponse) > 3:
                        if reco4 == True:
                            titre_reco4 = df_reponse.loc[3, 'Titre']
                            dico = mes_recommendations(titre_reco4)
                        elif len(df_reponse) > 4:
                            if reco5 == True:
                                titre_reco5 = df_reponse.loc[4, 'Titre']
                                dico = mes_recommendations(titre_reco5)
                
        if len(dico.keys()) > 0: 

            df_reco_g = df_final[df_final['ID'].isin(dico["Recommandations générales"])].reset_index() 
            df_reco_f = df_final[df_final['ID'].isin(dico["Recommandations en français"])].reset_index()       

            st.markdown("<h2 style='text-align: center;'>Recommandation de films à voir avec cette sélection : </h2>", unsafe_allow_html=True)

            col31, col32, col33, col34, col35 = st.columns(5)

            with col31: 
                id31 = df_reco_g.loc[0, 'ID']
                film_titre = df_reco_g.loc[0, 'Titre']  # On récupère directement le titre
                infos = details_films(id31)
                videos = video_films(id31)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=31):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_g.loc[0, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_g.loc[0, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            with col32:      
                id32 = df_reco_g.loc[1, 'ID']
                film_titre = df_reco_g.loc[1, 'Titre']  # On récupère directement le titre
                infos = details_films(id32)
                videos = video_films(id32)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=32):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_g.loc[1, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_g.loc[1, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            with col33:  
                id33 = df_reco_g.loc[2, 'ID']
                film_titre = df_reco_g.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id33)
                videos = video_films(id33)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=33):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_g.loc[2, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_g.loc[2, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            with col34:    
                id34 = df_reco_g.loc[3, 'ID']
                film_titre = df_reco_g.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id34)
                videos = video_films(id34)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=34):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_g.loc[3, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_g.loc[3, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            with col35: 
                id35 = df_reco_g.loc[4, 'ID']
                film_titre = df_reco_g.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id35)
                videos = video_films(id35)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=35):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_g.loc[4, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_g.loc[4, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            st.markdown("<h2 style='text-align: center;'>Si vous voulez un film Français : </h2>", unsafe_allow_html=True)

            col41, col42, col43, col44, col45 = st.columns(5)

            with col41:  
                id41 = df_reco_f.loc[0, 'ID']
                film_titre = df_reco_f.loc[0, 'Titre']  # On récupère directement le titre
                infos = details_films(id41)
                videos = video_films(id41)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=41):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_f.loc[0, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_f.loc[0, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

            with col42:     
                id42 = df_reco_f.loc[1, 'ID']
                film_titre = df_reco_f.loc[1, 'Titre']  # On récupère directement le titre
                infos = details_films(id42)
                videos = video_films(id42)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=42):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_f.loc[1, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_f.loc[1, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")
                    
                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")


            with col43:  
                id43 = df_reco_f.loc[2, 'ID']
                film_titre = df_reco_f.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id43)
                videos = video_films(id43)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=43):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_f.loc[2, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_f.loc[2, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")


            with col44:  
                id44 = df_reco_f.loc[3, 'ID']
                film_titre = df_reco_f.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id44)
                videos = video_films(id44)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=44):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_f.loc[3, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_f.loc[3, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")



            with col45:   
                id45 = df_reco_f.loc[4, 'ID']
                film_titre = df_reco_f.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id45)
                videos = video_films(id45)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.markdown("<h3 style='text-align: center;'>" + infos.get('original_title', '') + "</h3>", unsafe_allow_html=True)
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {round(infos.get('vote_average', ''), 1)}/10")

                if st.button(f"Voir les détails de {film_titre}", key=45):
                    st.markdown("<p>Réalisateur : " + ", ".join(df_reco_f.loc[4, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
                    st.markdown("<p>Acteurs principaux :</p>", unsafe_allow_html=True)
                    st.write(", ".join(df_reco_f.loc[4, 'Liste acteurs'][:3]))
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if len(videos) > 0:
                        video_key = videos[0].get('key', '')
                        if video_key:
                            st.video(f"https://www.youtube.com/watch?v={video_key}")

# Mise en place de la page 'Films à l'affiche':
if page == "Films à l'affiche":
    st.markdown("<h1 style='text-align: center;'>Films à l'affiche en ce moment</h1>", unsafe_allow_html=True)# "Les films populaires"
    col1, col2, col3 = st.columns([2, 10, 2])#Code pour donner du poid à une colonne plus qu'aux autres
    with col2:
        st.image("./Images/affiche.jpg",  use_container_width=True)

    films = films_populaire()

    # Afficher la liste des films avec le détail de l'affiche:
    cols = st.columns(5)  # Créer 5 colonnes pour les 5 affiches
    for i, movie in enumerate(films[:5]):
      with cols[i]:
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.markdown(f"<h1 style='text-align: center;'>{movie['title']}</h1>", unsafe_allow_html=True)
            # st.write(f':['tagline']')
            st.write(f"Date de sortie : {movie['release_date']}")
            st.write(f"Note spéctateur : {round(movie['vote_average'], 1)}/10")
            
            
            if st.button(f"Voir les détails de {movie['title']}", key=movie['id']):
                infos = details_films(movie['id'])
                videos= video_films(movie['id'])   # Ajoutée
                st.write(f"**Synopsis :** {infos['overview']}")
                st.write(f"**Durée :** {infos['runtime']} minutes")
                st.write(f"**Genres :** {', '.join([genre['name'] for genre in infos['genres']])}")
                st.write(f"**Pays d'origine :** {infos['origin_country'][0]}")
                if len(videos) > 0:
                    st.video(f"https://www.youtube.com/watch?v={videos[0]['key']}")
                else:
                    st.write("Pas de bande annonce diponible pour ce film")

    cols = st.columns(5)  # Créer 5 colonnes pour les 5 affiches
    for i, movie in enumerate(films[5 : 10]):
      with cols[i]:
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.markdown(f"<h1 style='text-align: center;'>{movie['title']}</h1>", unsafe_allow_html=True)
            # st.write(f':['tagline']')
            st.write(f"Date de sortie : {movie['release_date']}")
            st.write(f"Note spéctateur : {round(movie['vote_average'], 1)}/10")
            
            
            if st.button(f"Voir les détails de {movie['title']}", key=movie['id']):
                infos = details_films(movie['id'])
                videos= video_films(movie['id'])   # Ajoutée
                st.write(f"**Synopsis :** {infos['overview']}")
                st.write(f"**Durée :** {infos['runtime']} minutes")
                st.write(f"**Genres :** {', '.join([genre['name'] for genre in infos['genres']])}")
                st.write(f"**Pays d'origine :** {infos['origin_country'][0]}")
                if len(videos) > 0:
                    st.video(f"https://www.youtube.com/watch?v={videos[0]['key']}")
                else:
                    st.write("Pas de bande annonce diponible pour ce film")

    cols = st.columns(5)  # Créer 5 colonnes pour les 5 affiches
    for i, movie in enumerate(films[10:15]):
      with cols[i]:
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.markdown(f"<h1 style='text-align: center;'>{movie['title']}</h1>", unsafe_allow_html=True)
            # st.write(f':['tagline']')
            st.write(f"Date de sortie : {movie['release_date']}")
            st.write(f"Note spéctateur : {round(movie['vote_average'], 1)}/10")
            
            
            if st.button(f"Voir les détails de {movie['title']}", key=movie['id']):
                infos = details_films(movie['id'])
                videos= video_films(movie['id'])   # Ajoutée
                st.write(f"**Synopsis :** {infos['overview']}")
                st.write(f"**Durée :** {infos['runtime']} minutes")
                st.write(f"**Genres :** {', '.join([genre['name'] for genre in infos['genres']])}")
                st.write(f"**Pays d'origine :** {infos['origin_country'][0]}")
                if len(videos) > 0:
                    st.video(f"https://www.youtube.com/watch?v={videos[0]['key']}")
                else:
                    st.write("Pas de bande annonce diponible pour ce film")

    cols = st.columns(5)  # Créer 5 colonnes pour les 5 affiches
    for i, movie in enumerate(films[15 : 20]):
      with cols[i]:
            st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}")
            st.markdown(f"<h1 style='text-align: center;'>{movie['title']}</h1>", unsafe_allow_html=True)
            # st.write(f':['tagline']')
            st.write(f"Date de sortie : {movie['release_date']}")
            st.write(f"Note spéctateur : {round(movie['vote_average'], 1)}/10")
            
            
            if st.button(f"Voir les détails de {movie['title']}", key=movie['id']):
                infos = details_films(movie['id'])
                videos= video_films(movie['id'])   # Ajoutée
                st.write(f"**Synopsis :** {infos['overview']}")
                st.write(f"**Durée :** {infos['runtime']} minutes")
                st.write(f"**Genres :** {', '.join([genre['name'] for genre in infos['genres']])}")
                st.write(f"**Pays d'origine :** {infos['origin_country'][0]}")
                if len(videos) > 0:
                    st.video(f"https://www.youtube.com/watch?v={videos[0]['key']}")
                else:
                    st.write("Pas de bande annonce diponible pour ce film")
                


if page == "Statistiques":
    st.markdown("<h1 style='text-align: center;'>Quelques chiffres</h1>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([2, 10, 2])#Code pour donner du poid à une colonne plus qu'aux autres
    with col2:
        st.image("./Images/statistiques.jpeg",  use_container_width=True)

    st.markdown("<h2 style='text-align: center;'>Voici quelques statistiques sorties de notre base de donnée Aliciné, nous espérons que vous les trouverez intéressantes! N'hésitez pas à nous faire part de vos souhait si vous souhaitez en apprendre plus sur la superbe sélection que nous avons faite pour vous! A vos stats!</h2>", unsafe_allow_html=True)
              
    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.image("./Images/acteurs.png",  use_container_width=True)

        with col2:
            st.markdown("""<h1 style='text-align: center;'> 
            COCORICO!!
                     
            Nous pouvons voir que selon notre base de donnée Aliciné
                     
            L'acteur ayant tourné le plus de film depuis 1970 est nontre 
                     
            cher M.Gérard Depardieu! 
                     
            Un grand bravo à lui pour cette formaidable carrière!
                     
            On occultera volontairement le fait qu'il est le seul acteur 
                     
            français dans ce top 7...

            """, unsafe_allow_html=True)

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.markdown("""<h1 style='text-align: center;'> 
            Ah le Parrain! 
                     
            Que de scènes emblématiques! C'est donc le film qui recoit 
                        
            la meilleure note de notre sélection.
                     
            On remarquera que les 4 meilleures notes sont pour 4 drames, 
                        
            ce qui prouve bien notre amour de la tristesse et la désolation. 
                  
            Haut les coeurs!

            Pas de films français à se mettre sous la dent dans ce top.
                        
            Quel dommage !

            Surtout quand on connait l'extraordinaire qualité de notre cinéma,

            spécialement dans la catégorie "drames"...  

            """, unsafe_allow_html=True)

        with col2:
            st.image("./Images/films.png",  use_container_width=True)

    with st.container(border=True):
        col1, col2 = st.columns(2)
        with col1:
            st.image("./Images/durée.png",  use_container_width=True)

        with col2:
            st.markdown("""<h1 style='text-align: center;'> 
            Place aux rides et à l'expérience !!!
                        
            On constate que les acteurs prennent de l'âge au fil du temps, 
                        
            en revanche les films restent fidèles à leur format de 100 mins environ. 
                        
            Les producteurs misent beaucoup plus sur des stars "vintage ". 
                        
            Un choix qui prouve qu'en cinéma comme en vin, l'âge a du goût. 

            """, unsafe_allow_html=True)
                     
        
  
