""" BIENVENUE DANS NOTRE MODULE CHARGEMENT ET NETTOYAGE DES DONNEES"""

import os 

# On se place dans la partie 2 et on récupere le chemin du répertoire courant

current_path = os.getcwd()
#On remonte d'un niveau dans les dossiers
path = os.path.abspath(os.path.join(current_path, '..'))
#On joint le chemin obtenu avec le dossier 'data'
path_data = os.path.join(path, 'data')
os.chdir(path_data)


import pandas as pd

'DataFrame ARTIST'

df_art=pd.read_csv("artists.csv",encoding="utf-8")
df_art = df_art.rename(columns = {'name':'artists'}) #renomme libellé de la colonne
df_art['artists'] = df_art['artists'].str.lower()

#remplacer les crochets "[]" par une chaine vide dans chaque colonne
df_art= df_art.replace(to_replace=r'\[|\]', value='', regex=True)
#retirer les apostrophes & remplacer les valeurs manquantes pas 'Aucun'
df_art = df_art.replace(to_replace="'", value='', regex=True)
df_art = df_art.replace(to_replace="", value='Aucun', regex=True)

'DataFrame TRACK'

df_track=pd.read_csv("tracks.csv",encoding="utf-8")
#remplace les crochets "[]" par une chaine vide dans chaque colonne
df_track= df_track.replace(to_replace=r'\[|\]', value='', regex=True)
#retirer les apostrophes
df_track = df_track.replace(to_replace="'", value='', regex=True)
#Modifications dates : 
        #transformer en to_datetime
df_track["release_date"] = pd.to_datetime(df_track["release_date"], format="%Y-%m-%d")
        #créer une nouvelle colonne pour les années de sorties
df_track["release_year"] = df_track["release_date"].dt.strftime('%Y')


'DataFrame TOP200'

df_top200 = pd.read_csv("spotify_top200_global.csv",encoding="utf-8")

'DataFrame SIGNLEPARARTISTE'

#groupe par artiste et calcule la somme des streams pour chaque artiste (alternative à .agg)
sommestream = df_top200.groupby("Artist")["Streams"].sum().reset_index() 

#groupe par artiste et compte le nombre de titres unique pour chaque artiste
singleparartiste = df_top200.groupby("Artist")["Title"].nunique().reset_index() 
singleparartiste.columns = ["Artist", "Nombre de single dans le top200"] 

def clean():
    return df_art, df_track, df_top200, singleparartiste
