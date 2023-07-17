##Imports
from copy import deepcopy

from p4 import * 
from p4_utils import *

##IA

class IA():
    def __init__(self,difficulte,etat,joueur=0,derniercoup="",valeur=0,rangee=6,colonne=7,nombre_jetons_victoire=4,sous_arb=[]):
        self.__valeur=valeur
        self.__rangee=rangee
        self.__colonne=colonne
        self.__difficulte=difficulte
        self.__derniercoup=derniercoup
        if etat=="":
            self.__etat=[[" " for i in range(rangee)] for i in range(colonne)]
        else:
            self.__etat=etat
        self.__nombre_jetons_victoire=nombre_jetons_victoire
        self.__joueur=joueur
        self.__sous_arb=sous_arb[:]
        self.__valeur=0
        
        
    def get_derniercoup(self):
        return self.__derniercoup
    def set_derniercoup(self,valeur):
        self.__derniercoup=valeur
        
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
        return f"{self.get_etat()}{self.get_derniercoup()}"
    
    def ajout_ss_arb(self,other):
        self.set_sous_arb(other)
        
    def est_feuille(self):
        if self.get_sous_arb()==[] :
            return True
        else:         
            return False
        
    def copie(self):
        a_copie = IA(self.get_difficulte(),self.get_etat(), self.get_joueur(),self.get_derniercoup(),self.get_valeur(),self.get_rangee(),self.get_colonne(),self.get_nombrejetons(),self.get_sous_arb())
        for ss_arb in self.get_sous_arb():
            a_copie.ajout_ss_arb(ss_arb.copie())
        return a_copie
    
    def jouer_coup(self,jeu:Puissance4):
        Arb=arb_P4(self.difficulte,jeu,[jeu.derniers_coups[0],jeu.derniers_coups[1]],1)
        minimax(Arb,Evaluation,1,self.difficulte)   
        coupIA=f"{quelcoup(trajet(Arb))}"
        jeu.jouer_coup(coup_IA,1)

  