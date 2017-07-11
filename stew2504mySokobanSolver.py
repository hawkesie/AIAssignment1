
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban

from sokoban import Warehouse


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [(7521022, 'Jordan', 'Hawkes'),(7561555, 'Stewart','Whitehead')]
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -






def tabooCorners(warehouse, taboo):
    '''
    Finds corners of a warehouse which is not a target, wall or already
    marked as taboo and appends them to a list
    '''
    ne = (1, -1)
    se = (1, 1)
    sw = (-1, 1)
    nw = (-1, -1)
    corners = [ne, se, sw, nw]
    
    for corner in corners:
        for x,y in warehouse.walls:
            if (x + corner[0], y + corner[1]) in warehouse.walls:
                if ((x + corner[0]), y) not in warehouse.targets + warehouse.walls + taboo:
                        taboo.append(((x + corner[0]), y))
                if (x, (y + corner[1])) not in warehouse.targets + warehouse.walls + taboo:
                        taboo.append((x, (y + corner[1])))
                    

def foundOtherTabooCorner(currentCellX, currentCellY, wallDirection, taboo, warehouse):

        #Found another taboo corner, cells lining walls are all taboo
        x = currentCellX + wallDirection[0]
        y = currentCellY + wallDirection[1]
        if (x, y) in taboo:
            return True
        else:
            return False
            

def appendToOtherTabooCorner(currentCellx, currentCelly, startCellX, startCellY, direction, taboo):    
            # For walls travelling horizonatally
            #if currentCellY == startCellY:
            if direction == (1, 0) or (-1, 0):
                cellsTravelled = abs(currentCellx - startCellX)
                while cellsTravelled > 0:
                    if startCellX > currentCellx:
                        taboo.append((startCellX - cellsTravelled, startCellY))
                        cellsTravelled -= 1
                    elif startCellX < currentCellx:
                        taboo.append((startCellX + cellsTravelled, startCellY))
                        cellsTravelled -= 1
                        
            # For walls travelling vertically
            ##if currentCellX == startCellX:
            if direction == (0, 1) or (0, -1):
                cellsTravelled = (abs (currentCelly - startCellY))
                while cellsTravelled > 0:
                    if startCellY > currentCelly:
                        taboo.append((startCellX, startCellY - cellsTravelled))
                        cellsTravelled -= 1
                    elif startCellY < currentCelly:
                        taboo.append((startCellX, startCellY + cellsTravelled))
                        cellsTravelled -= 1

def tabooAgainstWall(warehouse, taboo):
    '''
    
    '''
    n = (0, -1)
    e = (1, 0)
    s = (0, 1)
    w = (-1, 0)
    
    originalTaboos = taboo
    
    direction = [n, e, s, w]
    for cell in originalTaboos:
        currentCellX = cell[0]
        currentCellY = cell[1]
        counter = 0
        
        for step in direction:
            
            horizontal = (e, w)
            vertical = (n, s)            
            #Direction we are checking
            if (step[0] != 0):
                checkWallPlane = vertical
            else:
                checkWallPlane = horizontal
                
            checkCell = (currentCellX + step[0], currentCellY + step[1])
            
            if (foundOtherTabooCorner(currentCellX, currentCellY, (step[0], step[1]), originalTaboos, warehouse) and counter > 0):
                appendToOtherTabooCorner(currentCellX, currentCellY, cell[0], cell[1], step, taboo)
            
            for plane in checkWallPlane:
                cornerFound = False
                counter = 0

                while cornerFound == False:
                    if checkCell in taboo:
                        cornerFound = True
                        if counter > 0:
                            appendToOtherTabooCorner(currentCellX, currentCellY, cell[0], cell[1], step, taboo)
                            cornerFound = True
                        else:
                            continue
                    elif checkCell in warehouse.walls:
                        cornerFound = True
                    elif checkCell in warehouse.targets:
                        cornerFound = True
                    elif (checkCell[0] + plane[0], checkCell[1] + plane[1]) not in warehouse.walls:
                        cornerFound = True
                    else:
                        counter += 1
                        currentCellX = checkCell[0]
                        currentCellY = checkCell[1]
                        checkCell = (currentCellX + step[0], currentCellY + step[1])
            

def taboo_cells(warehouse):
    '''  
    Identify the taboo cells of a warehouse. A cell is called 'taboo' 
    if whenever a box get pushed on such a cell then the puzzle becomes unsolvable.  
    When determining the taboo cells, you must ignore all the existing boxes, 
    simply consider the walls and the target  cells.  
    Use only the following two rules to determine the taboo cells;
     Rule 1: if a cell is a corner and not a target, then it is a taboo cell.
     Rule 2: all the cells between two corners along a wall are taboo if none of 
             these cells is a target.
    
    @param warehouse: a Warehouse object

    @return
       A string representing the puzzle with only the wall cells marked with 
       an '#' and the taboo cells marked with an 'X'.  
       The returned string should NOT have marks for the worker, the targets,
       and the boxes.  
    '''
    ##         "INSERT YOUR CODE HERE" 
    tabooCells=[]
    tabooCorners(warehouse, tabooCells)
    tabooAgainstWall(warehouse, tabooCells)
    
    X,Y = zip(*warehouse.walls)
    xLength= 1+max(X)
    yLength = 1+max(Y)
    charImage = [[" "] * xLength for y in range(yLength)]
    for (x,y) in warehouse.walls:
        charImage[y][x]="#"
    for (x,y) in tabooCells:
        charImage[y][x]="X"
        
    

    answer = "\n".join(["".join(row) for row in charImage])
    return answer
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -





class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.
    
    	Use the sliding puzzle and the pancake puzzle for inspiration!
    
    '''
    ##         "INSERT YOUR CODE HERE"
    
    def __init__(self, warehouse):
        problem_file = "./warehouses/warehouse_01.txt"
        self.initial=Warehouse();
        self.initial.read_warehouse_file(problem_file)
        self.taboos=taboo_cells(self.initial)
        self.worker=self.initial.worker
        self.walls=self.initial.walls
        self.boxes=self.initial.boxes
        self.targets=self.initial.targets
    

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        x,y=state.worker
        workerActions = ['Left', 'Right', 'Up', 'Down']
        numbers=[0,1,2,3]
        executableActions=[]
        
        
        moves= [(-1,0),(1,0),(0,-1),(0,1)]
        for move in numbers:                   
                xoff,yoff=moves[move]               
                if (((x+xoff,y+yoff) not in self.walls) & ((x+xoff,y+yoff) not in state.boxes)):
                    executableActions.append((workerActions[move]))
                
                elif (((x+xoff,y+yoff) not in self.walls) & ((x+xoff,y+yoff) in state.boxes)):
                    if (((x+xoff*2,y+yoff*2) not in self.taboos) & ((x+xoff*2,y+yoff*2) not in self.walls)):
                        executableActions.append((workerActions[move]))  
                
        return executableActions

    def goal_test(state):
        for box in state.boxes:       
            if box in state.targets:
                continue
            else:
                return False   
        return True
    
    def result(self, state, action):
        """Return the state that results from executing the given
        action in the given state. The action must be one of
        self.actions(state)."""
        tempState = state
        
        workerActions = ['Left', 'Right', 'Up', 'Down']   
        x,y=tempState.worker
        
        
        if action == workerActions[0]:
            xoff,yoff=(-1,0)
        elif action == workerActions[1]:
            xoff,yoff=(1,0)
        elif action == workerActions[2]:
            xoff,yoff=(0,-1)
        elif action == workerActions[3]:
            xoff,yoff=(0,1)
                
        if (((x+xoff,y+yoff) not in tempState.walls) & ((x+xoff,y+yoff) not in tempState.boxes)):
            
            tempState.worker=(x+xoff,y+yoff)
                
        elif (((x+xoff,y+yoff) not in tempState.walls) & ((x+xoff,y+yoff) in tempState.boxes)):
            if (x+xoff*2,y+yoff*2) not in tempState.taboos & (x+xoff*2,y+yoff*2) not in tempState.walls:
                tempState.boxes.remove(x+xoff,y+yoff)
                tempState.boxes.append(x+xoff*2,y+yoff*2)
                tempState.worker.remove(x,y)
                tempState.worker.append(x+xoff,y+yoff)
                
        return tempState
        
        
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c+1
        
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def check_action_seq(warehouse, action_seq):
    '''
    
    Determine if the sequence of actions listed in 'action_seq' is legal or not.
    
    Important notes:
      - a legal sequence of actions does not necessarily solve the puzzle.
      - an action is legal even if it pushes a box onto a taboo cell.
        
    @param warehouse: a valid Warehouse object

    @param action_seq: a sequence of legal actions.
           For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
           
    @return
        The string 'Failure', if one of the action was not successul.
           For example, if the agent tries to push two boxes at the same time,
                        or push one box into a wall.
        Otherwise, if all actions were successful, return                 
               A string representing the state of the puzzle after applying
               the sequence of actions.  This must be the same string as the
               string returned by the method  Warehouse.__str__()
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    puzzle = SokobanPuzzle(search.Problem)
    currentState=puzzle
    for acts in action_seq:
        if acts in currentState.actions(currentState):
            currentState = currentState.result(currentState, acts)
            #creating string representation of currentState because I couldn't get _str_() to work
            X,Y = zip(*currentState.walls)
            xLength= 1+max(X)
            yLength = 1+max(Y)
            charImage = [[" "] * xLength for y in range(yLength)]
            for (x,y) in currentState.walls:
                charImage[y][x]="#"
            for (x,y) in currentState.targets:
                charImage[y][x]="."
            for (x,y) in currentState.boxes:
                if charImage[y][x] == ".": # if on target
                      charImage[y][x] = "*"
                else:
                    charImage[y][x] = "$"
            if charImage[currentState.worker[1]][currentState.worker[0]] == ".":
                charImage[currentState.worker[1]][currentState.worker[0]] = "!"
            else:
                charImage[currentState.worker[1]][currentState.worker[0]] = "@"
 
            answer = "\n".join(["".join(row) for row in charImage])
           
        else:
            return ('Failure')
        
    return (answer)
        


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
warehouse=0
def solve_sokoban_elem(warehouse):
    '''    
    This function should solve using elementary actions 
    the puzzle defined in a file.
    
    @param warehouse: a valid Warehouse object

    @return
        A list of strings.
        If puzzle cannot be solved return ['Impossible']
        If a solution was found, return a list of elementary actions that solves
            the given puzzle coded with 'Left', 'Right', 'Up', 'Down'
            For example, ['Left', 'Down', Down','Right', 'Up', 'Down']
            If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    puzzle = SokobanPuzzle(search.Problem)
    actionList=[]
    
    h=checkDistances(puzzle)
    
    astar_graph_search(puzzle, h)
    
        
    
    

def checkDistances(puzzle):
    lowestDists=[]
    for box in puzzle.boxes:
        lowestDistance=100
        for targs in puzzle.targets:
            xdistance=box[0]-targs[0]
            ydistance=box[1]-targs[1]
            if(xdistance<0):
                xdistance=-xdistance
            if(ydistance<0):
                ydistance=-ydistance
            totaldistance=xdistance+ydistance
            if totaldistance<lowestDistance:
                lowestDistance=totaldistance
                
        lowestDists.append(lowestDistance)
    
    totalLowestDists=0
    for dists in lowestDists:
        totalLowestDists=totalLowestDists+dists
    return totalLowestDists
        
        
    
    
 #   solpuzzle = search.astar_graph_search(puzzle, h)
    
  #  if(solpuzzle.goal_test()==True):
   #         return actionList

#solve_sokoban_elem(warehouse)
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def can_go_there(warehouse, dst):
    '''    
    Determine whether the worker can walk to the cell dst=(row,col) 
    without pushing any box.
    
    @param warehouse: a valid Warehouse object

    @return
      True if the worker can walk to cell dst=(row,col) without pushing any box
      False otherwise
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def solve_sokoban_macro(warehouse):
    '''    
    Solve using macro actions the puzzle defined in the warehouse passed as
    a parameter. A sequence of macro actions should be 
    represented by a list M of the form
            [ ((r1,c1), a1), ((r2,c2), a2), ..., ((rn,cn), an) ]
    For example M = [ ((3,4),'Left') , ((5,2),'Up'), ((12,4),'Down') ] 
    means that the worker first goes the box at row 3 and column 4 and pushes it left,
    then goes the box at row 5 and column 2 and pushes it up, and finally
    goes the box at row 12 and column 4 and pushes it down.
    
    @param warehouse: a valid Warehouse object

    @return
        If puzzle cannot be solved return ['Impossible']
        Otherwise return M a sequence of macro actions that solves the puzzle.
        If the puzzle is already in a goal state, simply return []
    '''
    
    ##         "INSERT YOUR CODE HERE"
    
    raise NotImplementedError()

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

wh = sokoban.Warehouse()
wh.read_warehouse_file("./warehouses/warehouse_01.txt")
#    field.write_warehouse_file("./F_01.txt")





