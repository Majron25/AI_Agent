

class Map:
    def __init__(self, filename):
        self.grid = []
        self.start_pos = None
        self.goal_pos = []
        self.walls = []
        self.width = 1
        self.height = 1

        with open(filename, 'r') as f:
            # Read the grid dimensions from the first line
            [height, width] = map(int, f.readline()[1:-2].split(','))
            # Initialize the grid to contain only empty cells
            self.grid = [[' ' for j in range(width)] for i in range(height)]
            #print("This is the grid we are working on, visualy represented..kinda\n",self.grid)
            self.height = height
            self.width = width
            # Read the starting position of the robot from the second line
            [y, x] = map(int, f.readline()[1:-2].split(','))
            self.start_pos = (x, y)
            self.grid[x][y] = 'S'
            print("This is the starting position of our agent:", self.start_pos)
            # Read the goal positions from the third line
            print("The width and height of the grid:",width,height)
            goals = (f.readline()[1:-2]).replace("(","").replace(")","").strip().split('|')
            for g in goals:
              [x, y] = map(int, g.split(','))
              print(x,y,"|",width,height)
              if x >= 0 and x < self.width and y >= 0 and y < self.height:
                print("Goal state:[x]",x,"[y]",y)
                self.goal_pos.append((y, x)) #As we are working on reveres coordinates, we have to switch them to match correct coordinates
                self.grid[y][x] = 'G'
                #print("\nThis is the map with goal states:",self.grid)
              else:
                 print("The goal states seems to be out of the grid",x,y,"|",width,height)
            # Read the wall positions from the remaining lines y, y + h
            for line in f:
                [x, y, w, h] = map(int, line[1:-2].split(',')) #these values are for coordinates as well as width and height of the walls.
                for i in range(y, y + h): #to the value of y add the size of the wall
                    for j in range(x, x + w): #same to the value of x
                        self.grid[i][j] = '#'
                        self.walls.append((i, j))
            print("These are the coordinates of walls included within the grid:\n",self.walls)
        print("\nThis is the complete map:",self.grid)
class Move:
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    RIGHT = (1, 0)

    @staticmethod
    def get_move(from_pos, to_pos):
        dy = to_pos[0] - from_pos[0]
        dx = to_pos[1] - from_pos[1]
        if dx == 0:
            if dy == -1:
                return Move.UP
            elif dy == 1:
                return Move.DOWN
        elif dy == 0:
            if dx == -1:
                return Move.LEFT
            elif dx == 1:
                return Move.RIGHT
        return None

class Agent:
    def __init__(self, my_map):
        self.map = my_map
        self.moves = []
        print("Map width:", self.map.width)
        print("Map height:", self.map.height)
        #print(self.map.grid)
        self.move = Move

    def get_neighbors(self, pos):
        neighbors = []
        for i, j in [(0, 1), (-1, 0), (0, -1), (1, 0)]:
            neighbor = (pos[0] + i, pos[1] + j)
            if self.is_valid(neighbor) and neighbor not in neighbors:
                neighbors.append(neighbor)
                #self.map.grid[neighbor[0]][neighbor[1]] = "T" #This code shows where the agent is and what neighbours does it have
        #print(self.map.grid)
        return neighbors

    def is_valid(self, pos):
        if pos[0] < 0 or pos[0] >= self.map.height or pos[1] < 0 or pos[1] >= self.map.width:
            return False
        if self.map.grid[pos[0]][pos[1]] == '#':
            return False
        return True

      
    def bfs_search(self, start_pos, goal_pos):
        queue = [(start_pos, [])]
        visited = set()
        pos = start_pos
        print(pos)
        print(goal_pos[0],goal_pos[1])
        while queue:
          pos, moves = queue.pop(0)
          if pos == goal_pos[0] or pos == goal_pos[1]:
                print("Moves:", end=" ")
                for i in range(1, len(moves)):
                    move = self.move.get_move(moves[i - 1], moves[i])
                    if move == Move.UP:
                        print("up...,", end=" ")
                    elif move == Move.LEFT:
                        print("left...,", end=" ")
                    elif move == Move.DOWN:
                        print("down...,", end=" ")
                    elif move == Move.RIGHT:
                        print("right...,", end=" ")
                print()
                return moves
          visited.add(pos)
          #print("Visited",pos)
          for neighbor in self.get_neighbors(pos):
            if neighbor not in visited and neighbor not in self.map.walls:
                queue.append((neighbor, moves + [neighbor]))
        return None
    def dfs_search(self,start_pos,goal_pos):
        return None




class main():
    #Here we define which file to use to create our map.
    my_map = Map("RobotNav-test.txt") 
    #Create an Agent 
    agent = Agent(my_map)
    # Define a dictionary of search methods
    search_methods = {
    "BFS": agent.bfs_search,
    "DFS": agent.dfs_search,
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
      start_pos = my_map.start_pos
      goal_pos = my_map.goal_pos
      path = search_methods[search_method](start_pos, goal_pos)
      # Print the path
      print(f"\n{search_method} path: {path}")
