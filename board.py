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
        for i in range(16):
            for j in range(16):
                if((i,j) != (row,col)):
                    emptySpots.add((i,j))
        
        for k in range(constants.noOfMines): 
            i = random.randint(1,40)
            j = random.randint(1,40)
            while(not((i,j) in emptySpots)):
                i = random.randint(1,40)
                j = random.randint(1,40)
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