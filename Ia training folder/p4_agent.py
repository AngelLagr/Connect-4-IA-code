##Imports
import torch
import random
from collections import deque
from model import Linear_QNet, QTrainer
from helper import plot
from IAtrain.joueur import*

MAX_MEMORY = 100_000
BATCH_SIZE = 1000
LR = 0.001


##IA
Alphabet=["A","B","C","D","E","F"] #,"<",">","-","+","*A","*B","*C","*D","*E","*F","*G"]
class IAa():
    def __init__(self,etat,joueur=0,derniercoup="",valeur=0,rangee=6,colonne=7,nombre_jetons_victoire=4,sous_arb=[]):
        self.__valeur=valeur
        self.__rangee=rangee
        self.colonne=colonne
        self.__derniercoup=derniercoup
        if etat=="":
            self.__etat=[[" " for i in range(rangee)] for i in range(colonne)]
        else:
            self.__etat=etat
        self.__nombre_jetons_victoire=nombre_jetons_victoire
        self.__joueur=joueur
        self.__sous_arb=sous_arb[:]
        self.__valeur=0
        
        self.n_games = 0
        self.epsilon = 0 # randomness
        self.gamma = 0.9 # discount rate
        self.memory = deque(maxlen=MAX_MEMORY) # popleft()
        self.model = Linear_QNet(42, 256, 6)
        self.trainer = QTrainer(self.model, lr=LR, gamma=self.gamma)
        
    def get_derniercoup(self):
        return self.__derniercoup
    def set_derniercoup(self,valeur):
        self.__derniercoup=valeur
        
    def get_state(self):
        return self.__etat
    def set_etat(self,valeur):
        self.__etat=valeur
        
        
    def remember(self, state, action, reward, next_state, done):
        self.memory.append((state, action, reward, next_state, done)) # popleft if MAX_MEMORY is reached
        
    def train_long_memory(self):
        if len(self.memory) > BATCH_SIZE:
            mini_sample = random.sample(self.memory, BATCH_SIZE) # list of tuples
        else:
            mini_sample = self.memory

        states, actions, rewards, next_states, dones = zip(*mini_sample)
        self.trainer.train_step(states, actions, rewards, next_states, dones)
        #for state, action, reward, nexrt_state, done in mini_sample:
        #    self.trainer.train_step(state, action, reward, next_state, done)

    def train_short_memory(self, state, action, reward, next_state, done):
        self.trainer.train_step(state, action, reward, next_state, done)

        
    
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
        a_copie = IAa(self.get_difficulte(),self.get_etat(), self.get_joueur(),self.get_derniercoup(),self.get_valeur(),self.get_rangee(),self.get_colonne(),self.get_nombrejetons(),self.get_sous_arb())
        for ss_arb in self.get_sous_arb():
            a_copie.ajout_ss_arb(ss_arb.copie())
        return a_copie
    
    
    
    def get_action(self, state):
        # random moves: tradeoff exploration / exploitation
        self.epsilon = 500 - self.n_games
        if random.randint(0, 200) < self.epsilon:
            final_move = random.randint(0, len(Alphabet)-1)
        else:
            state0 = torch.tensor(state, dtype=torch.float)
            prediction = self.model(state0)
            final_move = torch.argmax(prediction).item()
            print(final_move,prediction)
        return final_move


def preprocess_state(state):
    mapping = {' ': 0, 'X': 1, 'O': 2}
    preprocessed_state=[]
    for row in state:
        for char in row:
            preprocessed_state.append(mapping[char])
    return preprocessed_state

def train():
    plot_scores = []
    plot_mean_scores = []
    total_score = 0
    record = -20
    nombre_de_coup=0
    done=False
    M = [[" ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " "],
         [" ", " ", " ", " ", " ", " ", " "]]
    agent = IAa(M)
    
    while True:
       
        if not done:
            # get old state
            state_old = preprocess_state(agent.get_state())
            # get move
            final_move = agent.get_action(state_old)
        
            # perform move and get new state        
            success,reward, done, score = jouer_coup(final_move,M)
            affichage(M)
            score = score-nombre_de_coup
            nombre_de_coup+=1
            
            if not success:
                print("PUNI")
                score=score-4    
            state_new = preprocess_state(agent.get_state())               
            # train short memory
            agent.train_short_memory(state_old, final_move, reward, state_new, done)
        
            # remember
            agent.remember(state_old, final_move, reward, state_new, done)
        


    
        if done:
            # train long memory, plot result*
            affichage(M)
            if verification_P4(M)=="X":
                score=-score
                
            M = [[" ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " "],
                 [" ", " ", " ", " ", " ", " ", " "]]
            
            agent.etat=M
            nombre_de_coup=0
            done=False
            
            agent.n_games += 1
            agent.train_long_memory()

            if score > record:
                record = score
                agent.model.save()
            
            
            print('Game', agent.n_games, 'Score', score, 'Record:', record)

            plot_scores.append(score)
            total_score += score
            mean_score = total_score / agent.n_games
            plot_mean_scores.append(mean_score)
            plot(plot_scores, plot_mean_scores)
            
            
        else: # si le coup aboutit on laisse l'IA jouer
            #l'IA joue:  
            
            done = jouer_coupia(M)
            nombre_de_coup+=1
            affichage(M)