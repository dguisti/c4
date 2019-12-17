from player import Player
import random
class ComputerPlayer(Player):
    # this class contains the logic for the computer player's moves.
    def __init__(self,designator,playerType,gb,computer=True):
        super().__init__(designator,playerType,gb,computer=True)
        self.name = "Dumb Computer"

    def nextMoveIsWinner(self,playerPiece,gb):
        # the computer player can block a player with three in a row, or try to win if it has three in a row
        #space = '◯  ' # empty space
        space = 0 # empty space
        piece = playerPiece # get player piece
        height = 7 #actually the width (col)
        width = 6  #actually the height (row)

        # check vertical spaces
        vlist = []
        for y in range(height): #columns
            for x in range(width - 3): #rows
                vlist.extend([gb[x][y], gb[x+1][y], gb[x+2][y], gb[x+3][y]])  # check all groups of four
                if sum(1 for c in vlist if c == piece) == 3 and sum(1 for c in vlist if c == space) == 1: # if there are three in a row, find the column with the blank space
                    this = vlist.index(space) 
                    return y
                else:
                    vlist.clear()
        
        # check horizontal spaces
        hlist = []
        for x in range(width): #rows
            for y in range(height - 3): #columns
                hlist.extend([gb[x][y], gb[x][y+1], gb[x][y+2], gb[x][y+3]]) # check all groups of four
                if sum(1 for c in hlist if c == piece) == 3 and sum(1 for c in hlist if c == space) == 1:  # if there are three in a row, find the column with the blank space             
                    this = hlist.index(space)
                    return y + this
                else:
                    hlist.clear()

        # check / diagonal spaces 
        drlist = []
        for x in range(width - 3): #rows
            for y in range(3, height): #columns
                drlist.extend([gb[x][y], gb[x+1][y-1], gb[x+2][y-2], gb[x+3][y-3]]) # check all groups of four
                if sum(1 for c in drlist if c == piece) == 3 and sum(1 for c in drlist if c == space) == 1: # if there are three in a row, find the column with the blank space
                    this = drlist.index(space) 
                    return y - this
                else:
                    drlist.clear()

        # check \ diagonal spaces
        dllist = []
        for x in range(width - 3): #rows
            for y in range(height - 3): #columns
                dllist.extend([gb[x][y], gb[x+1][y+1], gb[x+2][y+2], gb[x+3][y+3]]) # check all groups of four
                if sum(1 for c in dllist if c == piece) == 3 and sum(1 for c in dllist if c == space) == 1: # if there are three in a row, find the column with the blank space
                    this = dllist.index(space)             
                    return y + this
                else:
                    dllist.clear()

        return -1

    def getPlay(self,gb,playerPiece, otherPiece):
        compWin = self.nextMoveIsWinner(playerPiece,gb) # computer 3 in a row
        playerWin = self.nextMoveIsWinner(otherPiece,gb) # other player 3 in a row
        if compWin == -1:
            if playerWin == -1:
                return random.randint(0,6)
            else:
                return playerWin
        else:
            return compWin
