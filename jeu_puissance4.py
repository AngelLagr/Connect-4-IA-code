##Imports

from p4_utils import * #importe tout car on importe p4 et p4_ia dans p4_utils

##Importations Tkinter
from tkinter import *
from tkinter import messagebox
import time

global menu_principal,jeu,vr,vc,nj,d,fen,canvas,c #on utilise des variables globales pour pouvoir les communiquer entre les differentes fonctions de tkinter

##Main sans Tkinter 

##Main en Joueur contre Joueur 

def main_jvj():
    """
    Met en place le jeu du puissance4 et permet du JVJ sur un Puissance 4 de base (grille 6x7 et 4 pions a aligner)

    Returns
    -------
    None

    """
    grille = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
    G=Puissance4(grille)
    joueur=0
    while G.victoire()[1]==3:
        if joueur == 0 : 
            coupjoueur=input("Le coup du joueur 0 est : ")
                    
            #condition et Debug:
            if coupjoueur=="break" or G.victoire()[0]==True:
                break
            
            #Le joueur joue :
            if G.jouer_coup(coupjoueur,joueur)==False: # si le coup n'aboutit pas on ne fais rien
                print("TU PEUX PAS")
                joueur = 1 - joueur 
                
        elif joueur == 1: 
            coupjoueur=input("Le coup du joueur 1 est : ")
                    
            #condition et Debug:
            if coupjoueur=="break" or G.victoire()[0]==True:
                break
            
            #Le joueur joue :
            if G.jouer_coup(coupjoueur,joueur)==False: # si le coup n'aboutit pas on ne fais rien
                print("TU PEUX PAS")
                joueur = 1 - joueur 
        
        else:
            print("problème de joueur")
            
        joueur = 1 - joueur 
        G.affichage()
            
    print(f'Le joueur n°{G.victoire()[1]} a Gagne')

##Main en Joueur contre IA 
def jeu_ia():
    """
    Met en place le jeu du puissance4 et permet au joueur de jouer contre une IA

    Returns
    -------
    None

    """
    grille = [[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "],[" "," "," "," "," "," "]]
    G=Puissance4(grille)
    difficulte=int(input("Difficulte de l'IA : "))
    coupIA=" "
    while G.victoire()[1]==3:
        coupjoueur=input("Le coup joue est : ")
                
        #condition et Debug:
        if coupjoueur=="break" or G.victoire()[0]==True:
            if G.victoire()[1]==0 : return "Le joueur n°0 a Gagne"
            break
        
        #Le joueur joue :
        if G.jouer_coup(coupjoueur,0)==False: # si le coup n'aboutit pas on ne fais rien
            print("TU PEUX PAS")
            G.affichage()
           
        if G.victoire()[1]==0:
            break
        else: # si le coup aboutit on laisse l'IA jouer
            #l'IA joue:  
            
            Arb=arb_P4(difficulte,G,[coupjoueur,coupIA],1)
            minimax(Arb,Evaluation,1,difficulte)   
            
            coupIA=f"{trajet(Arb)}"[-1]
            
            print(f"\n COUP DE L'IA : {coupIA}")
            G.jouer_coup(coupIA,1)
            G.affichage()
        
    print(f'Le joueur n°{G.victoire()[1]} a Gagne')

##Tkinter

def menu():
    """
    Affcihe un menu pouor choisir les parametres du jeu Puissance 4 

    Returns
    -------
    None.

    """
    global menu_principal,vr,vc,nj,d
    
    #mise en place de la fenetre Tkinter du menu 
    menu_principal = Tk()
    menu_principal.title("Menu Principal du Puissance 4")
    menu_principal.minsize(1150,500)
    menu_principal.configure(bg="#FFEBCD")
    
    #Type de Jeu
    Frame_mode= Frame(menu_principal, borderwidth=2, relief=GROOVE,bg="#F5DEB3")
    Label(Frame_mode, text="Mode",bg="#F5DEB3").pack(padx=10, pady=10)
    
    #Difficulte
    Frame_difficulte = Frame(Frame_mode, borderwidth=2, relief=GROOVE,bg="#FFEBCD")
    Frame_difficulte.pack(padx=50,pady=10)
    Label(Frame_difficulte, text="Difficulte IA / JVJ ",bg="#FFEBCD").pack(padx=10, pady=10)
    
    def updateDifficulte(event=None): #fonction qui permet de modifier le label d'affichafe de la difficulte 
        global d
        item=difficulte.get(difficulte.curselection()[0])
        d.set(item)

    d=StringVar()
    
    difficulte = Listbox(Frame_difficulte)
    difficulte.insert(1,"Joueur contre Joueur")
    difficulte.insert(2, "1")
    difficulte.insert(3, "2")
    difficulte.insert(4, "4")
    difficulte.insert(5, "6")
    
    
    difficulte.bind("<<ListboxSelect>>",updateDifficulte)
    difficulte.select_set(0)

    difficulte.pack()

    lbl = Label(Frame_mode, textvariable=d,bg="#F5DEB3")
    lbl.pack()

    Frame_mode.grid(row=0,column=1,padx=10,pady=10)

   
    #Rangee
    def rangee():
       selected = "Rangees : " + str(vr.get())
       label_r.config(text = selected)
    
    vr = DoubleVar()
    vr.set(6)
    select_rangee = Scale(menu_principal, from_=4, to=26, variable = vr,bg="#FFEBCD",highlightthickness=0)
    select_rangee.grid(row=0,column=3,padx=100)
    
    bouton_rangee = Button(menu_principal, text="Selectionner le nombre de rangees",bg="#F5DEB3", command=rangee)
    bouton_rangee.grid(row=1,column=3,padx=10)
    
    label_r = Label(menu_principal,bg="#FFEBCD")
    label_r.grid(row=2,column=3)
    
    #Colonne
    def colonne():
       selected = "Colonnes : " + str(vc.get())
       label_c.config(text = selected)
    
    vc = DoubleVar()
    vc.set(7)
    select_colonne = Scale(menu_principal, from_=4, to=26, variable = vc,bg="#FFEBCD",highlightthickness=0) 
    select_colonne.grid(row=0,column=5,padx=100)
    
    bouton_colonne = Button(menu_principal, text="Selectionner le nombre de colonnes",bg="#F5DEB3", command=colonne)
    bouton_colonne.grid(row=1,column=5,padx=10)
    
    label_c = Label(menu_principal,bg="#FFEBCD")
    label_c.grid(row=2,column=5)
    
    #Nombre de jetons a aligner
    def jetons():
        if min(int(vr.get()),int(vr.get()))<int(nj.get()):
            selected = "Veuillez selectionner un nombre entre rangee et colonne"
            nj.set(4)
        else:
            selected = "Nombre de jetons a aligner : " + str(nj.get())
        label_j.config(text = selected)
    
    nj = DoubleVar()
    nj.set(4)
    select_colonne = Scale(menu_principal, from_=3, to=26, variable = nj,bg="#FFEBCD",highlightthickness=0) 
    select_colonne.grid(row=0,column=7,padx=100)
    
    bouton_colonne = Button(menu_principal, text="Selectionner le nombre de jetons a aligner",bg="#F5DEB3", command=jetons)
    bouton_colonne.grid(row=1,column=7,padx=10)
    
    label_j = Label(menu_principal,bg="#FFEBCD")
    label_j.grid(row=2,column=7)
    
    #Lancer le Jeu
    lancement=Button(menu_principal,text="Lancer le Jeu",bg="#F5DEB3",command=lancer)
    lancement.grid(row=5,column=5,pady=10)
    
    menu_principal.mainloop()
    
    
def lancer():
    """
    Lance une nouvelle fenetre de Tkinter avce une grille de puissance 4 

    Returns
    -------
    None.

    """
    global menu_principal,jeu,d
    if d.get()=='':
        erreurLancement = messagebox.showerror("Erreur de Difficulte", "Veuillez selectionner une difficulte")
    else:
        menu_principal.iconify()
        jeuP4()


##Jeu

##Dessin de la Grille

def dessine_tab(G):
    """
    Dessine un etat du jeu de Puissance 4 sur tkinter en créant un rectangle pour chaque case 

    Parameters
    ----------
    G : Puissance4
        
    Returns
    -------
    None.

    """
    global canvas,fen,cote
    canvas.delete("all")
    for l in range(G.rangee):
        for p in range(G.colonne):
            canvas.create_rectangle(cote*(p+1),cote*(l+1/2),cote*(p+2),cote*(l+3/2),fill="white",outline="blue",width=2)
            if G.grille[p][l]=="O":
                canvas.create_oval(cote*(p+1),cote*(l+1/2),cote*(p+2),cote*(l+3/2),fill="red",outline="black",width=2)
            elif G.grille[p][l]=="X": 
                canvas.create_oval(cote*(p+1),cote*(l+1/2),cote*(p+2),cote*(l+3/2),fill="yellow",outline="black",width=2)
    for i in range(G.colonne):
        txt = canvas.create_text(cote*(i+3/2),G.rangee*cote+75, text=Alphabet[i], font="Arial 16 italic", fill="blue")
    fen.update()

##Coup Joueur

def getCoup(event):
    global c,coup
    c=coup.get()
    print(c)
    coup.delete(0,END)
    return(c)

##Victoire 

def victoire_tk(j):
    time.sleep(1)
    MsgBox = messagebox.showwarning("Victoire", f"Victoire du joueur {j}")
    if MsgBox == 'ok':
       fen.destroy()
       menu_principal.deiconify()

##Main Joueur Contre Joueur 

def main_jvj_tk(G):
    global jeu,menu_principal,vr,vc,nj,d,fen,canvas,coup,c,label_joueur
    joueur=0
    while G.victoire()[1]==3:
        label_joueur.config(text=f"C'est au tour du joueur {joueur}")
        if joueur == 0 : 
            coupjoueur=c.upper()
            c=''
            
            if coupjoueur=="":
                joueur=1-joueur
                
            #condition et Debug:
            elif coupjoueur=="break" or G.victoire()[0]==True:
                break
            
            #Le joueur joue :
            elif G.jouer_coup(coupjoueur,joueur)==False: # si le coup n'aboutit pas on ne fais rien
                MessageErreur = messagebox.showinfo("Erreur de Coup", "Vous ne pouvez pas jouer ce coup")
                joueur=1-joueur
                
        elif joueur == 1: 
            coupjoueur=c.upper()
            c=''
            
            if coupjoueur=="":
                joueur=1-joueur
                    
            #condition et Debug:
            elif coupjoueur=="break" or G.victoire()[0]==True:
                break
            
            #Le joueur joue :
            elif G.jouer_coup(coupjoueur,joueur)==False: # si le coup n'aboutit pas on ne fais rien
                MessageErreur = messagebox.showinfo("Erreur de Coup", "Vous ne pouvez pas jouer ce coup")
                joueur = 1 - joueur 

        
        else:
            print("Probleme de Joueur")
            
        joueur = 1 - joueur 
        dessine_tab(G)
            
    victoire_tk(G.victoire()[1])

##Main Joueur VS IA
def coup_IA(etat:Puissance4,d:int,coupjoueur:str,coupIA:str):
    """
    permet de recuperer le coup jouer par l'IA
    """
    global fen,label_joueur,label_IA
    label_joueur.config(text="L'IA Joue ( Jaune )")
    
    fen.update()
    Arb=arb_P4(d,etat,[coupjoueur,coupIA],1)
    minimax(Arb,Evaluation,1,d)   
    
    coupIA=f"{quelcoup(trajet(Arb))}"
    
    label_IA.config(text=f"Le coup de L'IA est : {coupIA}")
    print(coupIA)
    
    return(coupIA)

def main_IA(G):
    global jeu,menu_principal,vr,vc,nj,d,fen,canvas,coup,c,label_joueur,label_IA
    difficulte=int(d.get())
    
    label_IA=Label(fen)
    label_IA.grid(row=3,column=1)
    label_IA.config(bg="#FFEBCD")
    
    while G.victoire()[1]==3:
        label_joueur.config(text=f"C'est au tour du Joueur Humain ( Rouge )")
        coupjoueur=c.upper()
        c=''
        
        if coupjoueur=="":
            c+=c
    
        #condition et Debug:
        elif coupjoueur=="break" or G.victoire()[0]==True:
            break
        
        #Le joueur joue :
        elif G.jouer_coup(coupjoueur,0)==False: # si le coup n'aboutit pas on ne fais rien
            label_IA.config(text="Tu pEuX pAS")
        
        elif G.victoire()[1]==0:
            dessine_tab(G)
            break
        
        else: # si le coup aboutit on laisse l'IA jouer
            #l'IA joue:
            cj,cia=G.derniers_coups[0], G.derniers_coups[1] 
            c_ia=coup_IA(G,difficulte,cj,cia)
            G.jouer_coup(c_ia,1)
            
        dessine_tab(G)
        
            
    victoire_tk(G.victoire()[1])


def jeuP4():
    global fen,menu_principal,vr,vc,nj,d,jeu,canvas,coup,cote,c,label_joueur
    
    rangee=int(vr.get())
    colonne=int(vc.get())
    nombre_a_aligner=int(nj.get())
    diff=d.get()
    
    c=''
    
    cote = 50
    larFen=colonne*cote
    hautFen=rangee*cote
    
    fen = Toplevel(menu_principal)
    fen.title("Jeu Puissance 4")
    fen.minsize(int(6/5*larFen),int(2*hautFen))
    fen.configure(bg="#FFEBCD")
    
    gP4 = [[" " for i in range(rangee)] for j in range(colonne)]
    jeu=Puissance4(gP4,["",""],[1,1],["O","X"],colonne,rangee,nombre_a_aligner)
    
    m=max(larFen,hautFen)
    canvas=Canvas(fen,bg="#FFEBCD",highlightthickness=0,width=m+100,height=m+100)
    canvas.grid(row=0,column=0)

    jeu.affichage()
    
    coup=Entry(fen)
    coup.grid(row=1,column=0)
    
    btn=Button(fen,height=1,width=10,text="Valider Coup", command=getCoup)
    btn.grid(row=2,column=0,pady=10)
    
    label_joueur=Label(fen)
    label_joueur.config(bg="#FFEBCD")
    label_joueur.grid(row=3,column=0)
    
    fen.bind('<Return>',getCoup)
    
    #etat_jeu=Label(fen,text="") a faire 
    
    dessine_tab(jeu)
    
    if diff == "Joueur contre Joueur":
        main_jvj_tk(jeu)
    
    else :
        main_IA(jeu)
        
    
    fen.mainloop()

if __name__=="__main__":
    menu()