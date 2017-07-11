
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
                    
                    

def tabooAgainstWall(warehouse, taboo):
    
    #Direction to check (up, right, down, left)
    direction = [(0, -1), (1, 0), (0, 1), (-1, 0)]

    #make a copy of taboos before it is appended to
    originalTaboos = []    
    for cell in taboo:
        originalTaboos.append((cell))
    
    #for each cell in original taboos, set currentCell to point to it and do stuff
    for cell in originalTaboos:
        currentCell = cell
        
        #for each direction, choose a walldirection to navigate. Assign cell as cell to be checked and check if it's blank
        for step in direction:
            currentCell = cell
            checkCell = (currentCell[0] + step[0], currentCell[1] + step[1])
            
            #if we are stepping vertically, wall must be horizonatal to step, else vertical
            if step[0] == 0:
                wallDirection = [(1,0), (-1, 0)]
            else:
                wallDirection = [(0, -1), (0, 1)]
            
            #if checkCell is a wall or target, check next iteration
            if checkCell in (warehouse.walls + warehouse.targets):
                continue
            
            for offset in wallDirection:
                wallCell = (checkCell[0] + offset[0], checkCell[1] + offset[1])

                #if wallCell is not a wall, go to next iteration
                if wallCell not in warehouse.walls:
                    continue
                
                #reset the counter and run the rest of our checks
                counter = 0
                cornerFound = False
                
                while cornerFound == False:
#                    
                    #Cell we are checking is taboo cell found by corners
                    if checkCell in originalTaboos:
                        cornerFound = True
                        if counter > 0:
                            
                            i = 0
                            while i < counter:
                                if (cell[0] + step[0] - i, cell[1]) in taboo:
                                    i += 1
                                    continue
                                
                                if step in [(1, 0), (-1, 0)]:
                                    if currentCell[0] < cell[0]:
                                        taboo.append((cell[0] + step[0] - i, cell[1]))
                                        i += 1
                                    elif currentCell[0] > cell[0]:
                                        taboo.append((cell[0] + step[0] + i, cell[1]))
                                        i += 1
#                                
                                if step in [(0, 1), (0, -1)]:
                                    if currentCell[1] < cell[1]:
                                        taboo.append((cell[0], cell[1] + step[1] - i))
                                        i += 1
                                    elif currentCell[1] > cell[1]:
                                        taboo.append((cell[0], cell[1] + step[1] + i))
                                        i += 1
                            continue
                                
                            cornerFound = True
                        else:
                            cornerFound = True
#                            continue
                    #If cell we are checking is a wall, check next item
                    elif checkCell in warehouse.walls:
                        cornerFound = True
                        #continue
                    #If cell we are checking is a target, check next item
                    elif checkCell in warehouse.targets:
                        cornerFound = True
                        #continue
                    #If cell adjacent to checking cell is not a wall, check next item
                    elif wallCell not in warehouse.walls:
                        cornerFound = True
                        #continue
                    elif wallCell in warehouse.walls:
                        counter += 1
                        currentCell = checkCell
                        checkCell = (currentCell[0] + step[0], currentCell[1] + step[1])
                        wallCell = (wallCell[0] + step[0], wallCell[1] + step[1])
                    else:
                        raise AssertionError()

            

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
    return tabooCells
    

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


totalActions=[]


class SokobanPuzzle(search.Problem):
    '''
    Class to represent a Sokoban puzzle.
    Your implementation should be compatible with the
    search functions of the provided module 'search.py'.
    
    	Use the sliding puzzle and the pancake puzzle for inspiration!
    
    '''
    ##         "INSERT YOUR CODE HERE"

    
    def __init__(self, warehouse):
        print ("init called")
        problem_file = "./warehouses/warehouse_01.txt"
        self.initial=Warehouse();
        self.initial.read_warehouse_file(problem_file)
        self.taboos=taboo_cells(self.initial)
        self.worker=self.initial.worker
        self.walls=self.initial.walls
        self.boxes=self.initial.boxes
        self.targets=self.initial.targets
        print(self.taboos)
        
        self.nodeCount=0
    

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
                if (((x+xoff,y+yoff) not in state.walls) & ((x+xoff,y+yoff) not in state.boxes)):
                    executableActions.append((workerActions[move]))
                    
                    
                    
                elif (((x+xoff,y+yoff) not in state.walls) & ((x+xoff,y+yoff) in state.boxes)):
                    if (((x+xoff*2,y+yoff*2) not in self.taboos) & ((x+xoff*2,y+yoff*2) not in self.walls) & ((x+xoff*2,y+yoff*2) not in self.boxes)):
                        executableActions.append((workerActions[move]))
                        
                  
                
        return executableActions

    def goal_test(self, state):
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
        acceptableActions=self.actions(tempState)
        
        workerActions = ['Left', 'Right', 'Up', 'Down']   
        x,y=tempState.worker
        
        
        if(action in acceptableActions):
            if action == workerActions[0]:
                xoff,yoff=(-1,0)
            elif action == workerActions[1]:
                xoff,yoff=(1,0)
            elif action == workerActions[2]:
                xoff,yoff=(0,-1)
            elif action == workerActions[3]:
                xoff,yoff=(0,1)
                    
            if (((x+xoff,y+yoff) not in tempState.walls) & ((x+xoff,y+yoff) not in tempState.boxes)):
                
                tempState.worker=((x+xoff,y+yoff))
               
                    
            elif (((x+xoff,y+yoff) not in tempState.walls) & ((x+xoff,y+yoff) in tempState.boxes)):
                if (((x+xoff*2,y+yoff*2) not in self.taboos) & ((x+xoff*2,y+yoff*2) not in tempState.walls)):
                    tempState.boxes.remove((x+xoff,y+yoff))
                    tempState.boxes.append((x+xoff*2,y+yoff*2))
                    tempState.worker=((x+xoff,y+yoff))
                    
        print (state.worker)
        self.nodeCount +=1           
        return tempState
        
        
    def path_cost(self, c, state1, action, state2):
        """Return the cost of a solution path that arrives at state2 from
        state1 via action action, assuming cost c to get up to state1. If the problem
        is such that the path doesn't matter, this function will only look at
        state2.  If the path does matter, it will consider c and maybe state1
        and action. The default method costs 1 for every step in the path."""
        return c+1
        
    def print_node(self, node):
        """Print the action and resulting state"""
        if node.action:
            print ("Move "+node.action)
        self.print_state(node.state)
        
    
    def h(self, node):
    #
        hTotal = findClosestDistance(node.state.boxes, node.state.targets)
        if len(node.state.boxes) > 1:
  #     search for closed targets dist in reverse orders  
            total =  findClosestDistance(reversed(node.state.boxes), node.state.targets)
            if hTotal > total:
                # if we can find a lest cost path to the array this would be a more efficeint system then of a previous one
                hTotal = total
        workers = [node.state.worker]
        pTotal =  findClosestDistance(node.state.boxes, workers)
        hTotal = hTotal * 10 + pTotal
        return hTotal

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#N Heuristic
def findClosestDistance (boxes, targets):
    total = 0
    # Search for closed targets for boxes 
    matchedBoxes = []
    for target in targets:
        closestDist= 99
        closestBox = None
        if target in boxes:
            closestDist = 0
            closestBox = target
        else:
            for box in boxes:
                if box not in matchedBoxes:
                    dist = abs(target[0] - box[0]) + abs(target[1] - box[1])
                    #manhattan distance
                    if closestDist > dist:
                        #if the closest distance to another box is closer to the previous one change target
                        closestBox = box
                        closestDist = dist
                        
                        if dist == 0:
                            #means that the box is on the target
                            break
        total = total + closestDist
        #incrementing the closest total by the closest distance
        matchedBoxes.append(closestBox)
        
    return total 
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
                
                if ((x,y) in currentState.targets):
                    charImage[y][x] == "*" # if on target
                    
                else:
                    charImage[y][x] = "."
            if currentState.worker==((x,y)):
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
   
    sol_puzzle = search.astar_graph_search(puzzle)
    
  
    if sol_puzzle == None:
        return 'Impossible'

    
    return sol_puzzle.solution()

    
    
    #Jordans attempt at heuristic

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





