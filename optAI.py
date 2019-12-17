import traingame
from player import Player
import random
import math
import time
import numpy as np
from collections import deque
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense
from tensorflow.keras.optimizers import Adam, SGD

GAMMA = 0.7 #discount factor for future value
ALPHA = 0.7 #how much the new information can change the existing information
LEARNING_RATE = 0.01

MEMORY_SIZE = 1_000_000
BATCH_SIZE = 10
LEARNING_SIZE = 100

EXPLORATION_MAX = 1.0
EXPLORATION_MIN = 0.01
EXPLORATION_DECAY = 0.9999

AVERAGE_THRESHOLD = 1000.0 #the number of steps we are trying to achieve

INDIVIDUAL_LEARNING = False

def sigmoid(z):
    return (1/(1+np.exp(-z)))

def gaussian(x, mu=0, sig=0.05):
    #gaussian function 
    #x is the input value
    #mu is the peak center position
    #sig is the width
    return np.exp(-np.power(x - mu, 2.) / (2 * np.power(sig, 2.)))

class AIPlayer(Player):
    # this class contains the logic for the computer player's moves.
    def __init__(self,designator,playerType,gb,computer=True):
        super().__init__(designator,playerType,gb,computer=True)
        self.name = "Kevin AI"
        #def __init__(self, state_space, action_space):
        self.exploration_rate = EXPLORATION_MAX
        self.action_space = 1 #the number of columns
        self.state_space = 6 # number of parameters
        #self.state_space = sum( [ len(listElem) for listElem in gb.getBoard()])

        #create the space to store "training" steps
        self.memory = deque(maxlen=MEMORY_SIZE)

        #create the Neural Network model - adjust as desired
        self.model = Sequential()
        self.model.add(Dense(self.state_space, input_shape=(self.state_space,),activation="linear"))
        self.model.add(Dense(48, activation="tanh"))
        self.model.add(Dense(self.action_space, activation="linear"))
        self.model.compile(loss="mse", optimizer=Adam(lr=LEARNING_RATE))


    def getPlay(self,state,playerPiece, otherPiece):
        flat_state = [item for sublist in state for item in sublist]
        return self.act(state)

    def remember(self, state, action, reward, next_state, done):
        #print(self.model.predict(state))
        #save information for learning
        flat_state = [item for sublist in state for item in sublist]
        flat_next_state = [item for sublist in next_state for item in sublist]
        #self.memory.append((np.asarray(flat_state).T, action, reward, np.asarray(flat_next_state).T, done))
        self.memory.append((np.array([flat_state]), action, reward, np.array([flat_next_state]), done))

    def save(self):
        #save the model
        fn = input("Enter model file name (include the .h5 file type). Enter nothing to skip saving.:")
        if fn != "":
            self.model.save(fn)
        #for future loading, use:        self.model = load_model('CartPoleModel.h5')

    def act(self, state):
        #predict an action during training
        #explore
        if np.random.rand() < self.exploration_rate:
            return random.randrange(self.action_space)
        #exploit
        flat_state = [item for sublist in state for item in sublist]
        #q_values = self.model.predict(np.asarray(flat_state).T)
        x = np.array([flat_state])
        q_values = self.model.predict(x)
        return np.argmax(q_values[0])

    def modelAct(self, state):
        #predict an action (not to be used during training)
        flat_state = [item for sublist in state for item in sublist]
        #q_values = self.model.predict(np.asarray(flat_state).T)
        x = np.array([flat_state])
        q_values = self.model.predict(x)
        return np.argmax(q_values[0])

    def learn(self):
        #the Q-learning algorithm used during training

        #don't do anything until you have enough data
        if len(self.memory) < LEARNING_SIZE: 
            return   
        #pick random data from all saved data to use to improve the model
        batch = random.sample(self.memory, LEARNING_SIZE)
        states_batch = []
        q_values_batch = []
    
        #use each set of data to improve the Q values
        for state, action, reward, state_next, terminal in batch:
            q_update = (reward + GAMMA * np.amax(self.model.predict(state_next))) if not terminal else reward
            q_values = self.model.predict(state)
            q_values_old = q_values[0][action]
            q_values[0][action] = (1-ALPHA)*q_values_old + ALPHA*q_update 
            if INDIVIDUAL_LEARNING:
                self.model.fit(state, q_values, epochs=10, verbose=0)
            else:
                states_batch.append(state[0])
                q_values_batch.append(q_values[0])

        if not INDIVIDUAL_LEARNING:
            #use the improved Q values to train the model  
            states_batch = np.array(states_batch).reshape(-1,self.state_space)
            q_values_batch = np.array(q_values_batch).reshape(-1,self.action_space)
            self.model.fit(states_batch, q_values_batch, batch_size= BATCH_SIZE, epochs=5, verbose=0)
    
        #reduce explorations
        self.exploration_rate *= EXPLORATION_DECAY
        self.exploration_rate = max(EXPLORATION_MIN, self.exploration_rate)

if __name__ == "__main__":
    reward = traingame.main(rmultw=0, rmultl=1, D1=16, D2=24)