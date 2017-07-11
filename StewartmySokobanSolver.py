
'''

The partially defined functions and classes of this module 
will be called by a marker script. 

You should complete the functions and classes according to their specified interfaces.
 

'''

import search

import sokoban


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -


def my_team():
    '''
    Return the list of the team members of this assignment submission as a list
    of triplet of the form (student_number, first_name, last_name)
    '''
    return [(7521022, 'Jordan', 'Hawkes'),(7561555, 'Stewart','Whitehead')]
#    return [ (1234567, 'Ada', 'Lovelace'), (1234568, 'Grace', 'Hopper'), (1234569, 'Eva', 'Tardos') ]

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

#Function relies on rule 1 being implemented perfectly (corner that isn't target is taboo)
def foundOtherTabooCorner(cellx, celly, startCellX, startCellY, wallDirection, *taboos):    

        #Found another taboo corner, cells lining walls are all taboo
        if ( (cellx + wallDirection[0], celly + wallDirection[1]) in taboos):
            
            # For walls travelling horizonatally
            #if celly == startCellY:
            if wallDirection == (1, 0) or (-1, 0):
                for cellsTravelled in (abs (cellx - startCellX)):
                    if startCellX > cellx:
                        taboos.append((startCellX - cellsTravelled - 1))
                    elif startCellX < cellx:
                        taboos.append((startCellX + cellsTravelled + 1))
                        
            # For walls travelling vertically
            #if cellx == startCellX:
            if wallDirection == (0, 1) or (0, -1):
                for cellsTravelled in (abs (celly - startCellY)):
                    if startCellY > celly:
                        taboos.append((startCellY - cellsTravelled - 1))
                    elif startCellY < celly:
                        taboos.append((startCellY + cellsTravelled + 1))
                        


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
    for x,y in warehouse.walls:
        if (x-1,y+1) in warehouse.walls:
           if(((x,y+1) not in warehouse.targets) & ((x,y+1) not in warehouse.walls) & ((x,y+1) not in tabooCells)):
            tabooCells.append((x, y+1))
           if(((x-1,y) not in warehouse.targets) & ((x-1,y) not in warehouse.walls) & ((x-1,y) not in tabooCells)):
               tabooCells.append((x-1,y))
               
        elif (x+1,y+1) in warehouse.walls:
            if(((x+1,y) not in warehouse.targets) & ((x+1,y) not in warehouse.walls) & ((x+1,y) not in tabooCells)):
                tabooCells.append((x+1, y))
            if(((x,y+1) not in warehouse.targets) & ((x,y+1) not in warehouse.walls) & ((x,y+1) not in tabooCells)):
               tabooCells.append((x,y+1))
               
        elif (x+1,y-1) in warehouse.walls:
            if(((x,y-1) not in warehouse.targets) & ((x,y-1) not in warehouse.walls) & ((x,y-1) not in tabooCells)):
                tabooCells.append((x, y-1))
            if(((x+1,y) not in warehouse.targets) & ((x+1,y) not in warehouse.walls) & ((x+1,y) not in tabooCells)):
               tabooCells.append((x+1,y))
            
        elif (x-1,y-1) in warehouse.walls:
            if(((x,y-1) not in warehouse.targets) & ((x,y-1) not in warehouse.walls) & ((x,y-1) not in tabooCells)):
                tabooCells.append((x,y-1))
            if(((x-1,y) not in warehouse.targets) & ((x-1,y) not in warehouse.walls) & ((x-1,y) not in tabooCells)):
               tabooCells.append((x-1,y))
    
    
    originalTaboos =tabooCells;
    north = (0, -1)
    east = (1, 0)
    south = (0, 1)
    west = (-1, 0)
    
    for cells in originalTaboos:
 
        cellx = cells[0]
        celly = cells[1]
        startCellX = cellx
        startCellY = celly
        counter=0   
        cornerFound= False
        
        while (cornerFound == False):
            if (((cellx + 1, celly) not in warehouse.walls) & ((cellx + 1, celly) not in warehouse.targets) & ((cellx + 1, celly-1) in warehouse.walls)):
                cellx=cellx+1
                counter=counter+1
            elif (cellx + 1, celly-1) not in warehouse.walls:
                cornerFound=True
            elif(cellx +1, celly) in warehouse.targets:
                cornerFound=True
            elif (cellx +1,celly) in warehouse.walls:
                index = 0
                while index < counter:
                    tabooCells.append(startCellX+index, startCellY)
                    index += 1
                cornerFound=True
                
    for cells in originalTaboos:
 
        cellx = cells[0]
        celly = cells[1]
        startCellX = cellx
        startCellY = celly
        counter=0   
        cornerFound= False
        while (cornerFound == False):
            if (((cellx + 1, celly) not in warehouse.walls) & ((cellx + 1, celly) not in warehouse.targets) & ((cellx + 1, celly+1) in warehouse.walls)):
                cellx=cellx+1
                counter=counter+1
            elif (cellx + 1, celly+1) not in warehouse.walls:
                cornerFound=True
            elif(cellx +1, celly) in warehouse.targets:
                cornerFound=True
            elif (cellx +1,celly) in warehouse.walls:
                index = 0
                while index < counter:
                    tabooCells.append(startCellX+index, startCellY)
                    index += 1
                cornerFound=True
                
    for cells in originalTaboos:
        
        cellx = cells[0]
        celly = cells[1]
        startCellX = cellx
        startCellY = celly
        counter=0   
        cornerFound= False
        while (cornerFound == False):
            if (((cellx, celly+1) not in warehouse.walls) & ((cellx, celly+1) not in warehouse.targets) & ((cellx - 1, celly+1) in warehouse.walls)):
                celly=celly+1
                counter=counter+1
            elif (cellx - 1, celly+1) not in warehouse.walls:
                cornerFound=True
            elif(cellx, celly +1) in warehouse.targets:
                cornerFound=True
            elif (cellx,celly+1) in warehouse.walls:
                index = 0
                while index < counter:
                    tabooCells.append(startCellX, startCellY +index)
                    index += 1
                cornerFound=True           
            
        
    for cells in originalTaboos:
        
        cellx = cells[0]
        celly = cells[1]
        startCellX = cellx
        startCellY = celly
        counter=0   
        cornerFound= False
        while (cornerFound == False):
            if (((cellx, celly+1) not in warehouse.walls) & ((cellx, celly+1) not in warehouse.targets) & ((cellx + 1, celly+1) in warehouse.walls)):
                celly=celly+1
                counter=counter+1
            elif (cellx + 1, celly+1) not in warehouse.walls:
                cornerFound=True
            elif(cellx, celly +1) in warehouse.targets:
                cornerFound=True
            elif (cellx,celly+1) in warehouse.walls:
                index = 0
                while index < counter:
                    tabooCells.append(startCellX, startCellY +index)
                    index += 1
                cornerFound=True
    
    

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
        self.initial=warehouse
        self.initial.read_warehouse_file(self,warehouse)
        
        
        
        

    def actions(self, state):
        """
        Return the list of actions that can be executed in the given state 
        if these actions do not push a box in a taboo cell.
        The actions must belong to the list ['Left', 'Down', 'Right', 'Up']        
        """
        raise NotImplementedError

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
    
    raise NotImplementedError()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

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
    
    raise NotImplementedError()

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
wh.read_warehouse_file("./warehouses/warehouse_03.txt")
#    field.write_warehouse_file("./F_01.txt")





