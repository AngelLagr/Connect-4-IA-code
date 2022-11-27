import math as mt
import copy 
from random import randint
from tkinter import *
from tkinter import ttk
from copy import deepcopy
######################################################################

def dfs(arb):
    liste = [arb.__repr__()]
    for ss_arb in arb.get_sous_arb():
        liste.extend(dfs(ss_arb))
    return liste

######################################################################
Alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"
grilletest = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
class Puissance4:
    def __init__(self,grille, colonne=7,rangee=6,derniers_coups=["",""],bombes=[1,1],nombre_jetons_victoire=4):
        assert len(grille)==colonne and len(grille[1])==rangee
        self.grille=grille
        self.derniers_coups=derniers_coups
        self.colonne=colonne
        self.rangee=rangee
        self.nombre_jetons_victoire=nombre_jetons_victoire
        self.bombes=bombes
        self.pion=["X","O"]
                
    def victoire(self):
        """
        Retourne un tuple (plein, joueur) avec :
            plein : bool, True si la grille est pleine False sinon
            joueur : int, 0 si le joueur 0 gagne, 1 si le joueur 1 gagne, 2 sinon.
        """
        nombre=3
        plein=True
        for colonne in range(self.colonne): #on teste si la grille est pleine
            if self.grille[colonne].count(" ")!=0:
                plein=False      
                
        for colonne in range(self.colonne) : # on teste en ligne si des pions sont alignés en colonne
            chaine="".join(self.grille[colonne])
            if nombre != 3 and ((nombre != 1 and self.nombre_jetons_victoire*"X" in chaine) or (nombre != 0 and self.nombre_jetons_victoire*"O" in chaine)): # si joueur 1 a gagné ou que  joueur 2 a gagné
                return (plein,2)  
            if self.nombre_jetons_victoire*"O" in chaine:
                nombre=0           
            elif self.nombre_jetons_victoire*"X" in chaine:
                nombre=1  
                                   
        for ligne in range(self.rangee) : # on teste en ligne si des pions sont alignés en ligne
            chaine=""
            for colonne in range(self.colonne):
                chaine=chaine+self.grille[colonne][ligne] 
            if nombre != 3 and ((nombre != 1 and self.nombre_jetons_victoire*"X" in chaine) or (nombre != 0 and self.nombre_jetons_victoire*"O" in chaine)): # si joueur 1 a gagné ou que  joueur 2 a gagné
                return (plein,2)  
            if self.nombre_jetons_victoire*"O" in chaine:
                nombre=0
            elif self.nombre_jetons_victoire*"X" in chaine:
                nombre=1  
                           
        for ligne in range(self.rangee) : # on teste en diagonale si des pions sont alignés
            chaine1=""
            chaine2=""
            j=0
            for colonne in range(self.colonne):            
                if ligne+j < self.rangee:
                    chaine1=chaine1+self.grille[colonne][ligne+j] 
                    
                if ligne-j < self.rangee and ligne-j>=0:
                    chaine2=chaine2+self.grille[colonne][ligne-j] 
                j=j+1
            if nombre != 3 and ((nombre != 0 and (self.nombre_jetons_victoire*"O" in chaine1 or self.nombre_jetons_victoire*"O" in chaine2)) or (nombre != 1 and (self.nombre_jetons_victoire*"X" in chaine1 or self.nombre_jetons_victoire*"X" in chaine2))):
                return (plein,2)
            if self.nombre_jetons_victoire*"O" in chaine1 or self.nombre_jetons_victoire*"O" in chaine2:
                nombre=0      
            elif self.nombre_jetons_victoire*"X" in chaine1 or self.nombre_jetons_victoire*"X" in chaine2:
                nombre=1

                        
        return (plein,nombre)
    def affichage(self):
        print(" "+self.colonne*' -')
        for l in range(self.rangee):
            c="|"
            for p in range(self.colonne):
                c+=" "+self.grille[p][l]
            print(c+" |")
        c=" "
        for p in range(self.colonne):
            c+=f" {Alphabet[p]}"
        print(" "+self.colonne*' -')
        print(c)
            
    def jouer_coup(self,coup_joue,joueur):
        if "*" == coup_joue[0]:
            if coup_joue[1] in Alphabet[0:self.colonne] and self.bombes[joueur]!=0:
                self.bombe(coup_joue[1])
                self.bombes[joueur]-=1
                self.dernier_coup_grille=coup_joue
                return True
            else:
                return False
            
        elif coup_joue[0] in Alphabet[0:self.colonne] and self.grille[Alphabet.index(coup_joue[0])][0]==" ":
            self.jouer_colonne(coup_joue[0],joueur)
            self.dernier_coup_grille=coup_joue
            return True
        
        else:
            return False
            
    def copie(self):
         return copy.deepcopy(self)       
##############################################################################
    def decalage_droit(self):
        """
        decale toutes les colonnes vers la droite
        ne retourne rien
        """
        nouvelle_liste=[["" for i in range(self.rangee)]for i in range(self.colonne)]
        for i in range(len(self.grille)-1):
            nouvelle_liste[i+1]=self.grille[i]
        nouvelle_liste[0]=self.grille[-1]
        self.grille=nouvelle_liste
        
    def decalage_gauche(self):
        """
        decale toutes les colonnes vers la gauche
        ne retourne rien
        """
        for i in range((self.colonne)-1):
            self.decalage_droit()         

     
    def bombe(self,colonne:str)->None:
        """
        colonnne est la colonne ou l'on va placer le pion bombe  type : str
        si les pions autour du pion bombe sont différent de " " alors ils sont remplaces par " "
        puis on utilise la fonction gravite pour faire "descendre" tout les pions qui n'aurait
        plus de pions en dessous d'eux
        """ 
        a=Alphabet.index(colonne)
        self.grille[a][0]="bombe"
        self.gravite()
        k = 0
        for i in range(self.rangee):
            if self.grille[Alphabet.index(colonne)][i]=="bombe":
                k=i

        if a==0 and k==0:
            for p in range(a,a+2):
                for q in range(k,k+2):
                    self.grille[p][q]=" "
        elif a==0 and k==self.rangee-1:
            for p in range(a,a+2):
                for q in range(k-1,k+1):
                    self.grille[p][q]=" "

        elif a==self.colonne-1 and k==0:
            for p in range(a-1,a+1):
                for q in range(k,k+2):
                    self.grille[p][q]=" "
        elif a==self.colonne-1 and k==self.rangee-1:
            for p in range(a-1,a+1):
                for q in range(k-1,k+1):
                    self.grille[p][q]=" "

        elif k==0:
            for p in range(a-1,a+2):
                for q in range(k,k+2):
                    self.grille[p][q]=" "
        elif k==self.rangee-1:
            for p in range(a-1,a+2):
                for q in range(k-1,k+1):
                    self.grille[p][q]=" "

        elif a==0:
            for p in range(a,a+2):
                for q in range(k-1,k+2):
                    self.grille[p][q]=" "
        elif a==self.colonne-1:
            for p in range(a-1,a+1):
                for q in range(k-1,k+2):
                    self.grille[p][q]=" "

        else:
            for p in range(a-1,a+2):
                for q in range(k-1,k+2):
                    self.grille[p][q]=" "
        self.gravite()
        
    def rotation_plus(self):
        """
        tourne la grille dans le sens direct (trigo) de 90Â°
        puis on utilise la fonction gravite pour faire "descendre" tout les pions qui n'aurait
        plus de pions en dessous d'eux 
        """
        L=self.m_transpose()
        for i in range(len(L)):
            for j in range(len(L)//2):
                L[i][j],L[i][len(L)-j]=L[i][len(L)-j],L[i][j]
        self.grille=L
        self.colonne,self.rangee=self.rangee,self.colonne
        self.gravite()        
        

    def rotation_moins(self):
        """
        tourne la grille dans le sens indirect (horaire) de 90Â°
        puis on utilise la fonction gravite pour faire "descendre" tout les pions qui n'aurait
        plus de pions en dessous d'eux 
        """
        L=self.m_transpose()
        for i in range(len(L)//2):
            L[i],L[len(L)-1-i]=L[len(L)-1-i],L[i]
        self.grille=L
        self.colonne,self.rangee=self.rangee,self.colonne
        self.gravite()
    
    @staticmethod
    def m_nulle(n,m):
        L=[0]*n
        for i in range(len(L)):
            L[i]=[0]*m
        return(L)
    @staticmethod
    def m_taille(L):
        n=len(L)
        m=len(L[0])
        return((n,m))

    def m_transpose(self):
        M=list(self.grille)
        n1,m1=self.m_taille(M)
        m,n=self.m_taille(M)
        L=self.m_nulle(n,m)
        for i in range(m1):
            for k in range(n1):
                L[i][k]=M[k][i]
        return(L)

#####################################################################         

    def jouer_colonne(self,colonne,joueur):
        """
        Parameters
        ----------
        colonne : str
            Colonne dans laquelle on veut mettre un pion.
        joueur : int
            Numéro du joueur.

        Returns
        -------
        None
            Ne retourne rien, modifie la colonne concernée.

        """
        if joueur==0:
            self.grille[Alphabet.index(colonne)][0]="O"
        else:
            self.grille[Alphabet.index(colonne)][0]="X"
        self.gravite()


    def gravite(self):
        """
        Prend une grille en paramètre et fait tomber tous les pions : effet de "gravité"

        Returns
        -------
        None, modifie la grille sur place

        """
        n=self.rangee-2 #quand l=0 pas de probleme d'indice
        for p in range(self.colonne):
            for l in range(self.rangee-1): #on veut pas verifier la ligne la plus haute car rien au dessus
                if self.grille[p][n-l]!=" " and self.grille[p][n-l+1]==" ":
                    k=n-l
                    while self.grille[p][k]!=" " and self.grille[p][k+1]==" ": #condition pour pouvoir le descendre jusqua rencontrer un caractere
                        if k==self.rangee-2:
                            self.grille[p][k],self.grille[p][k+1]=self.grille[p][k+1],self.grille[p][k]
                        else:
                            self.grille[p][k],self.grille[p][k+1]=self.grille[p][k+1],self.grille[p][k]
                            k+=1
                



class IA():
    def __init__(self,difficulte,etat,valeur=0,rangee=6,colonne=7,nombre_jetons_victoire=4,joueur=0,sous_arb=[]):
        self.__valeur=valeur
        self.__rangee=rangee
        self.__colonne=colonne
        self.__difficulte=difficulte
        if etat=="":
            self.__etat=[[" " for i in range(rangee)] for i in range(colonne)]
        else:
            self.__etat=etat
        self.__nombre_jetons_victoire=nombre_jetons_victoire
        self.__joueur=joueur
        self.__sous_arb=sous_arb[:]
        self.__valeur=0
        
        
    def get_etat(self):
        return self.__etat
    def set_etat(self,valeur):
        self.__etat=valeur
        
    def get_valeur(self):
        return self.__valeur
    def set_valeur(self,valeur):
        self.__valeur=valeur
    
    def get_nombre_jetons_victoire(self):
        return self.__nombre_jetons_victoire
    def set_nombre_jetons_victoire(self,valeur):
        self.__nombre_jetons_victoire=valeur
    
    def get_rangee(self):
        return self.__rangee
    def set__rangee(self,valeur):
        self.__rangee=valeur
    def get_colonne(self):
        return self.__colonne
    def set__colonne(self,valeur):
        self.__colonne=valeur
        
    def get_nombrejetons(self):
        return self.__nombre_jetons_victoire
    def set_nombrejetons(self,valeur):
        self.__nombre_jetons_victoire=valeur
    
    def get_joueur(self):
        return self.__joueur
    def set_joueur(self,valeur):
        self.__joueur=valeur
        
    def get_sous_arb(self):
        return self.__sous_arb
    def set_sous_arb(self,valeur):
        self.__sous_arb.append(valeur)
        
    def get_difficulte(self):
        return self.__difficulte
    def set_difficulte(self,valeur):
        self.__difficulte=valeur


    def __repr__(self):
        return f"{self.get_etat()})"
    
    def ajout_ss_arb(self,other):
        self.set_sous_arb(other)
        
    def est_feuille(self):
        if self.get_sous_arb()==[] :
            return True
        else:         
            return False
        
    def copie(self):
        a_copie = IA(self.get_etat(), self.get_dernier_coup(), self.get_controle())
        for ss_arb in self.get_sous_arb():
            a_copie.ajout_ss_arb(ss_arb.copie())
        return a_copie
   

    
def affichage(liste):
        print(" "+len(liste.get_etat())*' -')
        for l in range(len(liste.get_etat()[0])):
            c="|"
            for p in range(len(liste.get_etat())):
                c+=" "+liste.get_etat()[p][l]
            print(c+" |")
        c=" "
        for p in range(len(liste.get_etat())):
            c+=f" {Alphabet[p]}"
        print(" "+len(liste.get_etat())*' -')
        print(c)   

##Fonction de test pour l'euristie###################################################################
def VerifVictoire(arb:IA,joueur:int) -> int:
    """
    

    Parameters
    ----------
    arb : IA
    joueur : int

    Returns
    -------
    int
        Retourne une grande valeur si le joueur gagne et une valeur négative sinon.

    """
    if joueur==0 : pion,autrepion="O","X"
    elif joueur==1 : pion,autrepion="X","O"
    nombre=3      
    for colonne in range(arb.get_colonne()) : # on teste en ligne si des pions sont alignés en colonne
        chaine="".join(arb.get_etat()[colonne])
        if nombre != 3 and ((nombre != 1 and arb.get_nombrejetons()*autrepion in chaine) or (nombre != 0 and arb.get_nombrejetons()*pion in chaine)): # si joueur 1 a gagné ou que  joueur 2 a gagné
            return 0
        if arb.get_nombrejetons()*pion in chaine:
            nombre=0           
        elif arb.get_nombrejetons()*autrepion in chaine:
            nombre=1
    for ligne in range(arb.get_rangee()) : # on teste en ligne si des pions sont alignés en ligne
        chaine=""
        for colonne in range(arb.get_colonne()):
            chaine=chaine+arb.get_etat()[colonne][ligne] 
        if nombre != 3 and ((nombre != 1 and arb.get_nombrejetons()*autrepion in chaine) or (nombre != 0 and arb.get_nombrejetons()*pion in chaine)): # si joueur 1 a gagné ou que  joueur 2 a gagné
            return 0
        if arb.get_nombrejetons()*pion in chaine:
            nombre=0
        elif arb.get_nombrejetons()*autrepion in chaine:
            nombre=1
    for ligne in range(arb.get_rangee()) : # on teste en diagonale si des pions sont alignés
        chaine1=""
        chaine2=""
        j=0
        for colonne in range(arb.get_colonne()):            
            if ligne+j < arb.get_rangee():
                chaine1=chaine1+arb.get_etat()[colonne][ligne+j] 
                
            if ligne-j < arb.get_rangee() and ligne-j>=0:
                chaine2=chaine2+arb.get_etat()[colonne][ligne-j] 
            j=j+1
        if nombre != 3 and ((nombre != 0 and (arb.get_nombrejetons()*pion in chaine1 or arb.get_nombrejetons()*pion in chaine2)) or (nombre != 1 and (arb.get_nombrejetons()*autrepion in chaine1 or arb.get_nombrejetons()*autrepion in chaine2))):
            return 0
        if arb.get_nombrejetons()*pion in chaine1 or arb.get_nombrejetons()*pion in chaine2:
            nombre=0      
        elif arb.get_nombrejetons()*autrepion in chaine1 or arb.get_nombrejetons()*autrepion in chaine2:
            nombre=1
            
    #on renvoie la bonne valeur en fonction de qui a gagné        
    if joueur==nombre:          
        return 10
    
    if joueur==nombre:          
        return -10
    
    if nombre==3:
        return 0

def VerifAligne(arb:IA,joueur:int) -> int:
    """
    

    Parameters
    ----------
    arb : IA
    joueur : int

    Returns
    -------
    int
        Retourne une grande valeur si le joueur gagne et une valeur négative sinon.

    """
    if joueur==0 : pion,autrepion="O","X"
    elif joueur==1 : pion,autrepion="X","O"
    nombre=3      
    for colonne in range(arb.get_colonne()) : # on teste en ligne si des pions sont alignés en colonne
        chaine="".join(arb.get_etat()[colonne])
        if " "*arb.get_nombrejetons() + pion in chaine: #changer la cond pas finie
            
            
            
            
            
            
            nombre=0           
        elif " "+(arb.get_nombrejetons()-1)*autrepion in chaine:
            nombre=1
            
    for ligne in range(arb.get_rangee()) : # on teste en ligne si des pions sont alignés en ligne
        chaine=""
        for colonne in range(arb.get_colonne()):
            chaine=chaine+arb.get_etat()[colonne][ligne] 
        if " "+(arb.get_nombrejetons()-1)*pion in chaine:
            nombre=0
        elif arb.get_nombrejetons()*autrepion in chaine:
            nombre=1
    for ligne in range(arb.get_rangee()) : # on teste en diagonale si des pions sont alignés
        chaine1=""
        chaine2=""
        j=0
        for colonne in range(arb.get_colonne()):            
            if ligne+j < arb.get_rangee():
                chaine1=chaine1+arb.get_etat()[colonne][ligne+j] 
                
            if ligne-j < arb.get_rangee() and ligne-j>=0:
                chaine2=chaine2+arb.get_etat()[colonne][ligne-j] 
            j=j+1
        if arb.get_nombrejetons()*pion in chaine1 or arb.get_nombrejetons()*pion in chaine2:
            nombre=0      
        elif arb.get_nombrejetons()*autrepion in chaine1 or arb.get_nombrejetons()*autrepion in chaine2:
            nombre=1
            
    #on renvoie la bonne valeur en fonction de qui a gagné        
    if joueur==nombre:          
        return 10
    
    if joueur==nombre:          
        return -10
    
    if nombre==3:
        return 0

def Evaluation(arb,joueur): #on va vers le point qui donne le plus de possibilité d'aligner 4 coup
        #je pense pas qu'il y ait de bonnes ou de mauvaises situations... 
        #Mais quand on gagne c'est bien donc c'est 1 et si on perd c'est -1, dans le cas de l'égalité c'est 0. C'est ce qu'on vérifie ci-dessous:
        listevaleur=[]
        listevaleur.append(VerifVictoire(arb, joueur))
        
            
        
        
        
        #on renvoie la bonne valeur en fonction de qui a gagné        
        return max(listevaleur)
   
def arb_P4(pmax,P4,dernierCoup=["",""],joueur=0):
    A=IA(pmax,P4.grille)   
    
    def fin(arborescence):
        if Evaluation(arborescence,0) !=0 or max([arborescence.get_etat()[i].count(" ") for i in range(len(arborescence.get_etat()[0]))])==0:
            return True
        else:
            return False
        
    if fin(A) or pmax==0:
        return A
    else:
        if dernierCoup[0]=="*" :
             for lettre in Alphabet[0:A.get_colonne()]:
                 couppreced=dernierCoup
                 nouvP4=P4.copie()
                 nouvP4.jouer_colonne(lettre,joueur)
                 couppreced[joueur]=lettre
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
        else:
             ##On teste tout les placements possibles#######################
             for lettre in Alphabet[0:A.get_colonne()]:
                 couppreced=dernierCoup
                 nouvP4=P4.copie()
                 nouvP4.jouer_colonne(lettre,joueur)
                 couppreced[joueur]=lettre
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
             ##On teste les rotations#######################################
             """
             couppreced=dernierCoup
             nouvP4=P4.copie()
             nouvP4.rotation_plus()
             A.__colonne,A.__rangee=A.__rangee,A.__colonne
             A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
             
             
             couppreced=dernierCoup
             nouvP4=P4.copie()
             nouvP4.rotation_moins()
             A.__colonne,A.__rangee=A.__rangee,A.__colonne
             A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
             """
             ##On teste les décalages#######################################
             couppreced=dernierCoup
             nouvP4=P4.copie()
             nouvP4.decalage_gauche()
             A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
            
             couppreced=dernierCoup
             nouvP4=P4.copie()
             nouvP4.decalage_droit()
             A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
             
             ##On teste les bombes#######################################
             for lettre in Alphabet[0:A.get_colonne()]:
                 couppreced=dernierCoup
                 nouvP4=P4.copie()
                 nouvP4.bombe(lettre)
                 couppreced[joueur]=lettre
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
            
                
             
    return A



def minimax(arbre,evaluation,joueur,difficulte):
    if arbre.est_feuille() or difficulte==0:
        arbre.set_valeur(evaluation(arbre,joueur))
        return evaluation(arbre,joueur)
    else:
        if arbre.get_joueur()==joueur:
            valeur=-mt.inf    
            for fils in arbre.get_sous_arb():
                valeur=max(valeur,minimax(fils,evaluation,joueur,difficulte-1))
        else:
            valeur=mt.inf
            for fils in arbre.get_sous_arb():
                valeur=min(valeur,minimax(fils,evaluation,joueur,difficulte-1))
    arbre.set_valeur(valeur)
    
    return valeur

#################################################################################################################

#dictvaleur[Arb.__repr__()][cheminmax]=max(dictvaleur[Arb.__repr__()][cheminmax],Arb.get_valeur())
def Arbtodict(Arb,dictvaleur):
    if Arb.est_feuille():        
        return None
    else:    
        for suivants in Arb.get_sous_arb():            
            if suivants.__repr__() in dictvaleur.keys():
                if 'precedent' in dictvaleur[suivants.__repr__()].keys(): dictvaleur[Arb.__repr__()]['precedent'].union({Arb.__repr__()})
                else : dictvaleur[suivants.__repr__()]['precedent']={Arb.__repr__()}
                Arbtodict(suivants,dictvaleur)
            else:
                dictvaleur[suivants.__repr__()]=dict(duree=suivants.get_valeur())
                dictvaleur[suivants.__repr__()]['precedent']={Arb.__repr__()}
                Arbtodict(suivants,dictvaleur)



###################################################################################################################
def couleur_arc(dico_precedents:dict)->dict:
    graphe=deepcopy(dico_precedents)
    for sommet1 in graphe.keys():
        prec_color={}
        for sommet2 in graphe[sommet1]['precedent']:
            prec_color[sommet2]='black'
        graphe[sommet1]['precedent']=prec_color
    return graphe

def niveau(G:dict)->list:
    """

    Parameters
    ----------
    G : dict
        Graphe.

    Returns
    -------
    list
        Renvoie une liste des sommets du graphe rangés par niveau dans l'ordre croissant.

    """
    dic=deepcopy(G)
    #Transformation du dictionnaire des suivants en un ensemble
    for sommet in dic.keys():
        dic[sommet]['precedent']=set(dic[sommet]['precedent'].keys())
    #==========================================================
    liste=[set(),] # L'ensemble Ci sera liste[i]
    T=set() # Ensemble des sommets traites, initialise a "vide"
    S=set(dic.keys()) # Ensemble de tous les sommets
    k = 0 # k represente le niveau "traite" dans l'algorithme
    #===== Initialisation =====
    for sommet in S:
        if not dic[sommet]['precedent']: # Les sommets sans precedents ...
            T.add(sommet) # sont traites et ...
            liste[k].add(sommet) # sont de niveau 0
    #===== Boucle while =====
    while T != S :
        for sommet in S-T: # Pour les sommets non traites
            # On raye les sommets de niveau k dans la liste des precedents :
            dic[sommet]['precedent']=dic[sommet]['precedent']-liste[k]
        k = k + 1
        # On cree un ensemble pour le sommets de niveau "k+1", initialise a vide :
        liste.append(set())
        for sommet in S-T: # Pour tous les sommets non traites
            if not dic[sommet]['precedent']: # Si le sommet n'a plus de precedent
                T.add(sommet) # il est traite et ...
                liste[k].add(sommet) # est de niveau "k+1"
    return liste

def dic2dot(dic:dict,fileName=None)->dict:
    txt_f = 'digraph G2 {\nrankdir=LR;\nnode [shape = Mrecord, style=filled];'
    for sommet,dico in dic.items():        
        plustot=dico['tot']
        plustard=dico['tard']
        bordure=dico['couleur']
        txt_f += f'\n{sommet} :t [label="'+'{'+f' {plustot} | {plustard}'
        txt_f += ' }'+f'|<t> {sommet}",fillcolor={"white"},color={bordure}];'
    for sommet,dico in dic.items():
        for suivant in dico['suivant'].keys():
            cout=dico['duree']
            trait=dico['suivant'][suivant]
            txt_f += f'\n{sommet}->{suivant} [label={cout},color={trait}];'
    txt_f += '\n }'
    if fileName != None:
        with open(fileName,'w') as fd:
            fd.write(txt_f)
    return txt_f
##################################################################################################################################################################
def prec2complet(dico:dict)->dict:
    """

    Parameters
    ----------
    dico : dict
        Graphe.

    Returns
    -------
    dict
        Retourne le graphe donné en y ajoutant à ses sommet la clé 'suivant' et en lui affectant le graphe correspondant.

    """
    for dico_s in dico.values():
        dico_s['suivant']={}
    for sommet, dico_s in dico.items():
        for sommet_pre in dico_s['precedent'].keys():
            dico[sommet_pre]['suivant'][sommet]='black'
    return dico
##################################################################################################################################################################
def graph_fin(G:dict)->dict:
    """

    Parameters
    ----------
    G : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le graphe donné en y ajoutant un sommet 'fin' puis en y ajoutant à ses sommets la clé 'couleur' avec la valeur 'black'.

    """
    D=dict()
    for sommet, dico_s in G.items():
        dico_s['couleur']='black'
        for sommet_pre in dico_s['precedent'].keys():
            if dico_s['suivant']=={}:
                D[sommet]='black'
        
    G['fin']={'duree':0,'precedent':D,'suivant':{},'couleur':'black'}
    return prec2complet(G) # on réactualise les clés "suivant" pour le sommet fin
##################################################################################################################################################################
def affecte_niveau(G:dict)->dict:
    """

    Parameters
    ----------
    G : dict
        Graphe.

    Returns
    -------
    dict
        Renvoie le graphe donné en y ajoutant une clé "niveau" à tout ses sommets avec la bonne valeur associée.

    """
    L=niveau(G)
    for Niveau in range(0,len(L)):
        for sommet, dico_s in G.items():
            if sommet in L[Niveau]:
                dico_s['niveau']=Niveau
    return G
##################################################################################################################################################################
def graphe2mpm(G:dict)->dict:
    """

    Parameters
    ----------
    G : dict
        Graphe.

    Returns
    -------
    dict
        Ajoute les clés "tot" et "tard" à tout les sommets avec la valeur "_".

    """
    for sommet,dico_s in G.items():
      dico_s['tot']='_'
      dico_s['tard']='_'
    return G
##################################################################################################################################################################
def ford(sommet0:str,G:dict,f:str)->int:
    """
    
    Parameters
    ----------
    G : dict
        Graphe.
    f : str
        sommet.
    
    Returns
    -------
    int
        Retourne la valeur du chemin le plus élévé juqu'au sommet f en partant de n'importe quel sommet initial.
    
    """
    lniveau=niveau(G)  #on récupère la liste des sommets qui permettent d'atteindre le point f
    maximum=[]
    P={list(G.keys())[i] for i in range(len(G))} #ensemble des sommets
    trace={sommet0:[0,None]} #initialisation coût s0
    for s in P-{sommet0}: #initialisation coûts associés aux sommets différents de s0
        trace[s]=[mt.inf,None]
    k=1
    while trace[f][0]==mt.inf:
      for y in lniveau[k]: #ensemble des sommets de niveau k          
        value=[trace[x][0]+G[x]['duree'] for x in G[y]['precedent']]
        if value!=[]: 
          trace[y][0]=max(value)

        for z in G[y]['precedent']:       
          if trace[z][0]+G[z]['duree']==trace[y][0]:
            trace[y][1]=z      
      k+=1
    maximum.append(trace[f][0])    
             
    if maximum!=[]:
      maxi=max(maximum)  #on compare la durée des chemins menant à f suivant les sommets de départs choisis  
    else:
      maxi=0
    return maxi

grille = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
G=Puissance4(grille)        
Arb=arb_P4(2,G)
minimax(Arb,Evaluation,0,2)  
dictvaleur={Arb.__repr__():{'duree':0,'precedent':set()}}
Arbtodict(Arb,dictvaleur)

Gra=graphe2mpm(affecte_niveau(graph_fin(prec2complet(couleur_arc(dictvaleur)))))



def main():
    """
    Met en place le jeu du puissance4 et permet au joueur de jouer contre une IA

    Returns
    -------
    None

    """
    grille = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
    G=Puissance4(grille)
    difficulte=int(input("Difficulté de l'IA : "))
    while G.victoire()[1]==3:
        coupjoueur=input("Le coup joué est : ")
                
        #condition et Debug:
        if coupjoueur=="break" or G.victoire()[0]==True:
            break
        
        #Le joueur joue :
        if G.jouer_coup(coupjoueur,0)==False: # si le coup n'aboutit pas on ne fais rien
            print("TU PEUX PAS")
            G.affichage()
            
        else: # si le coup aboutit on laisse l'IA jouer
            #l'IA joue:  
            
            Arb=arb_P4(difficulte,G)
            minimax(Arb,Evaluation,0,2)   
            
            #faut trouver le chemin le plus long
            for i in Arb.get_sous_arb():
                affichage(i)

            coupIA=Alphabet[i]
            print(f"\n COUP DE L'IA : {coupIA}")
            G.jouer_coup(coupIA,1)
            G.affichage()
        
    print(f'Le joueur n°{G.victoire()[1]} a Gagné')
    

    
    
    
    
"""    
#Affichage#############################################################################################
colonne=7
rangee=6
root = Tk()
#Intro####################
param = Canvas(root, width=200, height=200, background='white')
#on choisit la difficulte avec une molette

difficulte = Listbox(root)
difficulte.insert(1, "1")
difficulte.insert(2, "2")
difficulte.insert(3, "4")
difficulte.insert(4, "6")

difficulte.pack()

#rangee
txtrang = Label(root, text="Entrez le nombre de rangée")
txtrang.pack()

rangeechoix = Entry(root, width=30)
rangeechoix.pack()
#colonne
txtcol = Label(root, text="Entrez le nombre de colonne")
txtcol.pack()

colonnechoix = Entry(root, width=30)
colonnechoix.pack()
#Jeu######################

canvas = Canvas(root, width=800, height=800, background='white')
for i in range(0,colonne+1): #colonne
    ligne1 = canvas.create_line(30+i*740/colonne, 150, 30+i*740/colonne, 795)
    txt = canvas.create_text(85+i*740/colonne,120, text=Alphabet[i], font="Arial 16 italic", fill="red")
for i in range(1,rangee+1):#rangee
    ligne2 = canvas.create_line(30, 150+i*645/(rangee), 770, 150+i*645/(rangee))
canvas.pack()


root.mainloop()


"""









