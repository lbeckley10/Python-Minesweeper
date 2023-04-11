#Author: Landon Beckley
import constants
import random

class Board:
    #Intialize the gameBoard and spriteBoard attributes
    def __init__(self):

        #gameBoard contains 0s for empty spaces and 1s for mines
        self.gameBoard = [[0 for i in range(constants.cols)] for j in range(constants.rows)]
        self.generated = False
        
        
    #Place the mines randomly throughout the 
    def generate(self,row,col):
        emptySpots = set()
        #Add every spot on board to the set of valid spots
        for i in range(16):
            for j in range(16):
                emptySpots.add((i,j))
        rLowerBound = row - 1
        rUpperBound = row + 1
        cLowerBound = col - 1
        cUpperBound = col + 1
        if(row == 0):
            rLowerBound = 0
            rUpperBound = row + 2
        if(row == 15):
            rUpperBound = 15
            rLowerBound = row - 2
        if(col == 0):
            cLowerBound = 0
            cUpperBound = col + 2
        if(col == 15):
            cUpperBound = 15
            cLowerBound = col - 2
        offLimits = set()
        for i in range(rLowerBound, rUpperBound+1):
            for j in range(cLowerBound, cUpperBound + 1):
                offLimits.add((i, j))
        for k in range(constants.noOfMines):
            i = random.randint(0,15)
            j = random.randint(0,15)
            while(not((i,j) in emptySpots) or ((i,j) in offLimits)):
                i = random.randint(0,15)
                j = random.randint(0,15)
            emptySpots.remove((i,j))
            self.gameBoard[i][j] = 1
        self.generated = True
    
    
    #Return the generated attribute
    def getGenerated(self):
        return self.generated

    #Return gameBoard attribute of self
    def getGameBoard(self):
        return self.gameBoard
    
    #Changes the value of an index in the gameBoard attribute
    def setGameBoard(self, row, col, val):
        self.gameBoard[row][col] = val