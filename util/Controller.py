class Controller:
    def __init__(self, left, right, up, down):
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        
    #returns movement as a tuple
    def getMovementVectors(self):
        x = 0
        y = 0
        if self.left:
            x -= 1
        if self.right:
            x+=1
        if self.up:
            y -= 1
        if self.down:
            y+=1
        return (x,y)
    def copyTo(self,receiver):
        receiver.left = self.left
        receiver.right = self.right
        receiver.up = self.up
        receiver.down = self.down