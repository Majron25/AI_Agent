
# class Node:
#     def __init__(self, cell, parent=None):
#         self.cell = cell
#         self.parent = parent
#         self.children = []
#         if parent is not None:
#             self.parent.children.append(self)

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
            #print("This is the grid we are working on, visualy represented..kinda\n",self.grid)
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

    def get_path(self, goal):
        if self.agent is None:
            for cell in self.map.cells:
                if cell.agent:
                    self.agent = Node(cell)
                    break
        frontier = [self.agent]
        visited = []

        while frontier:
            node = frontier.pop(0)
            visited.append(node)
            cell = node.cell
            if cell.goal:
                path = []
                while node.parent is not None:
                    path.append(node.cell)
                    node = node.parent
                path.append(self.agent.cell)
                path.reverse()
                return path
            for neighbor in self.get_neighbors(cell):
                if not neighbor.visited:
                    neighbor_node = Node(neighbor, node)
                    frontier.append(neighbor_node)
        return None

    def get_neighbors(self, agent):
        neightbors = []
        for cell in self.map.cells:
            if self.manhattan(agent.x, agent.y, cell.x, cell.y) and cell.visited == False and cell.wall == False:
                neightbors.append(cell)
        return neightbors
    
    def manhattan(self, x1,y1,x2,y2):
        return abs(x1-x2) + abs(y1-y2) == 1
    
    def isValid(self, cell):
        if cell.x in range(0,self.map.width) and cell.y in range(0,self.map.height) and cell.wall is False and cell.visited is False:
            return True
        return False

    def bfs_search(self,path = []):
        self.agent = False
        for cell in self.map.cells:
            if cell.agent == True:
                self.agent = cell
                self.agent.visited = True
        frontier = []
        firstel = []
        visited = []        
        self.start = self.agent
        parent_nodes = dict()
        parent_nodes[self.agent]= None
        frontier.append(self.agent)
        frontier = frontier + self.get_neighbors(self.agent)
        i = 0
        for n in frontier:
            print(i," Frontier For Agent: ",n.__str__())
        print("Self Agent Starting Position: ", self.agent.__str__())
        index = 20
        while frontier :#and index > 0:
            # for n in frontier:
            #     print("Frontier: ",n.__str__())
            # print("Self agent now: ", self.agent.__str__())
            for i in range(5):
                if i == 0: #Go Up
                    #print("Trying to go UP")
                    for cell in self.map.cells: 
                        if self.isValid(cell):
                            if cell.x == self.agent.x and cell.y == self.agent.y -1:
                                cell.visited = True
                                visited.append(cell)
                                self.agent.visited = True
                                if self.get_neighbors(cell) not in frontier:
                                    frontier = frontier + self.get_neighbors(cell)
                                    for neighbor in self.get_neighbors(cell):
                                        parent_nodes[neighbor] = cell
                                # for n in frontier:
                                #     print("Frontier: ",n.__str__())
                                # print("Self agent now: ", self.agent.__str__())
                                # print("Up-->", end= '')
                                break
                                    
                if i == 1: #Go Left
                    #print("Trying to go Left")
                    for cell in self.map.cells:
                        if self.isValid(cell):
                            if cell.y == self.agent.y and cell.x == self.agent.x - 1:
                                cell.visited = True
                                visited.append(cell)
                                self.agent.visited = True
                                if self.get_neighbors(cell) not in frontier:
                                    frontier = frontier + self.get_neighbors(cell)
                                    for neighbor in self.get_neighbors(cell):
                                        parent_nodes[neighbor] = cell
                                # for n in frontier:
                                #     print("Frontier: ",n.__str__())
                                # print("Self agent now: ", self.agent.__str__())
                                # print("Left-->",end= '')
                                break

                if i == 2: #Go Down
                    #print("Trying to go Down")
                    for cell in self.map.cells:
                        if self.isValid(cell):
                            if cell.x == self.agent.x and cell.y == self.agent.y + 1:
                                cell.visited = True
                                visited.append(cell)
                                self.agent.visited = True
                                if self.get_neighbors(cell) not in frontier:
                                    frontier = frontier + self.get_neighbors(cell)
                                    for neighbor in self.get_neighbors(cell):
                                        parent_nodes[neighbor] = cell
                                # for n in frontier:
                                #     print("Frontier: ",n.__str__())
                                # print("Self agent now: ", self.agent.__str__())
                                # print("Down-->", end= '')
                                break

                if i == 3: #Go Right
                    #print("Trying to go Right")
                    for cell in self.map.cells:
                        if self.isValid(cell):
                            if cell.y == self.agent.y and cell.x == self.agent.x + 1:
                                cell.visited = True
                                visited.append(cell)
                                self.agent.visited = True
                                if self.get_neighbors(cell) not in frontier:
                                    frontier = frontier + self.get_neighbors(cell)
                                    for neighbor in self.get_neighbors(cell):
                                        parent_nodes[neighbor] = cell
                                # for n in frontier:
                                #     print("Frontier: ",n.__str__())
                                # print("Self agent now: ", self.agent.__str__())
                                #print("Right-->", end= '')
                                break
                if self.agent.goal == True:
                    print("Found goal: [x]",self.agent.x,"[y]",self.agent.y)
                    path = []
                    parent = parent_nodes[self.agent]
                    while parent in parent_nodes:
                        path.append(parent)
                        parent = parent_nodes[parent]
                        print(parent.__str__())
                    path.append(parent) #add the first move of the agent
                    path.reverse()
                    print("The path in reverse:")
                    for a in path:
                        print(a.__str__())
                    return path + [self.agent]
                if i == 4:
                    firstel = frontier[0]
                    self.agent.agent = False
                    self.agent = firstel
                    self.agent.agent = True
                    visited.append(firstel)
                    #print("\tAgent on New Frontier[X]:",self.agent.x,"[Y]:",self.agent.y)
                    frontier.pop(0)
        return "The path could not be found"
    
    def dfs_search(self):
        return False




class main():
    #Here we define which file to use to create our map.
    my_map = Map("RobotNav-test.txt")
    #Create an Agent 
    algorithm = Algorithm(my_map)
    # Define a dictionary of search methods
    search_methods = {
    "BFS": algorithm.bfs_search,
    "DFS": algorithm.dfs_search,
    #"Astar": agent.astar_search
    }
    while True:
    # Print search options
      print("\nSearch Options:")
      print("1. BFS")
      print("2. DFS")
      print("3. A*")
      print("0. Exit")

    # Get user input for search method
      choice = input("\nEnter the number of the search method you would like to try: ")

    # Check if user wants to exit
      if choice == "0":
        break
    # Check if user input is valid
      if choice not in ["1", "2", "3","4"]: #add more at the end of assigment
        print("\nInvalid input. Please try again or insert the correct number.")
        continue
      # Get the search method based on user input
      search_method = list(search_methods.keys())[int(choice) - 1]
      # Run the search method
      # Print the path
      if search_method == "BFS":
        #Get current cell
        current_cell = Cell
        for cell in my_map.cells:
            if cell.agent is True:
                current_cell = cell
                current_cell.visited = True
        path = search_methods[search_method](current_cell)
        print("Solution path:")
        #get first move
        if path[0].x - 1 == current_cell.x:
            print("Start:RIGHT-->", end = '')
        elif path[0].x + 1 == current_cell.x:
            print("Start:LEFT-->", end = '')
        elif path[0].y + 1 == current_cell.y:
            print("Start:UP-->", end = '')
        elif path[0].y - 1 == current_cell.y:
            print("Start:DOWN-->", end = '')
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
        print("Found Goal")
