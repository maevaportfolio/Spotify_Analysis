# -*- coding: utf-8 -*-


##########Création de module 

'''
Ce module nous servira à stocker nos fonctions utilisées tout au long de notre
projet.

'''


##Import de librairies

import os
os.getcwd()

import os 
import pandas as pd
import numpy as np
import seaborn as sns 
from matplotlib import pyplot as plt
from datetime import datetime
import matplotlib.cm as cm 
from colorama import init, Fore, Back, Style


##Les données

df_art=pd.read_csv("artists.csv",encoding="utf-8")
df_art.head()

df_track=pd.read_csv("tracks.csv",encoding="utf-8")
df_track.head()

df_top200 = pd.read_csv("spotify_top200_global.csv",encoding="utf-8")
df_top200.head()


##Fonction pour des infos sommaires sur le dataframe

def data_summary(df):
    # Afficher les informations générales sur le DataFrame
    print("Informations générales sur le DataFrame:")
    print(df.info())
    print("\n")

    # Vérifier les valeurs nulles dans le DataFrame
    print("Valeurs manquantes dans le DataFrame:")
    print(df.isna().sum())
    print("\n")

    
    
################################### Pour l'analyse univariée

##Description du dataframe : df_art, df_track, 
def description(df):
    print("Le dataframe df_art a {} lignes et {} colonnes".format(df.shape[0], df.shape[1]))
    print("\nLes colonnes du dataframe sont: \n ")
    print(df.columns)
    print("\nLes libellés et types de variables : \n")
    print(df.dtypes)
    return


#### df_art
##Maximum et minimum de followers
def xtrm_flw(df_art):
    max_flw = df_art["followers"].max()
    min_flw = df_art["followers"].min()
    artist_maxflw = df_art[df_art["followers"] == max_flw]["name"].values[0]
    artist_minflw = df_art[df_art["followers"] == min_flw]["name"].values[0]
    
    print("L'artiste avec le plus de followers est", artist_maxflw, "avec", round(max_flw), "followers.")
    print("L'artiste avec le moins de followers est", artist_minflw, "avec", round(min_flw), "followers.")
    return


#### df_track
## Sons les plus ancien et récent
def old_new_song(df_track):   
    df_track["release_date"]= pd.to_datetime(df_track["release_date"], format="%Y-%m-%d")
    aujdh = datetime(2023, 11, 4)
    duree = aujdh - df_track["release_date"]
    df_track["duree_annee"] = round(duree/np.timedelta64(1, 'Y'))
    ##morceaux: plus ancien et plus récent
    oldest_song = df_track[df_track["duree_annee"] == df_track["duree_annee"].max()]["name"].values[0]
    newest_song = df_track[df_track["duree_annee"] == df_track["duree_annee"].min()]["name"].values[0]
    ##les artistes correspondants
    old_artiste = df_track[df_track["duree_annee"] == df_track["duree_annee"].max()]["artists"].values[0]
    new_artiste = df_track[df_track["duree_annee"] == df_track["duree_annee"].min()]["artists"].values[0]    
    print("Le morceau le plus ancien est:", oldest_song, "de", old_artiste)
    print("Le morceau le plus récent est:", newest_song, "de", new_artiste)
    return


#### df_top200
## Artistes les plus/moins streamés sur l'année
def maxminstream(df_top200):
    stream_max = df_top200[df_top200["Streams"] == df_top200["Streams"].max()]["Title"].values[0]
    stream_min = df_top200[df_top200["Streams"] == df_top200["Streams"].min()]["Title"].values[0]
    stream_max_artiste = df_top200[df_top200["Streams"] == df_top200["Streams"].max()]["Artist"].values[0]
    stream_min_artiste = df_top200[df_top200["Streams"] == df_top200["Streams"].min()]["Artist"].values[0]
    
    print("Le morceau le plus streamé du TOP 200 Spotify est:", stream_max, "de", stream_max_artiste)
    print("Le morceau le moins streamé du TOP 200 Spotify est:", stream_min, "de", stream_min_artiste)

    return



################################### Pour l'analyse bivariée

##Matrice de corrélation
def visualize_correlation(df):
    """
    Visualise la corrélation entre les colonnes d'un DataFrame sous forme d'un heatmap.

    :param df: Le DataFrame contenant les données.
    """
    corr_matrix = df.corr()
    plt.figure(figsize=(16, 10))
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', linewidths=0.5)
    plt.title("Heatmap de Corrélation")
    plt.show()

##Matrice de corrélation et commentaire
def bivariate_analysis(df, column1, column2):
    
    """
    Effectue une analyse bivariée entre deux colonnes d'un DataFrame et fournit des commentaires.

    :param df: Le DataFrame contenant les données.
    :param column1: Nom de la première colonne à analyser.
    :param column2: Nom de la deuxième colonne à analyser.
    """
    correlation = df[column1].corr(df[column2])

    if correlation > 0.7:
        comment = "Il existe une forte corrélation positive entre les deux colonnes.", column1, "et",column2
    elif correlation < -0.7:
        comment = "Il existe une forte corrélation négative entre les deux colonnes.", column1, "et",column2
    elif correlation > 0.3:
        comment = "Il existe une corrélation positive modérée entre les deux colonnes.", column1, "et",column2
    elif correlation < -0.3:
        comment = "Il existe une corrélation négative modérée entre les deux colonnes.", column1, "et",column2
    else:
        comment = "Il y a peu de corrélation entre les deux colonnes.", column1, "et",column2
        
    return (correlation, comment)


################### PARTIE 1


######Question 1

def top10_popularite(df_art):
    
    #trier le DF par ordre décroissant en fonction des valeurs de la colonne "popularity"
    df_art_pop = df_art.sort_values(by='popularity', ascending=False).head(10) 
    #selectionner les colonnes appropriées puis trier par followers decroissant
    df_top10_popularite = df_art_pop[['name','popularity', 'followers']].sort_values(by='followers', ascending=False)
    #en faire un graphique
    plt.bar(df_top10_popularite['name'],df_top10_popularite['followers'], color= cm.rainbow(np.linspace(0, 1, len(df_top10_popularite))))
    plt.xticks(rotation=45)
    plt.xlabel('Noms des artistes')
    plt.ylabel('Nombre de followers')
    plt.title('Classement décroissant des 10 artistes les plus populaires  par leur nombre de followers ')
    plt.show
    
    return  df_top10_popularite


#######Question 2

def chansonparannee():
    
    #On s'assure que la colonne de date a le bon format
    df_track["release_date"] = pd.to_datetime(df_track["release_date"], format="%Y-%m-%d")
    #Puis, on extrait l'année pour avoir un graphique plus simple
    df_track["release_year"] = df_track["release_date"].dt.strftime('%Y')
    #On cherche le nombre de sortie par an en les comptant
    nb_sortie_par_an = df_track.groupby("release_year").agg({"id": "count"})

    #Notre graphique
    plt.figure(figsize=(22, 10))
    plt.plot(nb_sortie_par_an.index, nb_sortie_par_an.values, marker='o', linestyle='--', color='magenta')
    plt.xlabel('Années')
    plt.xticks(rotation=45) #pour rendre les années plus lisibles
    plt.ylabel('Nombre de morceaux sortis')
    plt.title('Nombre de morceaux sortis chaque année')
    plt.show()
    
    display(nb_sortie_par_an)
    return 


#######Question 3

def chansonsdistinctes():
    
    sommestream = df_top200.groupby("Artist")["Streams"].sum().reset_index()
    #On regroupe les tires distincts des chansons par artistes.
    singleparartiste = df_top200.groupby("Artist")["Title"].nunique().reset_index()
    #Pour renommer le nom des colonnes du tableau
    singleparartiste.columns = ["Artist", "Nombre de single dans le top200"]

    #On va maintenant fusionner sommestream et singleparartiste avec la clé de fusion "Artist".
    merged_df = singleparartiste.merge(sommestream, on='Artist')
    #Puis on trie le résultat obtenu par de telle sorte avoir les plus streamés d'abord
    merged_df_2 = merged_df.sort_values(by= ['Nombre de single dans le top200', 'Streams'], ascending=[False, False])
    
    #Graphique top 10 artistes qui ont le plus de chansons distinctes dans le top 200
    top_10_artistes = merged_df_2.head(10)
    plt.figure(figsize = (12,8))
    plt.bar(top_10_artistes["Artist"],top_10_artistes["Nombre de single dans le top200"], color = "magenta")
    plt.xlabel("Noms des artistes")
    plt.xticks(rotation=45)
    plt.ylabel("Nombre de morceaux distincts dans le top200")
    plt.title("Top 10 des artistes avec le plus de morceaux distincts dans le Top 200 Spotify")
    plt.show()
    
    display(merged_df_2,merged_df_2.head(10))

    return 


#######Question 4


def correlation_pop(df, col1, col2):
    
    correlation = fusion[[col1] + list(col2)].corr()[col1]
    
    df_correlation = pd.DataFrame({"Variable": correlation.index, "Correlation": correlation.values})
    
    print(visualize_correlation(fusion))
    
    #On va parcourir chauqe ligne dans le dataframe df_correlation, puis extraire les colonnes qui nous interessent : colonne "variable" ainsi que la colonne "correlation"
    #index contient l'indice de la ligne actuelle, tandis que row contient les données de cette ligne sous forme d'objet
    for index, row in df_correlation.iterrows():
        variable = row["Variable"]
        correlation_value = row["Correlation"]
    
        # On effectue nos conditions
        if pd.isnull(correlation_value):
            commentaire = "Il n'y a pas de corrélation pour {}.".format(col1)
        elif correlation_value > 0.8:
            commentaire = "Il existe une forte corrélation positive avec {}.".format(col1)
        elif correlation_value < -0.8:
            commentaire = "Il existe une forte corrélation négative avec {}.".format(col1)
        elif correlation_value > 0.3:
            commentaire = "Il existe une corrélation positive modérée avec {}.".format(col1)
        elif correlation_value < -0.3:
            commentaire = "Il existe une corrélation négative modérée avec {}.".format(col1)
        else:
            commentaire = "Il y a peu de corrélation avec {}.".format(col1)

        print("Pour la variable {}, la corrélation avec {} est de {}. {}\n".format(variable, col1, correlation_value, commentaire))
    
    return




























