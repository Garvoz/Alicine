import pandas as pd
import ast
import streamlit as st
import pickle

st.set_page_config(layout="wide")

link6 = "./BD/df_recherche.csv"

df_recherche = pd.read_csv(link6)

df_recherche['Titres possibles'] = df_recherche['Titres possibles'].apply(ast.literal_eval)
df_recherche['Genres'] = df_recherche['Genres'].apply(ast.literal_eval)
df_recherche['Liste acteurs'] = df_recherche['Liste acteurs'].apply(ast.literal_eval)
df_recherche['Réalisateurs'] = df_recherche['Réalisateurs'].apply(ast.literal_eval)


st.markdown("<h1 style='text-align: center;'>Bienvenue sur ALICiné</h1>", unsafe_allow_html=True)

with open('./BD/mes_listes.pkl', 'rb') as f:
    acteurs = pickle.load(f)
    reals = pickle.load(f)
    genres = pickle.load(f)
    decennie = pickle.load(f)

search_titre = st.text_input('Recherche par titre :', '')

col1, col2 = st.columns(2)

with col1:
    search_acteur = st.selectbox('Recherche par acteur :', acteurs, index=None, placeholder="Choisissez un acteur...")
    search_real = st.selectbox('Recherche par réalisateur :', reals, index=None, placeholder="Choisissez un réalisateur...")

with col2:
    search_genre = st.selectbox('Recherche par genre', genres, index=None, placeholder="Choisissez un genre...")
    search_decennie = st.selectbox('Recherche par décénnie', decennie, index=None, placeholder="Choisissez une décénnie...")

if (search_titre != '') or (search_acteur != None) or (search_real != None) or (search_genre != None) or (search_decennie != None):
    st.markdown("<h2 style='text-align: center;'>Films les mieux notés selon votre recherche :</h2>", unsafe_allow_html=True)

    df_reponse = df_recherche.copy()

    if search_titre != '':
        df_reponse = df_reponse[df_reponse['Titres possibles'].apply(lambda x: search_titre in x)]
    if search_acteur != None:
        df_reponse = df_reponse[df_reponse['Liste acteurs'].apply(lambda x: search_acteur in x)]
    if search_real != None:
        df_reponse = df_reponse[df_reponse['Réalisateurs'].apply(lambda x: search_real in x)] 
    if search_genre != None:
        df_reponse = df_reponse[df_reponse['Genres'].apply(lambda x: search_genre in x)]
    if search_decennie != None:
        df_reponse = df_reponse[df_reponse['Décénnie'] == search_decennie]

    df_reponse = df_reponse.sort_values(by=['Note moyenne', 'Nb de votes'] , ascending=False).head(5).reset_index()

    col21, col22, col23, col24, col25 = st.columns(5)

    with col21:
        st.image("https://image.tmdb.org/t/p/w500" + df_reponse.loc[0, 'Lien du poster'] )
        st.markdown("<h3 style='text-align: center;'>" + df_reponse.loc[0, 'Titre'] + "</h3>", unsafe_allow_html=True)
        st.markdown("<p><b>Date de sortie :</b> " + df_reponse.loc[0, 'Date de sortie'] + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Réalisateur :</b> " + ", ".join(df_reponse.loc[0, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Note spectateurs :</b> " + str(df_reponse.loc[0, 'Note moyenne']) + "/10</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Durée :</b> " + str(df_reponse.loc[0, 'Durée (minutes)']) + " minutes</p>", unsafe_allow_html=True)
        if df_reponse.loc[0, 'Budget'] > 0:
            st.markdown("<p><b>Budget :</b> " + str(df_reponse.loc[0, 'Budget']) + " $</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Acteurs principaux :</b></p>", unsafe_allow_html=True)
        st.write(", ".join(df_reponse.loc[0, 'Liste acteurs'][:3]))  
        st.markdown("<p><b>Résumé en Anglais : </b></p>", unsafe_allow_html=True)      
        st.write(df_reponse.loc[0, 'Résumé'])
    
    with col22:
        st.image("https://image.tmdb.org/t/p/w500" + df_reponse.loc[1, 'Lien du poster'] )
        st.markdown("<h3 style='text-align: center;'>" + df_reponse.loc[1, 'Titre'] + "</h3>", unsafe_allow_html=True)
        st.markdown("<p><b>Date de sortie :</b> " + df_reponse.loc[1, 'Date de sortie'] + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Réalisateur :</b> " + ", ".join(df_reponse.loc[1, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Note spectateurs :</b> " + str(df_reponse.loc[1, 'Note moyenne']) + "/10</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Durée :</b> " + str(df_reponse.loc[1, 'Durée (minutes)']) + " minutes</p>", unsafe_allow_html=True)
        if df_reponse.loc[1, 'Budget'] > 0:
            st.markdown("<p><b>Budget :</b> " + str(df_reponse.loc[1, 'Budget']) + " $</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Acteurs principaux :</b></p>", unsafe_allow_html=True)
        st.write(", ".join(df_reponse.loc[1, 'Liste acteurs'][:3]))  
        st.markdown("<p><b>Résumé en Anglais : </b></p>", unsafe_allow_html=True)      
        st.write(df_reponse.loc[1, 'Résumé'])

    with col23:
        st.image("https://image.tmdb.org/t/p/w500" + df_reponse.loc[2, 'Lien du poster'] )
        st.markdown("<h3 style='text-align: center;'>" + df_reponse.loc[2, 'Titre'] + "</h3>", unsafe_allow_html=True)
        st.markdown("<p><b>Date de sortie :</b> " + df_reponse.loc[2, 'Date de sortie'] + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Réalisateur :</b> " + ", ".join(df_reponse.loc[2, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Note spectateurs :</b> " + str(df_reponse.loc[2, 'Note moyenne']) + "/10</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Durée :</b> " + str(df_reponse.loc[2, 'Durée (minutes)']) + " minutes</p>", unsafe_allow_html=True)
        if df_reponse.loc[2, 'Budget'] > 0:
            st.markdown("<p><b>Budget :</b> " + str(df_reponse.loc[2, 'Budget']) + " $</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Acteurs principaux :</b></p>", unsafe_allow_html=True)
        st.write(", ".join(df_reponse.loc[2, 'Liste acteurs'][:3]))  
        st.markdown("<p><b>Résumé en Anglais : </b></p>", unsafe_allow_html=True)      
        st.write(df_reponse.loc[2, 'Résumé'])

    with col24:
        st.image("https://image.tmdb.org/t/p/w500" + df_reponse.loc[3, 'Lien du poster'] )
        st.markdown("<h3 style='text-align: center;'>" + df_reponse.loc[3, 'Titre'] + "</h3>", unsafe_allow_html=True)
        st.markdown("<p><b>Date de sortie :</b> " + df_reponse.loc[3, 'Date de sortie'] + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Réalisateur :</b> " + ", ".join(df_reponse.loc[3, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Note spectateurs :</b> " + str(df_reponse.loc[3, 'Note moyenne']) + "/10</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Durée :</b> " + str(df_reponse.loc[3, 'Durée (minutes)']) + " minutes</p>", unsafe_allow_html=True)
        if df_reponse.loc[3, 'Budget'] > 0:
            st.markdown("<p><b>Budget :</b> " + str(df_reponse.loc[3, 'Budget']) + " $</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Acteurs principaux :</b></p>", unsafe_allow_html=True)
        st.write(", ".join(df_reponse.loc[3, 'Liste acteurs'][:3]))  
        st.markdown("<p><b>Résumé en Anglais : </b></p>", unsafe_allow_html=True)      
        st.write(df_reponse.loc[3, 'Résumé'])

    with col25:
        st.image("https://image.tmdb.org/t/p/w500" + df_reponse.loc[4, 'Lien du poster'] )
        st.markdown("<h3 style='text-align: center;'>" + df_reponse.loc[4, 'Titre'] + "</h3>", unsafe_allow_html=True)
        st.markdown("<p><b>Date de sortie :</b> " + df_reponse.loc[4, 'Date de sortie'] + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Réalisateur :</b> " + ", ".join(df_reponse.loc[4, 'Réalisateurs']) + "</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Note spectateurs :</b> " + str(df_reponse.loc[4, 'Note moyenne']) + "/10</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Durée :</b> " + str(df_reponse.loc[4, 'Durée (minutes)']) + " minutes</p>", unsafe_allow_html=True)
        if df_reponse.loc[4, 'Budget'] > 0:
            st.markdown("<p><b>Budget :</b> " + str(df_reponse.loc[4, 'Budget']) + " $</p>", unsafe_allow_html=True)
        st.markdown("<p><b>Acteurs principaux :</b></p>", unsafe_allow_html=True)
        st.write(", ".join(df_reponse.loc[4, 'Liste acteurs'][:3]))  
        st.markdown("<p><b>Résumé en Anglais : </b></p>", unsafe_allow_html=True)      
        st.write(df_reponse.loc[4, 'Résumé'])


with st.sidebar:
    st.title("Menu")
