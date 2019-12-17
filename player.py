class Player:
    def __init__(self, designator, playerType,gb,computer=False):
        if not computer:
            self.name = input("Enter "+designator+" player name:")
        self.p = designator
        self.t = playerType
    def getPlayerDesignator(self):
        return self.p
    def getPlayerName(self):
        return self.name
    def getPlayerType(self):
        return self.t
    def getPlay(self,gb,playerPiece, otherPiece):
        pass