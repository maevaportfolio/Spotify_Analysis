"""" BIENVENUE DANS NOTRE PARTIE 2 """

""" 

Ce ficher comporte la réalisation des question 1, 2 et 3 de la partie 2
en faisant appel au module nécessaire (modpart2)

"""

#Chemin relatif

import os 
current_path = os.getcwd()
path = os.path.abspath(os.path.join(current_path, '..'))
path_part2 = os.path.join(path, 'Partie_2')
os.chdir(path_part2)
print(os.getcwd())

#QUESTION 1 :

import modP2 as P2

def question1():
    
    '''
    question1() : fonction a pour but de répondre à la question 1 en exécutant
    les fonctions rechercheart, recherchetrack et recherchetop du module modpart2.
    
    input : 
    output : pour un nom d'artiste donné par l'utilisateur, le programme retourne
    son nombre d’abonnés, les 3 chansons les plus populaires, les 3 chansons les 
    plus récentes ainsi que le nombre de chansons qu’il a dans le top 200 global 
    de 2020 (s’il y en a).
    
    '''
    
    P2.recherchenom()
    
    return


question1()

#QUESTION 2 :

def question2 ():
    
    '''
    question2() : fonction a pour but de répondre à la question 2 en exécutant
    la fonction recherchetitre du module modpart2.
    
    input : 
    output : pour un titre donné par l'utilisateur, le programme retourne les 20
    premiers résultats qui correspondente en les ordonnant par popularité
    décroissante. 
    
    '''
    #demander à l'utilisateur d'entrer un titre

    #appelle la fonction recherchetitre du module modpart2
    sortie = P2.recherchetitre()
    print(sortie)
    
    return

question2()

#QUESTION 3 :

def question3():
    
    '''
    question3() : fonction a pour but de répondre à la question 3 en exécutant
    la fonction lookby_year_genre du module modpart2.
    
    input : 
    output : retourne les chansons correspondant à une année et un genre, donnés
    par l'utilisateur, par popularité d’artiste décroissante. Si un artiste a 
    plusieurs chansons celes-ci sont ordonnées par popularité décroissante

    '''

    P2.lookby_year_genre()
    return

question3()

#exemple 1 : vous pouvez essayer 1962 et vintage tango
#exemple 2 : vous pouvez essayer 2004 et chamame
#exemple 2 : vous pouvez essayer 2019 et Aucun