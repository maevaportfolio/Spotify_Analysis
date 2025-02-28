""" BIENVENUE DANS NOTRE MODULE POUR LA PARTIE 2 :)"""


""" 

Ce ficher est le module comportant les fonctions permettant de répondre
à la partie 2 du projet. Il lui-même au module 'cleaning' qui permet
de nettoyer les données.

"""

#Chemin relatif pour se placer dans la partie_2
import os 

current_path = os.getcwd()
path = os.path.abspath(os.path.join(current_path, '..'))
path_part2 = os.path.join(path, 'Partie_2')
os.chdir(path_part2)
print(os.getcwd())

import pandas as pd
import cleaning as cl
df_art, df_track, df_top200, singleparartiste = cl.clean()

""" LES FONCTIONS """

""" QUESTION 1 """

def recherchenom():
    '''
    obtenir_informations_artiste(nom): en fonction du nom d'artiste donné par l'utilisateur,
    la fonction rassemble les informations telles que le nombre de followers, les 3 chansons les
    plus populaires, les 3 chansons les plus récentes et le nombre de chansons dans le top 200
    global de 2020.
    
    input: nom
    
    output: nombre de followers de l'artiste, les 3 chansons les plus populaires, 
    les 3 chansons les plus récentes et le nombre de chansons dans le top 200 global de 2020.
    '''
    nom = input("Veuillez entrer un nom d'artiste s'il vous plaît :")
    if not isinstance(nom, str):
        print("Erreur ! Le nom de l'artiste doit être une chaîne de caractère.")
    
    # Recherche du nombre de followers de l'artiste
    flwrs = df_art[df_art['artists'].str.lower() == nom.lower()]['followers']
    nb_abos = None
    if not flwrs.empty:
        nb_abos = flwrs.values[0]
        
    # Recherche des chansons populaires et récentes
    morceau = df_track[df_track['artists'].str.lower() == nom.lower()]
    pop = None
    recence = None
    if not morceau.empty:
        pop = morceau.sort_values(by='popularity', ascending=False).head(3)[['name', 'popularity']]
        recence = morceau.sort_values(by='release_year', ascending=False).head(3)[['name', 'release_year']]
    
    # Recherche du nombre de chansons dans le top 200 global de 2020
    artiste_data = singleparartiste[singleparartiste['Artist'].str.lower() == nom.lower()]
    nb_chansons = None
    if not artiste_data.empty:
        nb_chansons = artiste_data["Nombre de single dans le top200"].values[0]
    
    print(nom, "a", nb_abos, "followers.\n", "Ses chansons les plus populaires sont \n", pop, "\n et ses chansons les plus récentes sont\n", recence, "\nCet artiste a", nb_chansons, "dans le top200 global 2020.")

    return 

if __name__ == "__main__":
    recherchenom()


"""QUESTION 2"""

def recherchetitre():
    
    '''
    recherchetitre(): en fonction du titre donné par l'utilisateur, la 
    fonction cherche dans le df track et retourne les 20 premiers résultats qui 
    correspondent à ce titre en les ordonnant par popularité décroissante.
    
    
    input : titre
    
    output : 20 premières chansons qui ont ce titre
    
    '''
    titre = input("Veuillez entrer un titre s'il vous plaît :")
    if not isinstance(titre, str):
        print("Erreur ! Le titre doit être une chaîne de caractère.")
    #sélectionne les lignes où le titre du morceau = titre donné
    titrecommun = df_track[df_track['name'].str.lower() == titre.lower()]

    if titrecommun.shape[0] == 0: #si le titre n'est pas présent dans df_track
        return "Aucun résultat correspondant à la chanson entrée. Veuillez respecter la casse en entrant le nom"
    
    #Si titre trouvé on trie le df 'titrecommun' en fonction de la popularité décroissante
    titrecommun = titrecommun.sort_values(by='popularity', ascending=False)
    
    return titrecommun.head(20)

if __name__ == "__main__":
    recherchetitre()


""" QUESTION 3 """ 

def lookby_year_genre():
    
    '''
    Cette fonction a pour but de demander à l'utilisateur de rentrer une année et
    un genre musical. Il lui sera retourné les titres correspondants par popularité
    décroissante.
    
    '''
    
    #On demande à l'utilisateur de rentrer une année et un genre
    year= input("Saisir une année :")
    genre= input("Saisir un genre : ")
    
    #On récupère l'id de l'artiste et le genre
    tab_art= df_art[['id','genres']]
    #On récupère tout ce qui nous importe de df_track
    tab_track=df_track[['name','popularity','id_artists','release_date','artists']]
    #on crée une colonne transformant la date en année uniquement
    tab_track['release_date'] = pd.to_datetime(df_track['release_date'], format="%Y-%m-%d")
    tab_track['release_year'] = tab_track['release_date'].dt.strftime('%Y') 
    #on supprime la colonne avec date complète : ne nous sert pas (axis=1 on supprime une colonne)
    tab_track= tab_track.drop("release_date", axis=1)
    
    #on fusionne nos 2 df en un avec la clé "artists"
    tab_at= pd.merge(tab_art, tab_track, left_on='id',right_on='id_artists', how='outer')
    #transforme la colonne genre qui est en liste, en chaine de caractère
    tab_at['genres'] = tab_at['genres'].astype(str)
    
    #filtre les données en fonction de l'année et du genre
    tab_at_yg = tab_at[(tab_at['release_year'] == year) & (tab_at['genres'].str.lower() == genre.lower())]
    #on trie  les données par popularité décroissante
    tab_at_ygp = tab_at_yg.sort_values(by=['popularity'], ascending=False)
    
    print("Voici les résultats selon l'année", year, "et le genre", genre)
    print(tab_at_ygp[['name', 'popularity','artists']])
    
    return

if __name__ == "__main__": #permet de lancer que si le module est le programme principal
    lookby_year_genre()
