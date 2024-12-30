import pandas as pd
import ast
import streamlit as st

link6 = "./BD/df_recherche.csv"

df_recherche = pd.read_csv(link6)

df_recherche['Titres possibles'] = df_recherche['Titres possibles'].apply(ast.literal_eval)
df_recherche['Genres'] = df_recherche['Genres'].apply(ast.literal_eval)
df_recherche['Liste acteurs'] = df_recherche['Liste acteurs'].apply(ast.literal_eval)
df_recherche['Réalisateurs'] = df_recherche['Réalisateurs'].apply(ast.literal_eval)


st.title("Bienvenue sur ALICiné")

#Listes des éléments uniques pour recherche:
acteurs = []
reals = []
genres = []

#Fonction pour un futur "apply" qui ajoute chaque liste du df à la liste vide
def liste_acteurs(x):
    acteurs.extend(x)

def liste_reals(x):
    reals.extend(x)

def liste_genres(x):
    genres.extend(x)   

df_recherche['Liste acteurs'].apply(liste_acteurs)
df_recherche['Réalisateurs'].apply(liste_reals)
df_recherche['Genres'].apply(liste_genres)

#Pour supprimer les doublons on passe par un set:

acteurs = ['Sélectionner un acteur'] + list(set(acteurs))
reals = ['Sélectionner un réalisateur'] + list(set(reals))
genres = ['Sélectionner un genre'] + list(set(genres))
decennie = ['Sélectionner une décénie'] + list(df_recherche['Décénnie'].unique())

search_titre = st.text_input('Recherche par titre :')
search_acteur = st.selectbox('Recherche par acteur :', acteurs)
search_real = st.selectbox('Recherche par réalisateur :', reals)
search_genre = st.selectbox('Recherche par genre', genres)
search_decennie = st.selectbox('Recherche par décénnie', decennie)



with st.sidebar:
    st.title("Menu")
