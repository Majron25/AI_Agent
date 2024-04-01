class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.neighbours = []
        self.agent = False
        self.goal = False
        self.wall = False
        self.visited = False
    def __str__(self):
        return "X: ", self.x, "Y: ",self.y, "Agent: ",self.agent, "Goal: ", self.goal, "Wall: ", self.wall, "Visited: ", self.visited

class Map:
    def __init__(self, filename):
        self.grid = []
        self.start_pos = None
        self.goal_pos = []
        self.walls = []
        self.width = []
        self.height = []
        self.cells = []
        self.goals = []

        with open(filename, 'r') as f:
            # Read the grid dimensions from the first line
            [height,width] = map(int, f.readline()[1:-2].split(','))
            # Initialize the grid to contain only empty cells
            self.grid = [[' ' for j in range(width)] for i in range(height)]
            self.height = height
            self.width = width
            #Create cells
            for x in range(width):
                for y in range(height):
                    self.cells.append(Cell(x,y))
            # Read the starting position of the robot from the second line
            [x, y] = map(int, f.readline()[1:-2].split(','))
            for cell in self.cells:
                if x == cell.x and y == cell.y:
                    cell.agent = True
            self.start_pos = (x, y)
            # Read the goal positions from the third line
            goals = (f.readline()[1:-2]).replace("(","").replace(")","").strip().split('|')
            for g in goals:
                [x, y] = map(int, g.split(','))
                self.goals.append([x,y])
            for goal in self.goals:
                for cell in self.cells:
                    if cell.x == goal[0] and cell.y == goal[1]:
                        cell.goal = True
            # Read the wall positions from the remaining lines y, y + h
            for line in f:
                [x, y, w, h] = map(int, line[1:-2].split(',')) #these values are for coordinates as well as width and height of the walls.
                for i in range(y, y + h): #to the value of y add the size of the wall
                    for j in range(x, x + w): #same to the value of x
                        for cell in self.cells:
                            if j == cell.x and i == cell.y:
                                cell.wall = True
            cells = self.cells
            #UNCOMMENT FOR CELL CHECK
            # for cell in self.cells:
            #     print(cell.__str__())

class Algorithm:
    def __init__(self, my_map):
        self.map = my_map
    
    def manhattan(self, x1,y1,x2,y2):
        return abs(x1-x2) + abs(y1-y2) == 1

    def isValid(self, cell):
        if cell.x in range(0,self.map.width) and cell.y in range(0,self.map.height) and cell.wall is False:
            return True
        return False
    

    def get_neighbor(self,current):
        neihgbors = []
        for cell in self.map.cells:
            if cell.visited == False and self.isValid(cell):
                if cell.y == current.y - 1 and cell.x == current.x:
                    neihgbors.append(cell)
                if cell.x == current.x - 1 and cell.y == current.y:
                    neihgbors.append(cell)
                if cell.y == current.y + 1 and cell.x == current.x:
                    neihgbors.append(cell)
                if cell.x == current.x + 1 and cell.y == current.y:
                    neihgbors.append(cell)
        return neihgbors

    def dfs_search(self, current_cell,path = []):
        if current_cell.goal is True:
            return path + [current_cell]
        frontier = self.get_neighbor(current_cell)
        for cell in frontier:
            if cell.visited is False:
                cell.visited = True
                #print("CHECKING NOW: ", cell.__str__())
                c = self.dfs_search(cell, path + [cell])
                if c:
                    return c
        return None

class main():
    def path_print(search_method, path, current_cell):
        count = 0
        print("The Search used: ", search_method)
        print("Solution path:", )
        #get first move
        if path[0].x - 1 == current_cell.x:
            print("Start->RIGHT-->", end = '')
        elif path[0].x + 1 == current_cell.x:
            print("Start->LEFT-->", end = '')
        elif path[0].y + 1 == current_cell.y:
            print("Start->UP-->", end = '')
        elif path[0].y - 1 == current_cell.y:
            print("Start->DOWN-->", end = '')
        #get other moves
        for i in range(1,len(path)):
            if path[i].x - 1 == path[i-1].x:
                print("RIGHT-->", end = '')
            elif path[i].x + 1 == path[i-1].x:
                print("LEFT-->", end = '')
            elif path[i].y + 1 == path[i-1].y:
                print("UP-->", end = '')
            elif path[i].y - 1 == path[i-1].y:
                print("DOWN-->", end = '')
        print("Found Goal\nNumber of Nodes: ", len(path))

    #Here we define which file to use to create our map.
    my_map = Map("RobotNav-test.txt")
    #Create an Agent 
    algorithm = Algorithm(my_map)
    # Define a dictionary of search methods
    search_methods = {
        "DFS": algorithm.dfs_search,
    }

    # Run the DFS search every time the program is run
    #Get current cell
    current_cell = Cell
    for cell in my_map.cells:
        if cell.agent is True:
            current_cell = cell
            current_cell.visited = True
    path = search_methods["DFS"](current_cell)
    path_print("DFS", path, current_cell)