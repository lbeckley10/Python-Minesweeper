#Author: Landon Beckley
import constants
import random

class Board:
    #Intialize the gameBoard and spriteBoard attributes
    def __init__(self):

        #gameBoard contains 0s for empty spaces and 1s for mines
        self.gameBoard = [[0 for i in range(constants.cols)] for j in range(constants.rows)]
        self.generated = False
        
        
    #Clears the current game board
    def clear(self):
        for i in range(constants.cols):
            for j in range(constants.rows):
                self.gameBoard[i][j] = 0
    
    #Place the mines randomly throughout the 
    def generate(self,row,col):
        self.clear()
        emptySpots = set()
        #Add every spot on board to the set of valid spots
        for i in range(constants.cols):
            for j in range(constants.rows):
                emptySpots.add((i,j))
        rLowerBound = row - 1
        rUpperBound = row + 1
        cLowerBound = col - 1
        cUpperBound = col + 1
        if(row == 0):
            rLowerBound = 0
            rUpperBound = row + 2
        if(row == constants.rows-1):
            rUpperBound = constants.rows-1
            rLowerBound = row - 2
        if(col == 0):
            cLowerBound = 0
            cUpperBound = col + 2
        if(col == constants.cols-1):
            cUpperBound = constants.cols-1
            cLowerBound = col - 2
        offLimits = set()
        for i in range(rLowerBound, rUpperBound+1):
            for j in range(cLowerBound, cUpperBound + 1):
                offLimits.add((i, j))
        for k in range(constants.noOfMines):
            i = random.randint(0,constants.cols-1)
            j = random.randint(0,constants.rows-1)
            while(not((i,j) in emptySpots) or ((i,j) in offLimits)):
                i = random.randint(0,constants.rows-1)
                j = random.randint(0,constants.cols-1)
            emptySpots.remove((i,j))
            self.gameBoard[i][j] = 1
        self.generated = True
    
    
    #Return the generated attribute
    def getGenerated(self):
        return self.generated
    
    #Sets the generated attribute
    def setGenerated(self, generated):
        self.generated = generated

    #Return gameBoard attribute of self
    def getGameBoard(self):
        return self.gameBoard
    
    #Changes the value of an index in the gameBoard attribute
    def setGameBoard(self, row, col, val):
        self.gameBoard[row][col] = val