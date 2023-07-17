##Imporattions Puissance4
import math as mt
import copy
from random import randint

Alphabet="ABCDEFGHIJKLMNOPQRSTUVWXYZ"

##Puissance 4

class Puissance4:
    def __init__(self,grille,derniers_coups=["",""],bombes=[1,1],pion=["O","X"],colonne=7,rangee=6,nombre_jetons_victoire=4):
        """
        Initialise les parametres du jeu Puissance 4 
        
        Parameters
        ----------
        grille : list of list
            Liste de listes representants les colonnes du puissance 4.
        
        derniers_coups : list of str
            Par defaut : ["",""]. 
            Premiere position : dernier coup du joueur 0 
            Deuxieme position : dernier coup du joueur 1
                        
        bombes : list of int
            Par defaut : [1,1].
            Premiere position : dernier coup du joueur 0 
            Deuxieme position : dernier coup du joueur 1
        
        pion : list of str
            Par defaut ["O","X"].
            Premiere position : Pion du joueur 0 
            Deuxieme position : Pion coup du joueur 1
            
        colonne : int
            Par defaut 7.
            Nombre de colonnes du jeu
            Entre 4 et 26
            
        rangee : int
            Par defaut 6.
            Nombre de rangees du jeu 
            Entre 4 et 26
            
        nombre_jetons_victoire : int
            Par defaut 4.
            Nombres de jetons a aligner pour gagner une partie

        Returns
        -------
        None.

        """
        assert 3<colonne<27
        assert 3<rangee<27
        self.grille=grille
        self.derniers_coups=derniers_coups
        self.bombes=bombes
        self.colonne=colonne
        self.rangee=rangee
        self.nombre_jetons_victoire=nombre_jetons_victoire

    def copie(self):
        """
        Copie le jeu 

        Returns 
        -------
        Puissance 4
        """
        return copy.deepcopy(self)

    def affichage(self):
        """
        Permet d'afficher un etat du jeu Puissance 4 (une grille) dans la console

        Returns
        -------
        None.

        """
        print(" "+self.colonne*' -') #ligne du haut 
        for l in range(self.rangee):
            c="|"
            for p in range(self.colonne):
                c+=" "+self.grille[p][l] #affiche le bon pion
            print(c+" |")
        c=" "
        for p in range(self.colonne):
            c+=f" {Alphabet[p]}" #affiche les lettres correspondants au colonnes
        print(" "+self.colonne*' -') #ligne du bas 
        print(c)

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
                
        for colonne in range(self.colonne) : # on teste en ligne si des pions sont alignes en colonne
            chaine="".join(self.grille[colonne])
            if nombre != 3 and ((nombre != 1 and self.nombre_jetons_victoire*"X" in chaine) or (nombre != 0 and self.nombre_jetons_victoire*"O" in chaine)): # si joueur 1 a gagne ou que  joueur 2 a gagne
                return (plein,2)  
            if self.nombre_jetons_victoire*"O" in chaine:
                nombre=0           
            elif self.nombre_jetons_victoire*"X" in chaine:
                nombre=1  
                                   
        for ligne in range(self.rangee) : # on teste en ligne si des pions sont alignes en ligne
            chaine=""
            for colonne in range(self.colonne):
                chaine=chaine+self.grille[colonne][ligne] 
            if nombre != 3 and ((nombre != 1 and self.nombre_jetons_victoire*"X" in chaine) or (nombre != 0 and self.nombre_jetons_victoire*"O" in chaine)): # si joueur 1 a gagne ou que  joueur 2 a gagne
                return (plein,2)  
            if self.nombre_jetons_victoire*"O" in chaine:
                nombre=0
            elif self.nombre_jetons_victoire*"X" in chaine:
                nombre=1  
                           
        L=self.diagonale() # on teste en diagonale si des pions sont alignes
        for i in range(len(L)):
            chaine="".join(L[i])
            if self.nombre_jetons_victoire*"O" in chaine and self.nombre_jetons_victoire*"X" in chaine :
                return( plein,2)
            else :
                if self.nombre_jetons_victoire*"O" in chaine :
                    nombre=0
                elif self.nombre_jetons_victoire*"X" in chaine :
                    nombre =1
        
        return (plein,nombre)
    
    def diagonale(self):
        """
        Retourne toutes les diagonales de la grille donnée en parametres 

        Returns
        -------
        diag : TYPE
            DESCRIPTION.

        """
        diagdroite = [[] for _ in range(self.colonne + self.rangee - 1)]
        diaggauche = [[] for _ in range(len(diagdroite))]
        min_diaggauche = -self.colonne + 1
        
        for x in range(self.rangee):
            for y in range(self.colonne):
                diagdroite[x+y].append(self.grille[y][x])
                diaggauche[x-y-min_diaggauche].append(self.grille[y][x])
        
        diag=diagdroite+diaggauche
        return diag

    def jouer_colonne(self,colonne:str,joueur:int)->None:
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
        Cree un str pour permettre d'enlever les cases vides puis concatene ce dernier afin de retrouver un str de la longeur du nombre de lignes
        Puis recree une liste de liste qui correspond a la bonne grille 
        Action de "gravite" sur les pions 
        
        Returns
        -------
        None
        """
        L=self.grille
        for i in range(self.colonne):
            chaine=''.join(L[i])
            chaine=chaine.replace(' ','')
            L[i]=[' ' for i in range(self.rangee-len(chaine))]+list(chaine)
        self.grille=L
    
    ##Decalage
    
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
    
    ##Rotation
    def rotation_plus(self):
        """
        tourne la grille dans le sens direct (trigo) de 90 degres
        puis on utilise la fonction gravite pour faire "descendre" tout les pions qui n'aurait
        plus de pions en dessous d'eux 
        """
        L=self.m_transpose()
        for i in range(len(L)):
            L[i].reverse()
        self.grille=L
        self.colonne,self.rangee=self.rangee,self.colonne
        self.gravite()     
        

    def rotation_moins(self):
        """
        tourne la grille dans le sens indirect (horaire) de 90 degres
        puis on utilise la fonction gravite pour faire "descendre" tout les pions qui n'aurait
        plus de pions en dessous d'eux 
        """
        L=self.m_transpose()
        for i in range(len(L)//2):
            L[i],L[len(L)-1-i]=L[len(L)-1-i],L[i]
        self.grille=L
        self.colonne,self.rangee=self.rangee,self.colonne
        self.gravite()
    
    ##Fonctions  pour la rotation 
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
    
    ##Bombe

    def bombe(self,colonne:str)->None:
        """
        Place une bombe dans une colonne et explose tous les pions autour de cette derniere.
        
        Parameters
        ----------
        colonne : str
            Colonne dans laquelle on veut placer la bombe.

        Returns
        -------
        None
            Modifie la grille sur place.

        """
        a=Alphabet.index(colonne) #on recupere le numero de la colonne jouee
        self.grille[a][0]="%" #on place le pion  bombe
        self.gravite()
        k = 0
        for i in range(self.rangee):
            if self.grille[Alphabet.index(colonne)][i]=="%":
                k=i #on recupere le numero de la rangee ou est la bombe
        
        #cas particuliers de placements pour eviter des out of range
        
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
        #dernier cas, cas general, si la bombe n'est pas sur un bord 
        else:
            for p in range(a-1,a+2):
                for q in range(k-1,k+2):
                    self.grille[p][q]=" "
        
        self.gravite() #on fait tomber tous les pions de la grille 
    
    ##Jouer 
    
    def jouer_coup(self,coup_joue:str,joueur:int):
        """
        Modifie la grille sur place en jouant le coup demandé
        Si le coup n'est pas jouable, il n'est pas joué

        Parameters
        ----------
        coup_joue : str
        joueur : int
        
        Returns
        -------
        bool
            True si le coup a ete effectue 
            False si le coup n'a pas ete effectue (coup non jouable a l'instant t du jeu)
        """
        
        coup_joue.upper() #on met le str d'entre en majuscule pour eviter un probleme eventuel 
        
        if coup_joue[0] in Alphabet[0:self.colonne] and self.grille[Alphabet.index(coup_joue[0])][0]==" ": #si le coup est juste de placer un pion, il y a juste une condition sur la colonne
            self.jouer_colonne(coup_joue[0],joueur)
            self.derniers_coups[joueur]=coup_joue #on modifie le dernier coup du joueur concerne
            return True

        else: #sinon, il faut que le dernier coup joue par le joeur ne soit pas un coup special 
            if self.derniers_coups[joueur]!="":
                try:
                    assert self.derniers_coups[joueur][0] in Alphabet
                except AssertionError : 
                    return False
            
        if "*" == coup_joue[0]: #si le coup est une bombe 
            
            if coup_joue[1] in Alphabet[0:self.colonne] and self.bombes[joueur]!=0: #condition sur la colonne et le nombre de bombes restantes pour le joueur 
                self.bombe(coup_joue[1]) #on place la bombe
                self.bombes[joueur]-=1 #on retire un bombe au joueur concerne
                self.derniers_coups[joueur]=coup_joue[:2]
                return True
        
        elif ">" == coup_joue: #si le coup est un decalage vers la droite
            if self.derniers_coups[1-joueur]=="<" or self.derniers_coups[1-joueur]==">":
                return False 
            else:
                self.decalage_droit()
                self.derniers_coups[joueur]=coup_joue[0]
                return True
        
        elif "<" == coup_joue: #si le coup est un decalage vers la droite
            if self.derniers_coups[1-joueur]=="<" or self.derniers_coups[1-joueur]==">":
                return False
            else: 
                self.decalage_gauche()
                self.derniers_coups[joueur]=coup_joue[0]
                return True
        
        elif "+" == coup_joue: #si le coup est une rotation dans le sens trigo
            if self.derniers_coups[1-joueur]=="+" or self.derniers_coups[1-joueur]=="-":
                return False
            else:
                self.rotation_plus()
                self.derniers_coups[joueur]=coup_joue[0]
                return True
        
        elif "-" == coup_joue: #si le coup est une rotation dans le sens horaire
            if self.derniers_coups[1-joueur]=="+" or self.derniers_coups[1-joueur]=="-":
                return False
            else: 
                self.rotation_moins()
                self.derniers_coups[joueur]=coup_joue[0]
                return True
        
        return False #si rien n'est fait avant on retourne False 

##Tests des fonctions du Puissance 4 

def testP4():
    grille = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
    G=Puissance4(grille)
    print('Placement de pions de bases')
    G.jouer_coup('A',0)
    G.affichage()
    G.jouer_coup('B',1)
    G.affichage()
    G.jouer_coup('C',0)
    G.affichage()
    G.jouer_coup('D',1)
    G.affichage()
    print(f"Decalage droit : {G.jouer_coup('>', 0)}")
    G.affichage()
    print(f"On place un pion pour eviter deux coups speciaux d'affilee : {G.jouer_coup('E',1)}")
    G.affichage()
    print(f"Decalage gauche : {G.jouer_coup('<', 0)}")
    G.affichage()
    print(f"On place un pion pour eviter deux coups speciaux d'affilee : {G.jouer_coup('F',1)}")
    G.affichage()
    print(f"Rotation sens trigo : {G.jouer_coup('+', 0)}")
    G.affichage()
    print(f"On place un pion sur une colonne qui n'existe plus : {G.jouer_coup('G',1)}")
    G.affichage()
    print(f"Le coup d'avant n'a pas aboutit, on place le pion sur une autre colonne : {G.jouer_coup('A',1)}")
    G.affichage()
    print(f"Rotation sens horaire : {G.jouer_coup('-', 0)}")
    G.affichage()
    print(f"Test d'une bombe apres une rotation : {G.jouer_coup('*D', 1)}")
    print(f"On place un pion car le coup d'avant n'a pas aboutit: {G.jouer_coup('E',1)}")
    G.affichage()
    print(f"Bombe en D : {G.jouer_coup('*D', 0)}")
    G.affichage()
