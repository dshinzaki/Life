# Dylan Shinzaki
# 9/10/13
# Improved implementation of Conway's game of life using a finite
# universe represented by a 2d array
# Uses a list of changed nodes. The program only inspects the
# changed nodes and neighbors of the changed nodes when 
# calculating the next generation. Additionally, it keeps 
# a running grid which contains the number of live neighbors to
# speed up calculating a cell's fate.

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
# python neighborLife.py
# Executes a test script

from basicLife import BasicLife
from sets import Set

class NeighborLife(BasicLife):
    LIVE = 1
    DEAD = 0
 
    def __init__(self, size=0):
        super(NeighborLife,self).__init__(size)
        self.neighborGrid = [[0]*self.size for i in range(self.size)]
        # An item is included in changeList if it or a neighbor was 
        # changed since the last generation. Only these cells
        # need to be visited 
        self.changeList = Set()
            
    # Helper function to update bookkeeping. It adds
    # the cell and its neighbors to the change list and updates
    # the neighbor's counts of live neighbors
    def __addToList(self, i, j, state):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
        if self.grid[i][j] != state:
            return
           
        if state:
            value = 1
        else:
            value = -1
            
        for x in (i-1, i, i+1):
            for y in (j-1, j, j+1):
                x = x if x >= 0 else self.size-1
                x = x if x < self.size else 0
                
                y = y if y >= 0 else self.size-1
                y = y if y < self.size else 0
                    
                t = x, y
                self.changeList.add(t)
                
                if x != i or y != j:
                    self.neighborGrid[x][y] += value  
                       
    
    def setLive(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        if self.grid[i][j] == self.LIVE:
            return
        super(NeighborLife, self).setLive(i,j)   
        self.__addToList(i, j, self.LIVE)

    
    def setDead(self, i, j):
        assert type(i) is int,  "i is not an integer: %r" % i
        assert type(j) is int,  "j is not an integer: %r" % j
    
        if self.grid[i][j] == self.DEAD:
            return
            
        super(NeighborLife, self).setDead(i,j)
        self.__addToList(i, j, self.DEAD)
        
    def __printNeighbors(self):
        for i in range(self.size):
            currList = ""
            for j in range(self.size):
                currList = currList + str(self.neighborGrid[i][j])
            print currList
    
    def nextGeneration(self):
        currList = self.changeList
        toggleList = Set()
        self.changeList = Set()

        for point in currList:
            i = point[0]
            j = point[1]
            if self.grid[i][j]:
                if (self.neighborGrid[i][j] != 2) and \
                    (self.neighborGrid[i][j] != 3):           
                    toggleList.add((i, j))
            else:
                if self.neighborGrid[i][j] == 3:
                    toggleList.add((i, j))
        
        for point in toggleList:
            if self.grid[point[0]][point[1]]:
                self.setDead(point[0], point[1])
            else:
                self.setLive(point[0], point[1])           
                
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
    