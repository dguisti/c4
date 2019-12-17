"""
Fall Project 2019 for Python II. Connect Four using classes.
Modified by Dr. Brewer for AI training

:author Maya Park-Weber
:version 10-19
:python 3.6.5

"""

from gameboard import GameBoard
from piece import Piece
from player import Player
from computerPlayer import ComputerPlayer


from AIPlayer import AIPlayer as AIPlayer


NUMBER_OF_TRAINING_ROUNDS = int(input("Please input number of training cycles: "))

class Game:
    
    def __init__(self, RMULTW, RMULTL, D1, D2, D3, D4, *args, **kwargs):
        self.gb = GameBoard()
        self.playerComputer = ComputerPlayer("first","computerPlayer",self.gb,computer=True)
        self.playerAI = AIPlayer("second","AIPlayer",self.gb, D1, D2, D3, D4, computer=True) #change to AI player
        print("Created players")
        self.runTraining(RMULTW, RMULTL)

    def runTraining(self, RMULTW, RMULTL):
        wincount = 0
        for trainingRound in range(NUMBER_OF_TRAINING_ROUNDS):
            winpercent = wincount*100/(trainingRound+1)
            print("Training round:",trainingRound)
            print("\tPercent AI Win:", str(round(winpercent, 3)))
            #setup the training round
            self.gb = GameBoard() #initialize a new gameboard for each round
            #self.gb.displayBoard()
            done = False
            reward = 21
            print ("\tOutcome:" , end=" ")
            while not done: # play game until done
                #self.gb.displayBoard()
                reward -= 1
                #AI moves first in training
                piece = Piece(self.playerAI.getPlayerDesignator()) 
                theMove = self.playerAI.getPlay(self.gb.getBoard(),piece.getValue(),piece.getOtherValue())
                #print("AI move:",theMove)
                theState = self.gb.getBoard()
                self.gb.playAPiece(piece, theMove)
                if self.gb.isWinner(piece): # check for a winner
                    done = True
                    #self.gb.displayBoard()
                    print("AI Win")
                    wincount += 1
                   #### reward += 100*RMULTW
                else:
                    #now the computer moves
                    #self.gb.displayBoard()
                    piece = Piece(self.playerComputer.getPlayerDesignator()) 
                    theMove = self.playerComputer.getPlay(self.gb.getBoard(),piece.getValue(),piece.getOtherValue())
                    #print("Computer move:",theMove)
                    self.gb.playAPiece(piece, theMove)
                    if self.gb.isWinner(piece): # check for a winner
                        done = True
                        print("Maya Win")
                        reward *= -1*RMULTL
                    theNextState = self.gb.getBoard()

                self.playerAI.remember(theState, theMove, reward, theNextState, done)
                self.playerAI.learn()
        winpercent = wincount*100/(trainingRound+1)
        print("I won", str(round(winpercent, 3)) + "%", "of the time." , end=" ")

        self.winpercent = winpercent

def main(rmultw=0, rmultl=1, D1=96, D2=48, D3=24, D4=12):
    connectGame = Game(rmultw, rmultl, D1, D2, D3, D4)
    return connectGame.winpercent

if __name__ == "__main__":
    RMULTW = 1
    RMULTL = 50
    D1 = 96
    D2 = 48
    D3 = 24
    D4 = 12
    main(RMULTW, RMULTL, D1, D2, D3, D4)