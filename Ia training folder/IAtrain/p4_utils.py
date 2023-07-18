##Puissance 4 utils
from IAtrain.p4_ia import *
from p4 import *

##Classe IA

def affichage(arb)->None:
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
    print(" "+len(arb.get_etat())*' -')
    for l in range(len(arb.get_etat()[0])):
        c="|"
        for p in range(len(arb.get_etat())):
            c+=" "+arb.get_etat()[p][l]
        print(c+" |")
    c=" "
    for p in range(len(arb.get_etat())):
        c+=f" {Alphabet[p]}"
    print(" "+len(arb.get_etat())*' -')
    print(c)   

def quelcoup(arbre)->str:
    """

    Parameters
    ----------
    arbre : IA
        Sommet d'une arborescence.

    Returns
    -------
    str
        Retourne quel coup à été fait pour arriver à ce sommet.

    """
    if arbre.__repr__()[-2]=='*':
        return arbre.__repr__()[-2]+arbre.__repr__()[-1]
    else:
        return arbre.__repr__()[-1]
    
##Fonction de test pour l'euristie###################################################################
def diagonale(L:list)->list:
    """

    Parameters
    ----------
    L : list
        Liste de liste des colonnes d'une grille.

    Returns
    -------
    list
        Retourne les listes correspondantes à toutes les diagonales de la grille.

    """
    
    diagdroite = [[] for i in range(len(L) + len(L[0]) - 1)]
    diaggauche = [[] for i in range(len(diagdroite))]
    min_diaggauche = -len(L) + 1
    for x in range(len(L[0])):
        for y in range(len(L)):
            diagdroite[x+y].append(L[y][x])
            diaggauche[x-y-min_diaggauche].append(L[y][x])
    
    diag=diagdroite+diaggauche
    return diag

def VerifVictoire(arb,joueur:int) -> int:
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
    pion,autrepion="O","X"
    nombre=3      
    for colonne in range(arb.get_colonne()) : # on teste en colonne si des pions sont alignés en colonne
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
    
    
    L=diagonale(arb.get_etat()) # on teste en diagonale si des pions sont alignés
    for i in range(len(L)):
        chaine="".join(L[i])
        
        if arb.get_nombrejetons()*pion in chaine and arb.get_nombrejetons()*autrepion in chaine :
            return 0
        else :
            if arb.get_nombrejetons()*pion in chaine :
                nombre=0
            elif arb.get_nombrejetons()*autrepion in chaine :
                nombre =1
                
                
            
    #on renvoie la bonne valeur en fonction de qui a gagné        
    if joueur==nombre:          
        return 100
    
    if joueur!=nombre and nombre!=3:          
        return -100
    
    if nombre==3:
        return "rien"

def Verifligne(arbre,coupjoue:'str', joueur:int) -> int:
    """
    
    Parameters
    ----------
    arb : IA
    joueur : int

    Returns
    -------
    int
        Retourne une valeur en fonction des possibilités d'alignement en ligne d'un coup si c'est au joueur de jouer 
        sinon renvoie cette même valeur mais en négatif

    """
    

    if arbre.get_joueur()==0 : pion,autrepion="X","O"
    elif arbre.get_joueur()==1 : pion,autrepion="O","X"
    arb=arbre.copie()
    nombre=0    
    grilletest=deepcopy(arb.get_etat())
    P4test=Puissance4(grilletest,arb.get_colonne(),arb.get_rangee())
    colonnelettre=Alphabet[0:arb.get_colonne()].index(coupjoue)#on recup les positions du coup posé
    lignelettre=P4test.grille[colonnelettre].index(pion)
    # On créer une liste des indices suceptibles d'arriver dans les alignements de win
    pasgauche=min(arb.get_nombre_jetons_victoire()-1,colonnelettre) #la place disponible a gauche
    pasdroite=min(arb.get_nombre_jetons_victoire(),arb.get_colonne()-colonnelettre)#la place disponible a droite
    colonnealign=[i for i in range(colonnelettre-pasgauche,colonnelettre+pasdroite+1)] # liste des indices de colonnes dispo
    #s'il y a une ligne de libre avec la lettre dedans on l'ajoute
    for indicolonne in colonnealign:#pour tout les indices des colonnes des placements qui permettraient un alignement 
        if indicolonne<=colonnelettre:
            if indicolonne+arb.get_nombre_jetons_victoire()<=arb.get_colonne() : bornedroite=indicolonne+arb.get_nombre_jetons_victoire() # le cas particulier où l'on depasserait sur la droite
            else: bornedroite=arb.get_colonne()-indicolonne
            listecaract=[P4test.grille[i][lignelettre] for i in range(indicolonne,bornedroite)]#on créé une liste qui prend les caractères voisins
            if len(listecaract)>=arb.get_nombre_jetons_victoire(): # si la liste est plus petite que le nombre de jetons necessaires à la victoire c'est inutile de continuer
                carac=''.join(listecaract) 
                k=0 # on initialise un compteur, ce dernier grandi si les coups d'alignements possibles sont faisable directement ce qui augmentera la valeur
                for p in range(0,len(carac)):
                    if carac[p] == pion : nombre+=0.25 #s'il y a déja des pions placés c'est mieux
                    if lignelettre<arb.get_rangee()-1:    
                        if P4test.grille[indicolonne+p][lignelettre+1]!=" ":
                            # si jamais il n'y a rien en dessous, ce n'est pas possible tout de suite donc moins de valeur
                             k+=0.1
                    else:
                        k+=0.1
                    
                if not autrepion in carac:
                    nombre=nombre+0.35+k
    #on renvoie la valeur d'alignement possible   
    if arbre.get_joueur()!=joueur:
        return nombre
    else:
        return -nombre

def compte_pion(arbre,joueur:int)->int:
    """

    Parameters
    ----------
    arbre : IA
        Sommet d'une arborescence.
    joueur : int
        joueur.

    Returns
    -------
    int
        Retourne le nombre de pion sur la grille si c'est au joueur de jouer sinon renvoie le nombre de pion en négatif.

    """
    if joueur==0 : pion="O"
    elif joueur==1 : pion="X"
    
    nombre=0
    for colonne in arbre.get_etat():
        nombre+=colonne.count(pion)
        
    if arbre.get_joueur()==joueur:
        return nombre
    else:
        return -nombre

def Verifdiag(arbre,coupjoue:str,joueur:int)->int:
    """

    Parameters
    ----------
    arbre : IA
        Sommet d'une arborescence.
    coupjoue : str
        Coup joué.
    joueur : int
        joueur.

    Returns
    -------
    int
        Retourne une valeur en fonction des possibilités d'alignement en diagonale d'un coup si c'est au joueur de jouer 
        sinon renvoie cette même valeur mais en négatif.

    """
    arb=arbre.copie()   
    grilletest=deepcopy(arb.get_etat())
    P4test=Puissance4(grilletest,arb.get_colonne(),arb.get_rangee())
    
    Listediag=diagonale(arbre.get_etat())

    if arbre.get_joueur()==0 : pion,autrepion="X","O"
    elif arbre.get_joueur()==1 : pion,autrepion="O","X"
    
    nombre=0
    colonnelettre=Alphabet[0:arbre.get_colonne()].index(coupjoue)#on recup les positions du coup joué

    lignelettre=P4test.grille[colonnelettre].index(pion)
    
    
    
    ##################DIAGONALE DESCENDANTE##############################
    indicediag=colonnelettre+lignelettre #on repère dans quelle diagonale est notre coup 
    indicerangee=lignelettre
    diagonalecoup=Listediag[indicediag]
    if len(diagonalecoup)>= arb.get_nombre_jetons_victoire():
        for i in range(0,arb.get_nombre_jetons_victoire()+1):#on analyse chaque enchainement d'alignement possible sur la même diagonale
            carac=''.join(diagonalecoup[indicerangee-arb.get_nombre_jetons_victoire()+i:indicerangee+i])

            if len(carac)>=4:
                if not autrepion in carac and pion in carac: 
                    nombre=nombre+0.35
                    for p in carac: 
                        if p == pion : nombre+=0.25 #s'il y a déja des pions placés c'est mieux
                        
    ##################DIAGONALE ASCENDANTE##############################
    indicediag=-colonnelettre+lignelettre-arb.get_colonne()+1 #on repère dans quelle diagonale est notre coup 
    indicerangee=lignelettre
    diagonalecoup=Listediag[indicediag]
    if len(diagonalecoup)>= arb.get_nombre_jetons_victoire():
        for i in range(0,arb.get_nombre_jetons_victoire()+1):#on analyse chaque enchainement d'alignement possible sur la même diagonale
            carac=''.join(diagonalecoup[indicerangee-arb.get_nombre_jetons_victoire()+i:indicerangee+i])

            if len(carac)>=4:
                if not autrepion in carac and pion in carac: 
                    nombre=nombre+0.35
                    for p in carac: 
                        if p == pion : nombre+=0.25 #s'il y a déja des pions placés c'est mieux                
                    
    if arbre.get_joueur()!=joueur:
        return nombre
    else:
        return -nombre
            
def maxi(L:list)->int:
    """

    Parameters
    ----------
    L : list
        Liste d'elements.

    Returns
    -------
    int
        Renvoie la valeur maximale en valeur absolue d'une liste.
        Ex : maxi([-10,15,-30]) renvera -30

    """
    Labs=[]
    for i in range(len(L)):
        Labs.append(abs(L[i]))
    return L[Labs.index(max(Labs))]
 

def Evaluation(arb,joueur:int)->int: 
    """
    

    Parameters
    ----------
    arb : IA
        Sommet d'une arborescence.
    joueur : int
        joueur.

    Returns
    -------
    int
        Evalue un sommet et lui donne une valeur en fonction de la capacité du coup à faire gagner le joueur où l'empecher de perdre.

    """
    #je ne pense pas qu'il y ait de bonnes ou de mauvaises situations... 
    
    listevaleur=[]
    testvict=VerifVictoire(arb, joueur)
    if testvict!="rien":
        listevaleur.append(testvict)
    coupjoue=quelcoup(arb)
    
    if coupjoue in Alphabet[0:arb.get_colonne()]:
       listevaleur.append(Verifdiag(arb,coupjoue ,joueur)+Verifligne(arb,coupjoue ,joueur)) #on va vers le point qui donne le plus de possibilité d'aligner n coup
    

    if listevaleur==[] : return compte_pion(arb, joueur) #on renvoie la valeur la plus importante pour chaque situation
    else: return maxi(listevaleur)+compte_pion(arb, joueur)


    
    
def arb_P4(pmax:int,P4:Puissance4,dernierCoup=["",""],joueur=1):
    """

    Parameters
    ----------
    pmax : int
        Valeur de la profondeur de l'arborescence.
    P4 : Puissance4
        Puissance 4.
    dernierCoup : list, optional
        Derniers coup joué par les deux joueur, la première valeur est le dernier coup du joueur 0
        la deuxième est pour le joueur 1. The default is ["rien","rien"].
    joueur : int, optional
        Joueur. The default is 1.

    Returns
    -------
    IA
        Retourne une arborescence des coups possibles à une profondeur pmax en partant d'un etat de base du P4 donné.

    """
    A=IA(pmax,P4.grille,joueur)
    A.set__colonne(P4.colonne)
    A.set__rangee(P4.rangee)
    A.set_derniercoup(dernierCoup[1-joueur])
    couppreced=dernierCoup[:]
    def fin(arborescence):
        if VerifVictoire(A, joueur)==100 or VerifVictoire(A, joueur)==-100 or max([arborescence.get_etat()[i].count(" ") for i in range(arborescence.get_colonne())])==0:
            return True
        else:
            return False
        
    if fin(A) or pmax==0:
        return A
    else:
        #on évite les erreurs de STR
        if dernierCoup[joueur]=="": dernierCoup[joueur]='rien'
        if dernierCoup[1-joueur]=="": dernierCoup[1-joueur]='rien'
        
        #pas de coup spéciaux consécutifs pour un joueur
        if dernierCoup[joueur][0]=="*" or dernierCoup[joueur]=="+" or dernierCoup[joueur]=="-" or dernierCoup[joueur]==">" or dernierCoup[joueur]=="<":
                for lettre in Alphabet[0:A.get_colonne()]:
                     if " " in A.get_etat()[Alphabet[0:A.get_colonne()].index(lettre)]:
                         couppreced[joueur]=lettre
                         nouvP4=P4.copie()
                         nouvP4.jouer_colonne(lettre,joueur)
                         A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
        else:
             ##On teste tout les placements possibles#######################
             for lettre in Alphabet[0:A.get_colonne()]:
                 if " " in A.get_etat()[Alphabet[0:A.get_colonne()].index(lettre)]:
                     couppreced[joueur]=lettre
                     nouvP4=P4.copie()
                     nouvP4.jouer_colonne(lettre,joueur)
                     A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
                     
             ##On teste les rotations#######################################
             #pas rotations si le joueur viens d'en faire une
             
             if dernierCoup[1-joueur]!="+" and dernierCoup[1-joueur]!="-" :
                 
                 #Rotation vers la gauche######
                 couppreced[joueur]="+"
                 nouvP4=P4.copie()
                 nouvP4.rotation_plus()
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
                 
                 #Rotation vers la droite######
                 couppreced[joueur]="-"
                 nouvP4=P4.copie()
                 nouvP4.rotation_moins()
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
                 
             ##On teste les décalages#######################################
             #pas décalage si le joueur viens d'en faire un
             if dernierCoup[1-joueur]!=">" and dernierCoup[1-joueur]!="<":
                 couppreced[joueur]="<"
                 nouvP4=P4.copie()
                 nouvP4.decalage_gauche()
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
                
                 couppreced[joueur]=">"
                 nouvP4=P4.copie()
                 nouvP4.decalage_droit()
                 A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))
             
             
             ##On teste les bombes#######################################
             if P4.bombes[joueur]!=0:
                 for lettre in Alphabet[0:A.get_colonne()]:
                     couppreced[joueur]="*"+lettre 
                     nouvP4=P4.copie()
                     nouvP4.bombe(lettre)
                     nouvP4.bombes[joueur]-=1
                     A.ajout_ss_arb(arb_P4(pmax-1,nouvP4,couppreced,1-joueur))  
                     
             
    return A

def minimax(arbre,evaluation,joueur,difficulte,a=-mt.inf,b=mt.inf):
    """
    

    Parameters
    ----------
    arbre : IA
        Sommet initial d'une arborescence.
    evaluation : fonction
        Euristie.
    joueur : int
        joueur.
    difficulte : int
        profondeur de l'arbre.
    a : TYPE, optional
        valeur minimale. The default is -mt.inf.
    b : TYPE, optional
        valeur maximale. The default is mt.inf.

    Returns
    -------
    TYPE
        DESCRIPTION.

    """
    if arbre.est_feuille() or difficulte==0:
        testeval=evaluation(arbre,joueur)
        if testeval>0:
            arbre.set_valeur(testeval+ difficulte)# on reduit la valeur si on doit faire plus de coup pour arriver à la victoire
        else:
            arbre.set_valeur(testeval)
        return evaluation(arbre,joueur)
    else:
        alpha,beta=a,b
        if arbre.get_joueur()==joueur: 
            for fils in arbre.get_sous_arb():
                alpha=max(alpha,minimax(fils,evaluation,joueur,difficulte-1,alpha,beta))
                if alpha>=beta : 
                    return beta
            arbre.set_valeur(alpha) 
            return alpha
        else:
            for fils in arbre.get_sous_arb(): 
                beta=min(beta,minimax(fils,evaluation,joueur,difficulte-1,alpha,beta))
                if alpha>=beta : 
                    return alpha
            arbre.set_valeur(beta) 
            return beta
        
def trajet(arbre):
    """

    Parameters
    ----------
    arbre : IA
        Arborescence dans laquelle on a appliqué Minimax

    Returns
    -------
    IA
         Renvoie le sommet qui à le plus de valeur.

    """
    i="rien"
    for j in range(len(arbre.get_sous_arb())):
        if arbre.get_sous_arb()[j].get_valeur()!=0:#si on n'a pas étudié avec l'elagage le coup la valeur de base est 0 donc on l'ignore
            i=j
    if i=="rien":
        i=randint(0,arbre.get_colonne()-1) #on ne gaspille pas de coup spéciaux quand on fais des coup aléatoires
        
    maxi=arbre.get_sous_arb()[i].get_valeur()
    trajet=arbre.get_sous_arb()[i]
    for sousarb in arbre.get_sous_arb():
        if maxi<sousarb.get_valeur() and (sousarb.get_valeur()!=0 or VerifVictoire(sousarb,sousarb.get_joueur())==0):
            maxi = sousarb.get_valeur()
            trajet=sousarb
    return trajet

def testia():
    grilletest=[[" "," "," "," ","X","O"],[" "," "," ","X","X","O"],[" "," ","X","O","X","O"],[" "," "," "," ","O","X"],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
    print("On réalise les tests avec une IA de niveau 2 sur une grille 7 par 6 avec comme dernier coup '-' pour le joueur 0, et 'C' pour le joueur 1, c'est au joueur 1 de jouer")
    G=Puissance4(grilletest,["-","C"])       
    Arb=arb_P4(2,G,["-","C"],1)
    minimax(Arb, Evaluation, 1, 2)
    print("on affiche les coups possibles grace au sous arbre du sommet initial :")
    for sousarb in Arb.get_sous_arb():
        affichage(sousarb)
        print(f"Le coup réalisé pour arriver à cet état est : {quelcoup(sousarb)}")
        print(f"valeur de la sous arborescence : {sousarb.get_valeur()}")
        if sousarb.get_valeur()==0:
            print(f"le coup à été élagé donc n'est pas pris en compte, sa valeur est 0, celle de base")
        if quelcoup(sousarb) in Alphabet[:7]:
            print(f"La valeur dependants des diagonales dispo grace au coup : {Verifdiag(sousarb,quelcoup(sousarb),1)} ")
            print(f"La valeur dependants des lignes dispo grace au coup : {Verifligne(sousarb,quelcoup(sousarb),1)} ")
    print(f"Le coup avec le plus de valeur est {quelcoup(trajet(Arb))}")
    print("Le coup de l'IA menera donc à l'état :")
    affichage(trajet(Arb))
