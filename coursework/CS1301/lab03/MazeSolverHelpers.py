from collections import deque
import math

class Cell:
    # Represents a single cell in the maze's grid
    def __init__(self, x, y):
        # Initializes a cell with its coordinates and default attributes
        self.coords = (x,y)
        self.neighbors = []
        self.visited = False
        self.cost = 0
        self.flooded = False

class Maze:
    # Manages the grid of Cells and handles maze-wide algorithms
    def __init__(self, nXCells, nYCells):
        # Initializes the maze grid with Cell objects
        self.grid = {}

        #create all cells in the grid
        for x in range(nXCells):
            for y in range(nYCells):
                self.grid[(x,y)] = Cell(x,y)

    def get_cell(self, coords):
        # Safely retrieves a cell object from the grid
        return self.grid.get(coords, None)

    def add_all_neighbors(self, nXCells, nYCells):
        # Initializes all potential neighbors for every cell
        for x in range(nXCells):
            for y in range(nYCells):
                cell = self.get_cell((x,y))
                if cell:
                    neighbors = []
                    #checking for all directions
                    potential = [
                        (x, y + 1),  # Up
                        (x, y - 1),  # Down
                        (x + 1, y),  # Right                      
                        (x - 1, y),  # Left                       
                    ]

                    for px, py in potential:
                        if 0 <= px < nXCells and 0 <= py < nYCells:
                            neighbors.append((px,py))
                    
                    neighbors.sort()
                    cell.neighbors = neighbors


    def update_neighbors(self, current_coords, navigable_neighbors):
        # Updates the neighbors for a cell based on wall detection
        current_cell = self.get_cell(current_coords)
        if not current_cell:
            return

        # set current neighbors to the navigable list
        current_cell.neighbors = navigable_neighbors[:]

        for coords, cell in self.grid.items():
            if coords == current_coords:
                continue
            
            if current_coords in cell.neighbors and coords not in navigable_neighbors:
                cell.neighbors.remove(current_coords)
            
            # If this cell should list current_coords but doesn't
            if coords in navigable_neighbors and current_coords not in cell.neighbors:
                cell.neighbors.append(current_coords)

    def update_costs(self, goal_coords):
        # Runs the flood-fill algorithm to update the cost for every cell
        for cell in self.grid.values():
            cell.flooded = False
            cell.cost = float('inf')

        goal_cell = self.get_cell(goal_coords)
        if not goal_cell: return

        queue = deque([goal_cell])
        goal_cell.cost = 0
        goal_cell.flooded = True

        while queue:
            current = queue.popleft()
            for neighbor_coords in current.neighbors:
                neighbor_cell = self.get_cell(neighbor_coords)
                if neighbor_cell and not neighbor_cell.flooded:
                    neighbor_cell.flooded = True
                    neighbor_cell.cost = current.cost + 1
                    queue.append(neighbor_cell)

    def get_next_cell(self, current_coords):
        # Determines the best neighboring cell to move to
        current_cell = self.get_cell(current_coords)
        if not current_cell or not current_cell.neighbors:
            return None
        
        unvisited = []
        for n in current_cell.neighbors:
            neighbor_cell = self.get_cell(n)
            if not neighbor_cell.visited:
                unvisited.append(n)
        
        if unvisited:
            # Choose unvisited neighbor with lowest cost
            best = min(unvisited, key=lambda n: self.get_cell(n).cost)
        else:
            # All visited, choose overall lowest cost
            best = min(current_cell.neighbors, key=lambda n: self.get_cell(n).cost)
        
        return best
    
# ==========================================================
# Helper Functions
    
def getRobotOrientation(heading):
    # Normalize heading to 0-360
    heading = heading % 360
    
    # Map to closest cardinal direction
    if 45 <= heading < 135:
        return "N"
    elif 135 <= heading < 225:
        return "W"
    elif 225 <= heading < 315:
        return "S"
    else:
        return "E"
    
def getPotentialNeighbors(currCell, orient):
    x, y = currCell
    
    if orient == "N":
        left = (x - 1, y)
        front = (x, y + 1)
        right = (x + 1, y)
        back = (x, y - 1)
    elif orient == "E":
        left = (x, y + 1)
        front = (x + 1, y)
        right = (x, y - 1)
        back = (x - 1, y)
    elif orient == "S":
        left = (x + 1, y)
        front = (x, y - 1)
        right = (x - 1, y)
        back = (x, y + 1)
    else:  # "W"
        left = (x, y - 1)
        front = (x - 1, y)
        right = (x, y + 1)
        back = (x + 1, y)
    
    return [left, front, right, back]

def getWallConfiguration(IR0, IR3, IR6, threshold):
    left_wall = IR0 > threshold
    front_wall = IR3 > threshold
    right_wall = IR6 > threshold
    
    return [left_wall, front_wall, right_wall]

def getNavigableNeighbors(wallsAroundCell, possibleNeighbors, prevCell, nXCells, nYCells):
    navigable = []
    left_wall, front_wall, right_wall = wallsAroundCell
    left, front, right, back = possibleNeighbors
    
    # Always allow going back to previous cell
    if prevCell is not None:
        navigable.append(prevCell)
    
    # Check each direction
    # Left
    if not left_wall and 0 <= left[0] < nXCells and 0 <= left[1] < nYCells:
        if left not in navigable:
            navigable.append(left)
    
    # Front
    if not front_wall and 0 <= front[0] < nXCells and 0 <= front[1] < nYCells:
        if front not in navigable:
            navigable.append(front)
    
    # Right
    if not right_wall and 0 <= right[0] < nXCells and 0 <= right[1] < nYCells:
        if right not in navigable:
            navigable.append(right)
    
    # # Back (always accessible if in bounds, for backtracking)
    # if 0 <= back[0] < nXCells and 0 <= back[1] < nYCells:
    #     if back not in navigable:
    #         navigable.append(back)
    
    return navigable


def checkCellArrived(currentCell, dest):
    return currentCell == dest
