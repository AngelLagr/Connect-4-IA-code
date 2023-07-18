import random as rd
import numpy as np
from math import inf
import copy
 

 
joueur = "X"
P4 = False

# Fonctions utiles 
def verif_colonne(col,M):
    '''vérifie si la colonne est valable, sinon, renvoie la première colonne à droite disponble'''
    while M[5][col] != " ":
        True==True
    return col

def colonne_disponible(M,col):
    '''retourne vrai ou faux suivant si la colonne est disponible'''
    return (M[5][col] == 0)
     
def ligne(colonne,M):
# Cette fonction retourne la ligne vide correspondant a la colonne demandee
    lig = 0
    for i in range (1,6):
        if ( M[i][colonne] == " " and M[i-1][colonne] != " " ):
            lig = i
    return lig

def verification_P4(M):
    '''teste si un joueur a gagné ou pas, renvoie le numéro du joueur le cas échéant'''
    vainqueur = " "
    for joueur in ["X","O"]:
        #teste toutes les possibilités en lignes
        for i in range(6):
            for j in range(4):
                if M[i][j] == joueur and M[i][j+1] == joueur and M[i][j+2] == joueur and M[i][j+3] == joueur:
                    vainqueur = joueur

        #teste toutes les possibilités en colonnes
        for j in range(7):
            for i in range(3):
                if M[i][j] == joueur and M[i+1][j] == joueur and M[i+2][j] == joueur and M[i+3][j] == joueur:
                    vainqueur = joueur
            
        #teste toutes les possibilités en diagonales montantes / et descendantes \
        for i in range(3):
            for j in range(4):
                if M[i][j] == joueur and M[i+1][j+1] == joueur and M[i+2][j+2] == joueur and M[i+3][j+3] == joueur:
                    vainqueur = joueur
                if M[i+3][j] == joueur and M[i+2][j+1] == joueur and M[i+1][j+2] == joueur and M[i][j+3] == joueur:
                    vainqueur = joueur

    return vainqueur

########################################################################################
# Différents niveaux de jeu

def niveau0(M):
    '''retourne une colonne aléatoire'''
    return rd.randint(0,5)

def niveau1(M):
    '''vérifie si peut gagner quelque part et y joue, sinon essaie de bloquer l'adversaire'''
    col = -1
    N=copy.deepcopy(M)
    for j in range(6):
        if N[j][0] == " ":
           
            N[j][0] = "O"
            gravite(N)
            if verification_P4(N) == "O":
                col = j
            N[j][N[j].index("O")] = " "    

    N=copy.deepcopy(M)
    if col == -1:
        for j in range(6):
            if N[j][0] == " ":
                
                N[j][0] = "X"
                gravite(N)
                if verification_P4(N) == "X":
                    col = j
                N[j][N[j].index("X")] = " " 

        if col == -1:
            return niveau0(M)
        else:
            return col
    else:
        return col

#Méthode minmax avec heuristiques
def heuristique(M):
    '''exemple d'heuristique : calcule le nombre d'endoit où le joueur peut gagner moins le nombre d'endroits où l'adversaire peut gagner '''
    heur = 0
    #teste toutes les possibilités en lignes
    for i in range(6):
        for j in range(4):
            if M[i][j] != "X" and M[i][j+1] != "X" and M[i][j+2] != "X" and M[i][j+3] != "X":
                heur +=1
            if M[i][j] != "O" and M[i][j+1] != "O" and M[i][j+2] != "O" and M[i][j+3] != "O":
                heur -=1


    #teste toutes les possibilités en colonnes
    for j in range(7):
        for i in range(3):
            if M[i][j] != "X" and M[i+1][j] != "X" and M[i+2][j] != "X" and M[i+3][j] != "X":
                heur +=1
            if M[i][j] != "O" and M[i+1][j] != "O" and M[i+2][j] != "O" and M[i+3][j] != "O":
                heur -=1

    #teste toutes les possibilités en diagonales montantes / et descendantes \
    for i in range(3):
        for j in range(4):
            if M[i][j] != "X" and M[i+1][j+1] != "X" and M[i+2][j+2] != "X" and M[i+3][j+3] != "X":
                heur +=1
            if M[i+3][j] != "X" and M[i+2][j+1] != "X" and M[i+1][j+2] != "X" and M[i][j+3] != "X":
                heur +=1
            if M[i][j] != "O" and M[i+1][j+1] != "O" and M[i+2][j+2] != "O" and M[i+3][j+3] != "O":
                heur -=1
            if M[i+3][j] != "O" and M[i+2][j+1] != "O" and M[i+1][j+2] != "O" and M[i][j+3] != "O":
                heur -=1

    return heur

def heuristique2(M):
        '''Heuristique un peu plus complexe'''
        somme = 0
        # colonnes
        for j in range(7):  #colonnes
            for i in range(3):  #lignes
                zone =[M[i][j], M[i+1][j], M[i+2][j], M[i+3][j]]
                if not("X" in zone) :
                    if zone.count("O") == 4:
                        somme += (1000)
                    else :
                        somme += zone.count(2)
                if not ("O" in zone) :
                    if zone.count("X") == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count("X")
        # lignes
        for i in range(6):     #lignes
            for j in range(4):  #colonnes
                zone = [M[i][j], M[i][j+1], M[i][j+2], M[i][j+3]]
                if not("X" in zone) :
                    if zone.count("O") == 4:
                        somme += (1000)
                    else :
                        somme += zone.count("O")
                if not ("O" in zone) :
                    if zone.count("X") == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count("X")
        # diagonales haut-droites
        for i in range(3):
            for j in range(4):
                zone = [M[i][j+3], M[i+1][j+2], M[i+2][j+1], M[i+3][j]]
                if not("X" in zone) :
                    if zone.count("O") == 4:
                        somme += (1000)
                    else :
                        somme += zone.count("O")
                if not ("O" in zone) :
                    if zone.count("X") == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count("X")
        # diagonales haut-gauches
        for i in range(3):
            for j in range(4):
                zone = [M[i+3][j+3], M[i+2][j+2], M[i+1][j+1], M[i][j]]
                if not("X" in zone) :
                    if zone.count("O") == 4:
                        somme += (1000)
                    else :
                        somme += zone.count("O")
                if not ("O" in zone) :
                    if zone.count("X") == 4:
                        somme -= (1000)
                    else :
                        somme -= zone.count("X")

        return somme

def list_minmax(M,profondeur,profondeur_initiale,liste):
    '''calcule la liste des heuristiques pour une profondeur donnée''' 
    if profondeur == 1:
        for col in range(7):
            if colonne_disponible(M,col):
                M[ligne(col)][col] = (profondeur_initiale - profondeur + 1)%2 +1
                liste.append(heuristique2(M))
                M[ligne(col)-1][col] = " " 
            else:
                liste.append(np.nan)
    else:
        liste_ce_niveau = list(liste)
        for col in range(7):
            if colonne_disponible(M,col):
                M[ligne(col)][col] = (profondeur_initiale - profondeur + 1)%2 +1
                liste.append(list_minmax(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
                M[ligne(col)-1][col] = " "
            else:
                liste.append(list_nan(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))

    return liste

def list_nan(M,profondeur,profondeur_initiale,liste):
    '''retrourne la liste de nan'''
    if profondeur == 1:
        for col in range(7):
            liste.append(np.nan)
    else:
        liste_ce_niveau = list(liste)
        for col in range(7):
            liste.append(list_nan(M,profondeur-1,profondeur_initiale,list(liste_ce_niveau)))
    return liste



def minmax(liste):
    '''applique l'algorithme minmax à la liste des états possibles du jeu futur'''
    if type(liste[0]) != list:
        return liste.index(vrai_max(liste)) 
    else:
        for i in range(len(liste)):
            liste[i] = min_spec(liste[i])
        return liste.index(vrai_max(liste))

def max_spec(liste):
    '''partie max recursive de l'algorithme'''
    if type(liste[0]) != list:
        return vrai_max(liste)
    else:
        for i in range(len(liste)):
            liste[i] = min_spec(liste[i])
        return max_spec(liste)


def min_spec(liste):
    '''partie min recursive de l'algorithme'''
    if type(liste[0]) != list:
        return vrai_min(liste)
    else:
        for i in range(len(liste)):
            liste[i] = max_spec(liste[i])
        return min_spec(liste)

def vrai_max(liste):
    '''retourne le maximum d'une liste avec des nan'''
    if liste == 7 * [np.nan]:
        return np.nan
    n = len(liste)
    maximum = -inf
    for i in range(n):
        element = liste[i]
        if type(element) == int and element>maximum:
            maximum = element
    return maximum

def vrai_min(liste):
    '''retourne le minimum d'une liste avec des nan'''
    if liste == 7 * [np.nan]:
        return np.nan 
    n = len(liste)
    minimum = inf
    for i in range(n):
        element = liste[i]
        if type(element) == int and element<minimum:
            minimum = element
    return minimum


def get_column(niveau,M):

    '''retourne la colonne où joue l'IA en fonction du niveau souhaité'''
    if int(niveau) == 0 :
        return niveau0() 
    elif int(niveau) == 1:
        return niveau1(M)
    elif int(niveau) > 1:
        return minmax(list_minmax(M,min(int(niveau)-1,4),min(int(niveau)-1,4),[]))

################################################################################
#Let's play !
def jouer_coupia(M):  
    colonne = get_column(1,M)
    print(f"\n COUP DE L'IAtest : {Alphabet[colonne]}")
    M[colonne][0] = "X"
    M=gravite(M)
    P4 = verification_P4(M)
    return P4=="X"
    

def gravite(grille):
    """
    Cree un str pour permettre d'enlever les cases vides puis concatene ce dernier afin de retrouver un str de la longeur du nombre de lignes
    Puis recree une liste de liste qui correspond a la bonne grille 
    Action de "gravite" sur les pions 
    
    Returns
    -------
    None
    """
    L=grille
    for i in range(6):
       
        chaine=''.join(L[i])
        chaine=chaine.replace(' ','')
        L[i]=[' ' for i in range(7-len(chaine))]+list(chaine)
    return L
 
def jouer_coup(coup_joue:str,M):  
    print(f"\n COUP DE L'IA VRAIE : {Alphabet[coup_joue]}")
    reward=0
    if M[coup_joue][0]!=" ":
        P4 = verification_P4(M)
        
        return False,-30, P4!=" ", 42 
    else:
        M[coup_joue][0]="O"
        M=gravite(M)
        P4 = verification_P4(M)
        reward=heuristique2(M)+heuristique(M)
        print("-------------------------",reward)
        return True, reward, P4!=" ", 42   
 
Alphabet="ABCDEF"

def affichage(etat)->None:
    """

    Parameters
    ----------
    arb : IA
        Sommet d'un arborescence.

    Returns
    -------
    None
        Retourne rien, affiche une grille correspondant à l'état du sommet.

    """
    print(" "+len(etat)*' -')
    for l in range(len(etat[0])):
        c="|"
        for p in range(len(etat)):
            c+=" "+etat[p][l]
        print(c+" |")
    c=" "
    for p in range(len(etat)):
        c+=f" {Alphabet[p]}"
    print(" "+len(etat)*' -')
    print(c)   
    
