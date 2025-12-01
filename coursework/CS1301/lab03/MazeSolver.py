from irobot_edu_sdk.backend.bluetooth import Bluetooth
from irobot_edu_sdk.robots import event, hand_over, Color, Robot, Root, Create3
from irobot_edu_sdk.music import Note
from collections import deque
import math

# robot is the instance of the robot that will allow us to call its methods.
robot = Create3(Bluetooth("HRISTO-BOT"))

# === FLAG VARIABLES
HAS_COLLIDED = False
HAS_ARRIVED = False

# === MAZE CONSTANTS
N_X_CELLS = 3
N_Y_CELLS = 3
CELL_DIM = 45

# === ROBOT STATE VARIABLES
PREV_CELL = None
START = (0,0)
CURR_CELL = START
DESTINATION = (1,1)

# === PROXIMITY TOLERANCES
WALL_THRESHOLD = 80

# ==========================================================
# Object-Oriented Maze Representation

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
# FAIL SAFE MECHANISMS

@event(robot.when_touched, [True, True])
async def when_either_button_touched(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)


@event(robot.when_bumped, [True, True])
async def when_either_bumped(robot):
    global HAS_COLLIDED
    HAS_COLLIDED = True
    await robot.set_wheel_speeds(0, 0)
    await robot.set_lights_rgb(255, 0, 0)


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

    return navigable


def checkCellArrived(currentCell, dest):
    return currentCell == dest

# ==========================================================
# INITIALIZE MAZE OBJECT

# Create an instance of the Maze class
maze = Maze(N_X_CELLS, N_Y_CELLS)

# Mark the starting cell as visited within the maze object
maze.get_cell(CURR_CELL).visited = True

# ==========================================================
# EXPLORATION AND NAVIGATION

async def navigateToNextCell(robot, nextCell, orient):
    global maze, PREV_CELL, CURR_CELL, CELL_DIM
    
    # Calculate direction to turn
    dx = nextCell[0] - CURR_CELL[0]
    dy = nextCell[1] - CURR_CELL[1]
    
    # Determine target direction
    if dx == 1:
        target_dir = "E"
    elif dx == -1:
        target_dir = "W"
    elif dy == 1:
        target_dir = "N"
    elif dy == -1:
        target_dir = "S"
    else:
        return  # No movement needed
    
    # Calculate turn needed
    directions = ["N", "E", "S", "W"]
    current_idx = directions.index(orient)
    target_idx = directions.index(target_dir)
    turn_diff = (target_idx - current_idx) % 4
    
    # Execute turn
    if turn_diff == 1:  # Turn right
        await robot.turn_right(90)
    elif turn_diff == 2:  # Turn around
        await robot.turn_right(180)
    elif turn_diff == 3:  # Turn left
        await robot.turn_left(90)
    # If turn_diff == 0, no turn needed

    # Move forward one cell
    start_pos = await robot.get_position()
    start_x = start_pos.x
    start_y = start_pos.y

    await robot.set_wheel_speeds(15, 15)

    while not HAS_COLLIDED:
        current_pos = await robot.get_position()
        distance_traveled = math.sqrt(
            (current_pos.x - start_x)**2 + 
            (current_pos.y - start_y)**2
        )

        if distance_traveled >= CELL_DIM:
            await robot.set_wheel_speeds(0, 0)
            break

        await robot.wait(0.1)

    if HAS_COLLIDED:
        return
    
    # Update state
    PREV_CELL = CURR_CELL
    CURR_CELL = nextCell
    maze.get_cell(nextCell).visited = True
    
    # Visual debugging
    if target_dir == "N":
        await robot.set_lights_rgb(0, 0, 255)  # Blue = North
    elif target_dir == "E":
        await robot.set_lights_rgb(255, 255, 0)  # Yellow = East
    elif target_dir == "S":
        await robot.set_lights_rgb(255, 0, 255)  # Magenta = South
    elif target_dir == "W":
        await robot.set_lights_rgb(0, 255, 255)  # Cyan = West
    

@event(robot.when_play)
async def navigateMaze(robot):
    global HAS_COLLIDED, HAS_ARRIVED
    global PREV_CELL, CURR_CELL, START, DESTINATION
    global maze, N_X_CELLS, N_Y_CELLS, CELL_DIM, WALL_THRESHOLD
    
    # The main loop will now call methods on the 'maze' object
    # Initialize
    CURR_CELL = START
    maze.get_cell(CURR_CELL).visited = True
    await robot.set_wheel_speeds(10, 10)
    await robot.set_lights_rgb(0, 255, 0)
    
    # Main navigation loop
    while not HAS_ARRIVED and not HAS_COLLIDED:
        # Read sensors
        sensors = (await robot.get_ir_proximity()).sensors
        IR0 = sensors[0]
        IR3 = sensors[3]
        IR6 = sensors[6]
        
        # Get robot position and heading
        position = await robot.get_position()
        heading = position.heading
        
        # Get orientation
        orientation = getRobotOrientation(heading)
        
        # Get wall configuration
        walls = getWallConfiguration(IR0, IR3, IR6, WALL_THRESHOLD)

        # Audio debugging
        wall_count = sum(walls)  # Count how many walls detected
        if wall_count == 1:
            await robot.play_note(Note.C4, 0.1)  # One beep for 1 wall
        elif wall_count == 2:
            await robot.play_note(Note.C4, 0.1)  # Two beeps for 2 walls
            await robot.play_note(Note.C4, 0.1)  
        elif wall_count == 3:
            await robot.play_note(Note.C4, 0.1)  # 3 beeps for 3 walls
            await robot.play_note(Note.C4, 0.1)
            await robot.play_note(Note.C4, 0.1)  
        
        # Get potential neighbors based on orientation
        potential = getPotentialNeighbors(CURR_CELL, orientation)
        
        # Filter to navigable neighbors
        navigable = getNavigableNeighbors(walls, potential, PREV_CELL, N_X_CELLS, N_Y_CELLS)
        
        # Update maze structure
        maze.update_neighbors(CURR_CELL, navigable)
        maze.update_costs(DESTINATION)
        
        # Choose next cell
        next_cell = maze.get_next_cell(CURR_CELL)
        
        if next_cell is None:
            # Dead end
            await robot.set_lights_rgb(255, 0, 0)
            break
        
        # Move to next cell
        await navigateToNextCell(robot, next_cell, orientation)
        
        # Check if arrived
        if checkCellArrived(CURR_CELL, DESTINATION):
            HAS_ARRIVED = True
            await robot.set_lights_spin_rgb(0, 255, 0)
            await robot.turn_right(360)
            await robot.play_note(Note.C5, 0.3)
            await robot.play_note(Note.E5, 0.3)
            await robot.play_note(Note.G5, 0.3)
            await robot.play_note(Note.C6, 0.6)
            break
    
    # Stop robot
    await robot.set_wheel_speeds(0, 0)

robot.play()
