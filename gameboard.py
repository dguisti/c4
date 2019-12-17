
class GameBoard:
    # this class controls the appearance of the gameboard. The main functions add a piece and check for a winner.
    def __init__(self, *args, **kwargs):
        #self.emptySpace = "◯  " # change empty space here
        self.emptySpace = 0 # change empty space here (0)
        self.board = [[self.emptySpace for i in range(7)] for i in range(6)] # create a 6 x 7 board of empty spaces
    
    def getBoard(self):
        # reutrns the gameboard as a list
        return self.board 
    
    def displayBoard(self):
        # converts board to string and adds column numbers
        print("0123456")
        for row in self.board:
            for col in row:
                print(col,end='') 
            print(' ')

    def playAPiece(self, playerPiece, playerInput): 
        # takes player's desired column and current playing peice and adds peice to board
        column = playerInput
        piece = playerPiece.getValue()

        putItHere = 5 # try to place peice at the bottom row
        
        for row in range(6):
            elem = self.board[row][column]
            if elem != self.emptySpace:
                putItHere = row - 1 # if there is already a piece, move row up
                break

        rowList = self.board[putItHere] # find the row in list format
        newRow = rowList[:column] + [piece] + rowList[(column + 1):] # make a new row with the piece added
        self.board[putItHere] = newRow # replace new row with old row
        
        return self.board # return the new board

    def isWinner(self,playerPiece):
        # checks if there is four in a row of a specific piece on the gameboard
        piece = playerPiece.getValue() # get value of piece
        height = 7
        width = 6
        
        # check horizontal spaces
        for y in range(height):
            for x in range(width - 3):
                if self.board[x][y] == piece and self.board[x+1][y] == piece and self.board[x+2][y] == piece and self.board[x+3][y] == piece:
                    return True

        # check vertical spaces
        for x in range(width):
            for y in range(height - 3):
                if self.board[x][y] == piece and self.board[x][y+1] == piece and self.board[x][y+2] == piece and self.board[x][y+3] == piece:
                    return True

        # check / diagonal spaces
        for x in range(width - 3):
            for y in range(3, height):
                if self.board[x][y] == piece and self.board[x+1][y-1] == piece and self.board[x+2][y-2] == piece and self.board[x+3][y-3] == piece:
                    return True

        # check \ diagonal spaces
        for x in range(width - 3):
            for y in range(height - 3):
                if self.board[x][y] == piece and self.board[x+1][y+1] == piece and self.board[x+2][y+2] == piece and self.board[x+3][y+3] == piece:
                    return True

        return False