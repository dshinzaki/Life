# Dylan Shinzaki
# 9/10/13
# Basic implementation of Conway's game of life using a finite
# universe represented by a 2d array

# BasicLife(n): constructs nxn universe indexed from 0 to n-1
# toggle(i,j): changes the state of (i, j) to the opposite
# getState(i, j): Returns true if (i, j) is live and false otherwise
# setLive(i, j): Sets (i, j) to be alive
# setDead(i, j): Sets (i, j) to be dead
# nextGeneration(): Simulates the next generation based game of 
#   life rules
# exportGrid(): Returns nxn grid representing the universe.
# printGrid(): Prints the universe in a human-readable format

# Execution:
# python basicLife.py
# Executes a test script

class BasicLife(object):
    LIVE = 1
    DEAD = 0
    def __init__(self, size=0):
        assert type(size) is int, "size is not an integer: %r" % size
        assert size >= 0, "size is negative: %r" % size
        
        self.size = size
        self.grid = [[0]*size for i in range(size)]
    
    def toggle(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
        if self.grid[i][j]:
            self.setDead(i, j)
        else:
            self.setLive(i, j)
    
    def getState(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
        return self.grid[i][j]        
    
    def setLive(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        self.grid[i][j] = self.LIVE
    
    def setDead(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        self.grid[i][j] = self.DEAD
    
    # Visits each neighbor (with wrap around) to count the number
    # of live neighbors to determine the fate of the current cell
    def __nextGenerationBit(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
        
        liveNeighbor = 0
        
        leftI = i-1 if i-1 >= 0 else self.size-1
        rightI = i+1 if i+1 < self.size else 0
        leftJ = j-1 if j-1 >= 0 else self.size-1
        rightJ = j+1 if j+1 < self.size else 0
        
        liveNeighbor += self.grid[leftI][leftJ]
        liveNeighbor += self.grid[leftI][j]
        liveNeighbor += self.grid[leftI][rightJ]
        
        liveNeighbor += self.grid[i][leftJ]
        liveNeighbor += self.grid[i][rightJ]
        
        liveNeighbor += self.grid[rightI][leftJ]
        liveNeighbor += self.grid[rightI][j]
        liveNeighbor += self.grid[rightI][rightJ]
        
        if self.grid[i][j]:
            return (liveNeighbor == 2) or (liveNeighbor == 3)
        else:
            return liveNeighbor == 3
            
    def nextGeneration(self):
        tmpGrid = [[0]*self.size for i in range(self.size)]
        for i in range(self.size):
            for j in range(self.size):
                tmpGrid[i][j] = self.__nextGenerationBit(i,j)
        self.grid = tmpGrid
        
    def exportGrid(self):
        return self.grid
        
    def printGrid(self):
        for i in range(self.size):
            currLine = ""
            for j in range(self.size):
                if self.grid[i][j]:
                    currLine = currLine + "x"
                else:
                    currLine = currLine + "."
            print currLine
            

if __name__=="__main__":
    print "Testing 10X10 world"
    life = BasicLife(10)
    life.setLive(4,5)
    life.setLive(5,5)
    life.setLive(6,5)
    
    print "Generation 1:"
    life.printGrid()
    life.nextGeneration()
    print "Generation 2:"
    life.printGrid()
    life.nextGeneration()
    print "Generation 3:"    
    life.printGrid()
    life.nextGeneration()
    print "Generation 4:" 
    life.printGrid()
        