class Piece:
    # this class deals with the value of a piece.
    def __init__(self,designator):
        self.p = designator
        if self.p == 'first':
            #self.val = '🔴  ' # change piece icon here
            self.val = 1 # change piece icon here
        else:
            #self.val = '🔵  ' # change piece icon here
            self.val = 2 # change piece icon here
    def getValue(self):
        return self.val # red (1) or blue (2)
    def getOtherValue(self):
        if self.p == 'first':
            #return '🔵  '
            return 2
        else:
            #return '🔴  '
            return 1