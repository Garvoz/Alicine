import streamlit as st
import requests
from streamlit_option_menu import option_menu
import pandas as pd
import streamlit as st
import ast
import pickle
import base64
from sklearn.neighbors import NearestNeighbors


link2 = "./BD/movies.csv"
movies = pd.read_csv(link2)

#Code Machine learning:
def mes_recommendations(movie_title, nb_films=5):
    if movie_title not in movies['Titre'].values:
        return "Le film demandé n'est pas dans la base de données."
    
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
        "Recommandations générales": list(recommended_movie_ids),
        "Recommandations en français": list(recommended_french_movie_ids)
    }


# Etendre le contenu de la page.
st.set_page_config( layout="wide")
# st.st.cache_resource.clear() # st.cache_data ou st.cache_resource ou st.cache

# Ajouter le logo en haut de la sidebar
st.sidebar.image('./Alicine_logo.jpeg', use_container_width=True)
# st.sidebar.image('Projet2PersoAZ/logoCineCreusois.jpeg', width=200) # je fige la taille de l'image


# Pict_SB = './Images/falling_popcorn.jpeg'
# Pict_fond = './Images/Meme_confort_maison.jpeg'

# # Image Sidebar
# with open(Pict_SB, "rb") as image_file:
#     encoded_image = base64.b64encode(image_file.read()).decode()

#     st.markdown(
#         f"""
#         <style>
#         [data-testid="stSidebar"] > div:first-child {{
#             background-image: url("data:image/jpeg;base64,{encoded_image}");
#             background-size: cover;
#         }}
#         </style>
#         """,
#         unsafe_allow_html=True
#     )

# Image fond de site
# with open(Pict_fond, "rb") as image_file:
#     encoded_image2 = base64.b64encode(image_file.read()).decode()

# template_htlm = f"""
#         <style>
#         body {{
#         background-image: url(data:image/jpeg;base64,{encoded_image2});
#         background-size: cover;
#         background-repeat: no-repeat;
#         background-position: center;
#         overflow: hidden;
#         display: flex;}}
#         </style>
#         """
        
# st.markdown(template_htlm, unsafe_allow_html=True)



# Gérer la bare des taches (sidebar):
with st.sidebar:

    page = option_menu(menu_title=None, options = ["Accueil", "Mieux nous connaitre", "Recherche personnalisée", "Films à l'affiche",  "Statistiques"])

    st.sidebar.markdown('<p style="color:white;">Besoin de nous contacter?</p>', unsafe_allow_html=True)
    st.sidebar.markdown('<p style="color:white;">contact@cine-creusois.com</p>', unsafe_allow_html=True)
    # st.sidebar.markdown("[contact@cine-creusois.com](mailto:contact@cine-creusois.com)")
    st.sidebar.markdown("<p style='color:white;'>+33 5 55 25 25 25 (prix d'un appel local)</p>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='color:white;'>Avenue d'auvergne, 23000 Gueret, France</p>", unsafe_allow_html=True)



Nom_Cine = "ALICINÉ" # Ciné Creusois, CinéCéven, Le Cévenol (en ref aux Cévennes la chaine de montagne),


if page == "Accueil":
  st.image("./accueil.jpeg")
  st.title(f"Bienvenue dans l'univers {Nom_Cine} !") 
  # autre proposition du subheader : Le cinéma s'offre une métamorphose digitale / Le cinéma se transforme et entre dans l'ère numérique
  st.subheader(f"Votre cinéma se modernise et vous dévoile son côté digital ") 
  st.write("""          
           Nous sommes heureux de vous offrir une sélection de films variée et de qualité, dans un cadre convivial et chaleureux. 
           """)
  st.write("""          
           Découvrez notre programmation, les films à l'affiche, nos recommandations personnalisées et les statistiques intéressantes. 
           """)
  st.write("Et surtout bonne navigation!")

   # image Ciné à ajouter



if page == "Mieux nous connaitre":
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


            # Fonction pour API(s):

      # URL de base de l'API TMDb
BASE_URL = 'https://api.themoviedb.org/3/'
    # Votre clé API TMDb
API_KEY = '3bca9c26909e582a5584220844dc20e1'
# 1- Fonction qui permet de récupérer les films populaires à jour API TMDB:
def films_populaire():
    url = f'{BASE_URL}movie/popular?api_key={API_KEY}&language=fr-FR&page=1'
    response = requests.get(url)
    data = response.json()
    return data['results']

# 2- Fonction pour récupérer les détails d'un film grace à un ID depuis API TMDB:
def details_films(movie_id):
    url = f'{BASE_URL}movie/{movie_id}?api_key={API_KEY}&language=fr-FR'
    response = requests.get(url)
    return response.json()
  
# 3- Fonction qui permet de récupérer les bandes annonce grace à un ID depuis API TMDB:: 
def video_films(movie_id):
      url = f'{BASE_URL}movie/{movie_id}/videos?api_key={API_KEY}&language=fr-FR'
      response = requests.get(url)
      video = response.json()
      return video["results"]

# le nécéssaire pour la recherche personnalisée via API TMDB:
link = "./BD/df_final.csv"
df_final = pd.read_csv(link)

df_final['Genres'] = df_final['Genres'].apply(ast.literal_eval)
df_final['Liste acteurs'] = df_final['Liste acteurs'].apply(ast.literal_eval)
df_final['Réalisateurs'] = df_final['Réalisateurs'].apply(ast.literal_eval)

with open('./BD/mes_listes.pkl', 'rb') as f:
    acteurs = pickle.load(f)
    reals = pickle.load(f)
    genres = pickle.load(f)
    decennie = pickle.load(f)


if page == "Recherche personnalisée":
    st.markdown("<h1 style='text-align: center;'>Qu'est-ce qu'on regarde ce soir ?</h1>", unsafe_allow_html=True)
    st.image("recherche.jpg", caption="Image centrée", use_container_width=True)

        # Présentation du moteur de recherche :
        
    search_titre = st.text_input('Recherche par titre :', '')
    col1, col2 = st.columns(2)
    with col1:
        search_acteur = st.selectbox('Recherche par acteur :', acteurs, index=None, placeholder="Choisissez un acteur...")
        search_real = st.selectbox('Recherche par réalisateur :', reals, index=None, placeholder="Choisissez un réalisateur...")
    with col2:
        search_genre = st.selectbox('Recherche par genre', genres, index=None, placeholder="Choisissez un genre...")
        search_decennie = st.selectbox('Recherche par décénnie', decennie, index=None, placeholder="Choisissez une décénnie...")


  # code de recherche : 
    df_reponse = df_final.copy()

    if search_titre != '':
         # traitement de la recherche en string, case = False  ==> ignore la casse, 
         df_reponse = df_reponse[df_reponse['Titres possibles'].str.contains(search_titre, case=False)]
    if search_acteur != None:
        df_reponse = df_reponse[df_reponse['Liste acteurs'].apply(lambda x: search_acteur in x)]
    if search_real != None:
        df_reponse = df_reponse[df_reponse['Réalisateurs'].apply(lambda x: search_real in x)] 
    if search_genre != None:
        df_reponse = df_reponse[df_reponse['Genres'].apply(lambda x: search_genre in x)]
    if search_decennie != None:
        df_reponse = df_reponse[df_reponse['Décénnie'] == search_decennie]

    df_reponse = df_reponse.sort_values(by=['Note moyenne', 'Nb de votes'] , ascending=False).head().reset_index()
    # movies = df_reponse.copy()

# il affiche scoobido car c'est le premier film du df lors du test de df_reponse.loc[0, 'Titre']
    if (search_titre != '') or (search_acteur != None) or (search_real != None) or (search_genre != None) or (search_decennie != None):
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
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id1)):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

                    if videos and len(videos) > 0:
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

                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id2)):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")
                        
        with col23:
            if len(df_reponse) > 2:
                id3 = df_reponse.loc[2, 'ID']
                film_titre = df_reponse.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id3)
                videos = video_films(id3)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco3 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=23)

                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id3)):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")            

        with col24:
            if len(df_reponse) > 3:
                id4 = df_reponse.loc[3, 'ID']
                film_titre = df_reponse.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id4)
                videos = video_films(id4)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco4 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=24)

                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id4)):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

        with col25:
            if len(df_reponse) > 4:
                id5 = df_reponse.loc[4, 'ID']
                film_titre = df_reponse.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id5)
                videos = video_films(id5)

                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                reco5 = st.checkbox("Voir les meilleurs films similaires recommandés:", key=25)
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=str(id5)):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")
  

        dico = {}

        if len(df_reponse) > 0:
            if reco1 == True:
                titre_reco = df_reponse.loc[0, 'Titre']
                dico = mes_recommendations(titre_reco)
            elif len(df_reponse) > 1:
                if reco2 == True:
                    titre_reco = df_reponse.loc[1, 'Titre']
                    dico = mes_recommendations(titre_reco)
                elif len(df_reponse) > 2:
                    if reco3 == True:
                        titre_reco = df_reponse.loc[2, 'Titre']
                        dico = mes_recommendations(titre_reco)
                    elif len(df_reponse) > 3:
                        if reco4 == True:
                            titre_reco = df_reponse.loc[3, 'Titre']
                            dico = mes_recommendations(titre_reco)
                        elif len(df_reponse) > 4:
                            if reco5 == True:
                                titre_reco = df_reponse.loc[4, 'Titre']
                                dico = mes_recommendations(titre_reco)
                
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
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=31):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            with col32:      
                id32 = df_reco_g.loc[1, 'ID']
                film_titre = df_reco_g.loc[1, 'Titre']  # On récupère directement le titre
                infos = details_films(id32)
                videos = video_films(id32)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=32):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            with col33:  
                id33 = df_reco_g.loc[2, 'ID']
                film_titre = df_reco_g.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id33)
                videos = video_films(id33)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=33):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            with col34:    
                id34 = df_reco_g.loc[3, 'ID']
                film_titre = df_reco_g.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id34)
                videos = video_films(id34)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=34):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            with col35: 
                id35 = df_reco_g.loc[4, 'ID']
                film_titre = df_reco_g.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id35)
                videos = video_films(id35)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=35):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            st.markdown("<h2 style='text-align: center;'>Si vous voulez un film Français : </h2>", unsafe_allow_html=True)

            col41, col42, col43, col44, col45 = st.columns(5)

            with col41:  
                id41 = df_reco_f.loc[0, 'ID']
                film_titre = df_reco_f.loc[0, 'Titre']  # On récupère directement le titre
                infos = details_films(id41)
                videos = video_films(id41)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=41):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

            with col42:     
                id42 = df_reco_f.loc[1, 'ID']
                film_titre = df_reco_f.loc[1, 'Titre']  # On récupère directement le titre
                infos = details_films(id42)
                videos = video_films(id42)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=42):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")


            with col43:  
                id43 = df_reco_f.loc[2, 'ID']
                film_titre = df_reco_f.loc[2, 'Titre']  # On récupère directement le titre
                infos = details_films(id43)
                videos = video_films(id43)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=43):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")


            with col44:  
                id44 = df_reco_f.loc[3, 'ID']
                film_titre = df_reco_f.loc[3, 'Titre']  # On récupère directement le titre
                infos = details_films(id44)
                videos = video_films(id44)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=44):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")



            with col45:   
                id45 = df_reco_f.loc[4, 'ID']
                film_titre = df_reco_f.loc[4, 'Titre']  # On récupère directement le titre
                infos = details_films(id45)
                videos = video_films(id45)
                                                
                if infos.get('poster_path'): 
                    st.image(f"https://image.tmdb.org/t/p/w500{infos['poster_path']}")
                st.subheader(infos.get('original_title', ''))
                st.write(f"Date de sortie : {infos.get('release_date', '')}")
                st.write(f"Note spectateur : {infos.get('vote_average', '')}/10")

                if st.button(f"Voir les détails de {film_titre}", key=45):
                    st.write(f"Synopsis : {infos.get('overview', '')}")
                    st.write(f"Durée : {infos.get('runtime', '')} minutes")

                    genres = infos.get('genres', [])
                    genre_names = [genre.get('name', '') for genre in genres]
                    st.write(f"Genres : {', '.join(genre_names)}")

                    pays = infos.get('origin_country', [])
                    if pays and len(pays) > 0:
                        st.write(f"Pays d'origine : {pays[0]}")

if page == "Films à l'affiche":
    # test interface utilisateur Streamlit
    st.title("A l'affiche : ")    # "Les films populaires"

    # Récupérer les films populaires "data['results']"
    movies = films_populaire()

    # Afficher la liste des films avec le détail de l'affiche:
    cols = st.columns(5)  # Créer 5 colonnes pour les 5 affiches
    for i, movie in enumerate(movies[:5]):
      with cols[i]:
              st.image(f"https://image.tmdb.org/t/p/w500{movie['poster_path']}", width=200)
              st.subheader(movie['title'])
              # st.write(f':['tagline']')
              st.write(f"Date de sortie : {movie['release_date']}")
              st.write(f"Note spéctateur : {movie['vote_average']}/10")
              
              
              if st.button(f"Voir les détails de {movie['title']}", key=movie['id']):
                  infos = details_films(movie['id'])
                  videos= video_films(movie['id'])   # Ajoutée
                  st.write(f"**Synopsis :** {infos['overview']}")
                  st.write(f"**Durée :** {infos['runtime']} minutes")
                  st.write(f"**Genres :** {', '.join([genre['name'] for genre in infos['genres']])}")
                  st.write(f"**Pays d'origine :** {infos['origin_country'][0]}")
                  st.video(f"https://www.youtube.com/watch?v={videos[0]["key"]}")


if page == "Statistique":
  st.title("Voici quelques Statistique sur les films")
  # st.image("https://www.code-couleur.com/images/listing/rose-lilas.jpg")
  col1, col2 = st.columns(2)
  
  with col1:
    st.header("Présentation par genre")
    # st.image('C:\Users\ibtis\Desktop\VS_Code\Quetes\Stream_Lit\photos\Présentation_genres.jpg')


  # test : en plus vu l'indentation décalé cette selectbox apparait dans toute les sidebarres
  Liste = [' ', 'Tom', 'Tom Hanks', 'Tom Cruise', 'Tom Hardy', 'Tom bétise', 'Tom zoulou', 'Chico', 'charlotte', 'princess Charlotte']
  st.selectbox("Quels sont vos personnages favoris ?", Liste, placeholder="Selectionnez un acteur...")  
