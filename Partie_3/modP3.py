""" BIENVENUE DANS NOTRE PARTIE 3 :) """

""" Dans cette partie, nous créons une interface graphique permettant à 
l'utilisateur d'obtenir des informations précises sur l'ariste, le titre ou 
l'année/genre de son choix. Nous n'avons malheureusement pas réussi a relié le 
code de cette partie 3 au module 'modpart2' pour en importer plus simplement
les fonctions des questions de la partie 2. Nous avons donc dû copier coller les
fonctions directement sur ce script en modifiant la question 3."""

#Nous étions positionnés dans la partie 2 au niveau du chemin, 
#on execute le code pour accéder à la partie 3 dans le chemin.
import os 

current_path = os.getcwd()
path = os.path.abspath(os.path.join(current_path, '..'))
path_part3 = os.path.join(path, 'Partie_3')
os.chdir(path_part3)
print(os.getcwd())

import pandas as pd
import tkinter as tk
from tkinter import ttk #donne accès à des widgets
import webbrowser
import cleaning as cl
df_art, df_track, df_top200, singleparartiste = cl.clean()

" Réecriture de la partie 1 "
## QUESTION 1

def recherchenom(nom):
    '''
    recherchenom(nom): en fonction du nom d'artiste donné par l'utilisateur,
    la fonction rassemble les informations telles que le nombre de followers, les 3 chansons les
    plus populaires, les 3 chansons les plus récentes et le nombre de chansons dans le top 200
    global de 2020.
    
    input: nom
    
    output: nombre de followers de l'artiste, les 3 chansons les plus populaires, 
    les 3 chansons les plus récentes et le nombre de chansons dans le top 200 global de 2020.
    '''
    
    ##DF_ART
    #sélectionne les lignes de df_art où le nom artiste = titre donné 
    flwrs = df_art[df_art['artists'].str.lower() == nom.lower()]['followers']
    nb_abos = None #initialise nb_abos a None (on ne lui attribut pas de valeur spécifique)
    
    #si flwrs est non vide, le nombre d'abonnés = 1ère valeur de flwrs (col followers)
    
    if not flwrs.empty:
        nb_abos = flwrs.values[0]
        
    ##DF_TRACK   
    #sélectionne les lignes de df_art où le nom artiste = titre donné 
    nom_idtq = df_track[df_track['artists'].str.lower() == nom.lower()]
    
    #initialise pop et recence à None 
    pop = None
    recence = None
        
    #si 'nom_idtq' est pas vide on :
    if not nom_idtq.empty:
        ##trie les nom_idtqx par popularité décroissante (+ populaire au - populaire)
        pop = nom_idtq.sort_values(by='popularity', ascending=False).head(3)[['name', 'popularity']]
        #trie les singles par année de sortie décroissante (+ récent au + ancien)
        recence = nom_idtq.sort_values(by='release_year', ascending=False).head(3)[['name', 'release_year']]
    
    ##DF_singleparartiste
    
    #sélectionne les lignes de singleparartiste où le nom artiste = titre donné
    top1 = singleparartiste[singleparartiste['Artist'].str.lower() == nom.lower()]
    nb_chansons = None #initialise nb_chansons à None 
    if not top1.empty: #si 'nom_idtq' est non vide (càd a trouvé le même nom dans la colonne) on :
        #compte le nb de chansons dans le top1 de l'artiste du nom donné
        nb_chansons = top1["Nombre de single dans le top200"].values[0]
    
    #si le nom n'est pas trouvé dans la colonne noms -> toutes les variables sont vides
    if nb_abos is None and pop is None and recence is None and nb_chansons is None:
        print("Aucune information n'est donnée pour cet artiste :(")
        return None, None, None, None
    
    print(nom, "a", nb_abos, "followers.\n", "Ses chansons les plus populaires sont \n", pop, "\n et ses chansons les plus récentes sont\n", recence, "\nCet artiste a", nb_chansons, "dans le top200 global 2020.")

    return nb_abos, pop, recence, nb_chansons

## Question 2

def recherchetitre(titre):
    
    '''
    recherchetitre(titre): en fonction du titre donné par l'utilisateur, la 
    fonction cherche dans le df track et retourne les 20 premiers résultats qui 
    correspondent à ce titre en les ordonnant par popularité décroissante.
    
    input : titre
    
    output : 20 premières chansons qui ont ce titre
    
    '''
    #sélectionne les lignes où le titre du nom_idtq = titre donné
    titre_idtq = df_track[df_track['name'].str.lower() == titre.lower()]

    if titre_idtq.shape[0] == 0: #si le titre n'est pas présent dans df_track
        return "Aucun résultat correspondant à la chanson entrée. Veillez à respecter la casse en entrant le nom"
    
    #Si titre trouvé on trie le df 'titre_idtq' en fonction de la popularité décroissante
    titre_idtq = titre_idtq.sort_values(by='popularity', ascending=False)
    
    return titre_idtq.head(20)

## Question 3

def rechercheag(annee, genre):
    '''
    rechercheag(annee, genre) : trouve les titres correspondants à une année et
    un genre donnés par l'utilisateur, puis les retourne par popularité
    décroissante.
    
    inputs : année & genre donnés l'utilisateur

    output: DataFrame contenant les titres correspondantà l'annéé et le genre 
    donnés' par popularité décroissante
    '''
    #on garde les colonnes qui nous intéressent dans nos dataframes :
    tab_art = df_art[['id', 'genres','popularity']] 
    tab_track = df_track[['name', 'id_artists', 'release_date', 'artists']]
    
    ##Df_track : on crée un colonne année de sortie 
    tab_track['release_date'] = pd.to_datetime(df_track['release_date'], format="%Y-%m-%d")
    tab_track['release_year'] = tab_track['release_date'].dt.strftime('%Y') 
    #on supprime la colonne avec date complète : ne nous sert pas (axis=1 supprime une colonne)
    tab_track = tab_track.drop("release_date", axis=1)
    
    ##fusion de nos 2 daataframes avec la clé "artists"
    #on fusionne tab_art (clef de fusion : id) & tab_track (clef de fusion : id_artists)
    #outer : type de fusion qui conserve toutes les lignes
    fusion = pd.merge(tab_art, tab_track, left_on='id', right_on='id_artists', how='outer')
    
    #tri de l'artiste le + populaire au - populaire
    fusion = fusion.sort_values(by='popularity', ascending=False) 
    
    ##créer une liste vide qui va stocker nos lignes resultats
    #initialement nous ne voulions pas cette méthode qui est lente (problème expliqué dans le rapport)
    liste_resultat = []  
    
    #mise en place d'une boucle qui itère chaque ligne du df fusionné et vérifie
    #si les valeurs de 'année' et 'genre' données sont présentes. Si elles le sont
    #on stocke ces ligne dans la liste_resultat

    for index, row in fusion.iterrows():
        if str(row['genres']).lower() == genre.lower() and str(row['release_year']) == str(annee):
            liste_resultat.append(row[['name', 'artists','popularity']])

    #si la liste n'est pas vide alors on retransforme celle-ci en dataframe avec les lignes 
    if len(liste_resultat) > 0:
        return pd.DataFrame(liste_resultat, columns=['name','artists', 'popularity'])
    else:
        return pd.DataFrame(columns=['name', 'artists','popularity'])



""" CREATION DE L'INTERFACE GRAPHIQUE """
"""Paramètres de l'interface graphique """



ig = tk.Tk() #création de la fenêtre principale (interface graphique)
ig.title("Interface de données Spotify")
ig.geometry("1000x600") #définir les dimensions de la fenêtre
ig.configure(bg="#1ed65f") #définir la couleur du fond
ig.iconbitmap("Spotify_logo.ico") #changer le petit logo

##message de bienvenue
welcome = tk.Label(ig, text="Bienvenue dans notre \n interface graphique ! :) ", font=("Gotham Bold", 14), bg="#1ed65f", fg="white")
#place welcome en haut à gauche en le décalant des bords
welcome.grid(row=0, column=0, padx=20, pady=20, sticky='nw')

#créer les labels (se situent avant les champs) pour chaque info à donner
artiste = tk.Label(ig, text="Artiste :", font=("Gotham Bold", 12), bg="#1ed65f", fg="white")
titre = tk.Label(ig, text="Titre :", font=("Gotham Bold", 12), bg="#1ed65f", fg="white")
annee = tk.Label(ig, text="Année :", font=("Gotham Bold", 12), bg="#1ed65f", fg="white")
genre = tk.Label(ig, text="Genre :", font=("Gotham Bold", 12), bg="#1ed65f", fg="white")
#Label(fenêtre où  placer les labels, police, couleur du fond, couleur de l'écriture)


champ_art = tk.Entry(ig, width=20) #champ où entrer le nom de l'artiste
champ_morc = tk.Entry(ig, width=20) #champ où entrer le titre
champ_gen = tk.Entry(ig, width=25)#champ où entrer l'année
champ_an = tk.Entry(ig, width=20) #champ où entrer le genre 

#placer les labels sur la grille de notre fenêtre
artiste.grid(row=0, column=0, padx=3, pady=5) 
titre.grid(row=1, column=0, padx=3, pady=5)
annee.grid(row=0, column=2, padx=3, pady=5)
genre.grid(row=1, column=2, padx=3, pady=5)
#explication label artiste : 1ère ligne, 1 ère colonne, décalage de 3 unité par 
#rapport à l'axe des abscisses et de 5 unités par rapport à l'axe ordonnées

#positionner les champs de saisie sur la grille de notre fenêtre
champ_art.grid(row=0, column=1, padx=7, pady=5)
champ_morc.grid(row=1, column=1, padx=7, pady=5)
champ_an.grid(row=0, column=3, padx=7, pady=5)
champ_gen.grid(row=1, column=3, padx=7, pady=5)

nb_abos = 0
nb_chansons = 0

""" fonction associées aux boutons """
""" Pour les étapes ci-dessous nous allons utiliser des widgets Treeview de la 
librairie Tkinter. Ce sous module Treeview permet d'afficher des données sous 
forme d'un tableau interactif"""

def recherchenom_btn():
    
    """
    
    recherchenom_btn() : à partir d'un nom d'artiste entré dans le champ par
    l'utilisateur, lorsqu'il clique sur le bouton 'recherche par artiste',
    la fonction va retourner dans les tableaux d'un onglet : les 3 nom_idtqx les 
    plus populaires, les 3 les plus récents et le nombre d'abonnés de l'artiste
    
    input :
    output : remplissage du tableau avec les données trouvées dans la question 1
    de la partie 2.
    
    """
    #enlever les données du tableau tab_popu liées à la recherche précédente
    for child in tab_popu.get_children():
        tab_popu.delete(child)
    
    #enlever les données du tableau tab_rec liées à la recherche précédente
    for child in tab_rec.get_children():
        tab_rec.delete(child)


    artist = champ_art.get().lower() #récupère le nom entré par l'utilisateur en minuscules
    #appelle la fonction 'recherchenom' avec en paramètre le nom donné par l'utilisateur dans le champ
    nb_abos, pop, recence, nb_chansons = recherchenom(artist)
    
    if nb_abos is None: #si le nombre de followers de l'artiste n'est pas trouvé
        nb_abos_text.config(text="Le nombre d'abonnés n'est pas renseigné pour cet artiste")
    else: #sinon on les affiche dans les widgets :
        nb_abos_text.config(text="Nombre de followers : " + str(nb_abos))
        nb_chansons_text.config(text="Nombre de morceaux dans le top 200 global : " + str(nb_chansons))

    
    ##popularité
    if pop is not None: #si les chansons les + populaires sont trouvées
        for index, row in pop.iterrows(): #pour chaque tuple (index,ligne (serie de la ligne))
            tab_popu.insert("", "end", values=tuple(row)) #on l'insère dans le tableau
            #.insert(mettre les donnés au début du tableau, mettre nouvelle données
            #à la fin, quelles données mettre)
    else:
        print("Aucune donnée de popularité à afficher") 
   ##récence
    if recence is not None: #si les chansons les + récentes sont trouvées
        for index, row in recence.iterrows(): #pour chaque tuple (index,ligne (serie de la ligne))
            tab_rec.insert("", "end", values=tuple(row)) #on insère le tuple dans le tableau
    else:
        print("Aucune donnée de récence à afficher")

def recherchetitre_btn():
    """
    
    recherchetitre_btn() : à partir d'un titre entré dans le champ par l'utilisateur, 
    lorsqu'il clique sur le bouton 'recherche par titre', la fonction va retourner 
    dans les tableaux de l'onglet 2 tous les morceaux qui ont ce titre et leurs informations.
    
    input :
    output : remplissage du tableau avec les données trouvées dans la question 2
    de la partie 2.
    
    """
    
    #enlever les données du tableau tab_titre liées à la recherche précédente
    for child in tab_titre.get_children():
        tab_titre.delete(child)
      
    title = champ_morc.get() #récupère le titre entré par l'utilisateur en minuscules 
    #appelle la fonction 'recherchetitre' avec en paramètre le titre donné dans le champ
    morc_titre = recherchetitre(title)
    
    if not morc_titre.empty: #si le dataframe morc_titre n'est pas vide (on a trouvé au - un titre correspondant)
        for index, row in morc_titre.iterrows(): #pour chaque tuple (index,ligne (serie de la ligne))
            tab_titre.insert("", "end", values=tuple(row)) #on l'insère dans le tableau
    else: #si pas de morceau  correspondant au titre :
        erreur_titre.config(text="Aucun résultat correspondant à la chanson entrée")

def rechercheag_btn():
    """
    
    rechercheag_btn() : à partir d'une année et un genre entrés dans le champ 
    par l'utilisateur, lorsqu'il clique sur le bouton 'recherche par année et genre', 
    la fonction va retourner dans les tableaux de l'onglet 3 tous les morceaux 
    de l'année et du genre en question.
    
    input :
    output : remplissage du tableau avec les données trouvées dans la question 3
    de la partie 2.
    
    """
    #enlever les données du tableau tab_titre liées à la recherche précédente
    for child in tab_ag.get_children():
        tab_ag.delete(child)

    annee = int(champ_an.get()) #récupère l'année entrée par l'utilisateur en integer
    genre = str(champ_gen.get()) #récupère le genre entré par l'utilisateur en string
    
    #appelle la fonction 'rechercheag' avec en paramètres l'année et genre donnés dans le champ
    morc_ag = rechercheag(annee, genre)
    
    #si morc_ag a des données valides et est pas vide 
    #(on a trouvé au - une anné et un genre correspondant)
    if morc_ag is not None and not morc_ag.empty:
        for index, row in morc_ag.iterrows(): #pour chaque tuple (index,ligne (serie de la ligne))
            tab_ag.insert("", "end", values=tuple(row)) #on l'insère dans le tableau
    else: #si pas d'année et genre correspondant à ce donnés :       
        erreur_ag.config(text="Aucune information pour ce genre et cette année trouvée ! :(")


"""CREATION DES WIDGETS """

##BOUTONS 
#CREATION
artiste_btn = tk.Button(ig, text="Recherche par artiste", command=recherchenom_btn, bg='white', fg="black") #bouton artiste 
titre_btn = tk.Button(ig, text="Recherche par titre", command=recherchetitre_btn, bg='white', fg="black") #bouton titre 
ag_btn = tk.Button(ig, text="Recherche par année et genre", command=rechercheag_btn, bg='white', fg="black") #bouton annee & genre 

#LOCALISER LES BOUTONS SUR LA FENETRES
artiste_btn.grid(row=3, column=0, pady=10)
titre_btn.grid(row=3, column=1, pady=10)
ag_btn.grid(row=3, column=2, pady=10)

##ONGLETS
onglets = ttk.Notebook(ig) #création d'un carnet qui contient plusieurs onglets
#création des 3 onglets dont on a besoin (1 par question) placé dans le carnet
ong1 = ttk.Frame(onglets)
ong2 = ttk.Frame(onglets)
ong3 = ttk.Frame(onglets)

##TABLEAUX
#COLONNES TABLEAUX
col_artiste = tuple(pd.Index(['name', 'popularity'])) #tuple de colonnes pour le tableau artiste (q1) 
col_titre = tuple(df_track.columns) #tuple de colonnes pour le tableau titre (q2) 
#contenant les même colonnes que le df_track
col_ag = tuple(pd.Index(['name', 'artists','popularity']))#tuple de colonnes pour le tableau annee/genre (q3) 
 
#on fait des tuples car ils sont inchangeables une fois crées

#WIDGET TREEVIEW (TABLEAUX)
tab_popu = ttk.Treeview(ong1, columns=col_artiste, show='headings', height=3)
#ttk.Treeview(onglet où placer, colonnes définies, montrer que les en-têtes, 
#longueurs de 3 lignes max (puisque 3 chansons les + populaires))
tab_rec = ttk.Treeview(ong1, columns=col_artiste, show='headings', height=3)
tab_titre = ttk.Treeview(ong2, columns=col_titre, show='headings')
tab_ag = ttk.Treeview(ong3, columns=col_ag, show='headings')

##EN-TÊTES DES COLONNES DES TABLEAUX
for col in col_artiste: #boucle qui itère chaque colonnes
    tab_popu.heading(col, text=col)
    tab_titre.heading(col, text=col)
    tab_rec.heading(col, text=col)

for col in col_titre:
	tab_titre.heading(col, text=col)

for col in col_ag:
	tab_ag.heading(col, text=col)

##BARRES DE DEFILEMENTS
##Dans le cas des tableaux titre et ag, les longueurs sont infinies. On doit
#donc pouvoir défiler jusqu'en bas dans les tableaux pour voir tous les résultats
barreverti2 = ttk.Scrollbar(ong2, orient="vertical", command=tab_titre.yview)
barreverti3 = ttk.Scrollbar(ong3, orient="vertical", command=tab_ag.yview)
#les barres de défilement touchent tous les tableaux
barrehorizpopu = ttk.Scrollbar(ong1, orient="horizontal", command=tab_popu.xview)
barrehorizrec = ttk.Scrollbar(ong1, orient="horizontal", command=tab_rec.xview)
barrehoriztitre = ttk.Scrollbar(ong2, orient="horizontal", command=tab_titre.xview)
barrehorizag = ttk.Scrollbar(ong3, orient="horizontal", command=tab_ag.xview)
#ttk.Scrollbar(onglet où la mettre, orientation de la barre, type de défilement (gauche/droite ou haut/bas))

#lien avec les tableaux
tab_titre.configure(yscrollcommand=barreverti2.set, xscrollcommand=barrehoriztitre.set)
tab_ag.configure(yscrollcommand=barreverti3.set, xscrollcommand=barrehorizag.set)
tab_popu.configure(xscrollcommand=barrehorizpopu.set)
tab_rec.configure(xscrollcommand=barrehorizrec.set)
#placer les barres de défilement dans les tableaux (en haut/bas ou à gauche/droite)
barreverti2.pack(side="right", fill="y")
#ici on place la barre à droite du tableau et remplissent verticalement l'espace
barreverti3.pack(side="right", fill="y")
barrehorizrec.pack(side="bottom", fill="x")
barrehorizpopu.pack(side="bottom", fill="x")
barrehoriztitre.pack(side="bottom", fill="x")
barrehorizag.pack(side="bottom", fill="x")

##TABLEAUX DANS ONGLETS
tk.Label(ong1, text="Les 3 chansons les plus populaires de l'artiste").pack()
#mettre un nom de tableau dans onglet 1 et le nommer.
tab_popu.pack(expand=True, fill="both")
#tableau associé au nom ci-dessus
tk.Label(ong1, text="Les 3 chansons les plus récentes de l'artiste").pack(fill='both')
tab_rec.pack(expand=True, fill="both")
tab_titre.pack(expand=True, fill="both") 
#.pack(espace que le tableau doit prendre dans l'onglet, prend l'espace vertical et horizontal)
tab_ag.pack(expand=True, fill="both")

##INFORMATIONS SUPPLEMENTAIRES QUESTION 1
#On place les informations supplémentaires dans leurs onglets respectifs
nb_abos_text = tk.Label(ong1, text="Nombre d'abonnés : " + str(nb_abos))
nb_chansons_text = tk.Label(ong1, text="Nombre de chansons dans le top 200 global : " + str(nb_chansons))
nb_abos_text.pack()
nb_chansons_text.pack() 

##MESSAGES ERREURS 
#dans les fonction 2 et 3 on a des messages d'erreurs en cas de non correspondance
#on les place dans leurs onglets respectifs et on les initialise vide
erreur_titre = tk.Label(ong2, text="")
erreur_ag = tk.Label(ong3, text="")
erreur_titre.pack()
erreur_ag.pack()

##PLACER LES ONGLETS DANS LE CARNET
onglets.add(ong1, text='Informations par artiste')
onglets.add(ong2, text='Informations par titre')
onglets.add(ong3, text='Informations par année et genre')

##PLACER LE CARNET DANS LA FENETRE
onglets.grid(row=5, column=0, columnspan=4, padx=10, pady=10)

##AJUSTEMENT AUTOMATIQUE DU CONTENU QUAND LA FENTRE CHANGE DE TAILLE
ig.columnconfigure(0, weight=1)

def wikipedia():
    
    """
    open_wikipedia(): lorsque l'utilisateur entre un nom d'artiste dans le champ
    associé et qu'il clique sur le bouton 'ouvrir wikipédia', la fonction s'exécute
    et permet d'ouvrir une fenêtre sur internet redirigeant l'utilisateur sur la page 
    wikipédia de l'artiste
    
    input :
    output : redirige vers la page wikipédia de l'artiste
        
    """
    
    #on défini le lien à ouvrir : on recupère le nom écrit par l'utilisateur et 
    #on met la 1ère lettre de chaque mot en majuscule et met en liste le nom obtenu ['Justin', 'Bieber']
    #on met le tout dans '.join' pour obtenir : "Justin_Bieber" associé à l'url de Wikipédia
    
    lien_wiki = f"https://fr.wikipedia.org/wiki/{'_'.join(champ_art.get().title().split(' '))}"
    webbrowser.open(lien_wiki)

def spotify():
    
    """
    open_wikipedia(): lorsque l'utilisateur entre un nom d'artiste dans le champ
    associé et qu'il clique sur le bouton 'ouvrir spotify', la fonction s'exécute
    et permet d'ouvrir une fenêtre sur internet redirigeant l'utilisateur sur la page 
    spotify de l'artiste
    
    input :
    output : redirige vers la page spotify de l'artiste
        
    """
    #on défini le lien à ouvrir : on recupère le nom écrit par l'utilisateur et 
    #on met la 1ère lettre de chaque mot en majuscule et met en liste le nom obtenu ['Justin', 'Bieber']
    #on met le tout dans '.join' pour obtenir : "Justin_Bieber" associé à l'url de Spotify
    lien_spot = f"https://open.spotify.com/search/{'_'.join(champ_art.get().title().split(' '))}"
    webbrowser.open(lien_spot)

##CREATION ET PLACEMENT DES BOUTONS WIKIPEDIA ET SPOTIFY
wikipedia_btn = tk.Button(ong1, text="Ouvrir Wikipedia", command=wikipedia)
wikipedia_btn.pack()
spotify_btn = tk.Button(ong1, text="Ouvrir Spotify", command=spotify)
spotify_btn.pack()

#lance la boucle principale
ig.mainloop()
