from filecmp import cmp
import sys 

class Node():
    def __init__(self , state , parent , action) :
        self.state = state
        self.parent = parent
        self.action = action
class GreedyNode(Node):
    def __init__(self , state , parent , action , cost) :
        super().__init__(state , parent , action)
        self.cost = cost
    def __lt__(self, other):
        return self.cost < other.cost
class StackFrontier():
    def __init__(self) :
        self.frontier = []
    def add(self,node):
        self.frontier.append(node)
    def contains_state(self ,state):
        return any(node.state == state for node in self.frontier)
    def empty(self):
        return len(self.frontier ) == 0
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else :
            #in stack frontier we remove the last node
            #we can use it for depth first search
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node
#let's create a queue frontier, inherit from stack frontier
#we can use it for breadth first search
class QueueFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else :
            #in queue frontier we remove the first node
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node
#let's create a greedy frontier, inherit from stack frontier
#we can use it for greedy best first search
class GreedyFrontier(StackFrontier):
    def remove(self):
        if self.empty():
            raise Exception("Empty frontier")
        else :
            #in greedy frontier we remove the minimum node
            node = min(self.frontier)
            self.frontier.remove(node)
            return node

#let's create a maze class
#it will read the maze from a file, # is walls, A is start, B is goal and space is the path
class Maze():
    def __init__(self,filename):
        with open(filename) as f:
            contents = f.read()
        #validate start and goal
        if contents.count("A") != 1:
            raise Exception("maze must have exactly one start point but it has {}".format(contents.count("A")))
        if contents.count("B") != 1:
            raise Exception("maze must have exactly one goal but it has {}".format(contents.count("B")))
        #Determine height and width of maze
        #splitlines() method splits the string at line breaks and returns a list of lines in the string
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)
        
        #Keep track of walls
        self.walls = [] #list of walls
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    if contents[i][j] == "A":
                        self.start = (i,j) #Set the start position
                        row.append(False)
                    elif contents[i][j] == "B":
                        self.goal = (i,j) #Set the goal position
                        row.append(False)
                    elif contents[i][j] == " ":
                        row.append(False)
                    else :
                        #if it is not A,B or space, it is a wall so append True
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        #initialization of the solution as None
        self.solution = None
    
    #print the maze
    
    def print(self):
        
        solution = self.solution[1] if self.solution is not None else None
        print()
        #for learn the enumerate function, you can take a look to the comment lines below
        #summary : enumerate function returns a tuple containing a count (from start which defaults to 0) and the values obtained from iterating over sequence
        #for i,row in enumerate(self.walls):
        #    print(i,row)
        for i,row in enumerate(self.walls):
            for j,col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.start:
                    print("A", end="")
                elif (i, j) == self.goal:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    def neighbors(self, state):
        row,col = state
        candidates = [
            ("up", (row - 1, col)),
            ("down", (row + 1, col)),
            ("left", (row, col - 1)),
            ("right", (row, col + 1))
        ]
        result = []
        for action, (r,c) in candidates:
            if 0 <= r < self.height and 0 <= c < self.width and not self.walls[r][c]:
                result.append((action,(r,c)))
        return result
    def solve_greedy(self):
        """Finds a solution to maze, if one exists."""
        
        #Keep track of number of states explored
        self.num_explored = 0 #initialization
        
        #Initialize frontier to just the starting position
        start = GreedyNode(state = self.start , parent = None , action = None,cost = abs((self.goal[0] - self.start[0]))+abs((self.goal[1] - self.start[1])))
        #frontier = StackFrontier() #we will use stack frontier for depth first search
        frontier = GreedyFrontier()
        frontier.add(start)
        
        #Initialize an empty explored set
        self.explored = set()
        
        #Keep looping until solution found
        while True:
            
            #If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            #Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            
            #If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                
                #Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                    
                #Reverse the lists to get the solution
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            
            #Mark node as explored
            self.explored.add(node.state)
            
            #Add neighbors to frontier
            for action,state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    #child = Node(state = state , parent = node , action = action)
                    child = GreedyNode(state = state , parent = node , action = action , cost = abs((self.goal[0] - state[0]))+abs((self.goal[1] - state[1])))
                    frontier.add(child)
        
        
    def solve(self):
        """Finds a solution to maze, if one exists."""
        
        #Keep track of number of states explored
        self.num_explored = 0 #initialization
        
        #Initialize frontier to just the starting position
        start = Node(state = self.start , parent = None , action = None)
        #frontier = StackFrontier() #we will use stack frontier for depth first search
        frontier = QueueFrontier()
        frontier.add(start)
        
        #Initialize an empty explored set
        self.explored = set()
        
        #Keep looping until solution found
        while True:
            
            #If nothing left in frontier, then no path
            if frontier.empty():
                raise Exception("no solution")
            
            #Choose a node from the frontier
            node = frontier.remove()
            self.num_explored += 1
            
            #If node is the goal, then we have a solution
            if node.state == self.goal:
                actions = []
                cells = []
                
                #Follow parent nodes to find solution
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                    
                #Reverse the lists to get the solution
                actions.reverse()
                cells.reverse()
                self.solution = (actions,cells)
                return
            
            #Mark node as explored
            self.explored.add(node.state)
            
            #Add neighbors to frontier
            for action,state in self.neighbors(node.state):
                if not frontier.contains_state(state) and state not in self.explored:
                    child = Node(state = state , parent = node , action = action)
                    frontier.add(child)
        
    def output_image(self, filename, show_solution=True, show_explored=False):
        from PIL import Image, ImageDraw
        cell_size = 50
        cell_border = 2

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.width * cell_size, self.height * cell_size),
            "black"
        )
        draw = ImageDraw.Draw(img)

        solution = self.solution[1] if self.solution is not None else None
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):

                # Walls
                if col:
                    fill = (40, 40, 40)#it fills the wall with gray color

                # Start
                elif (i, j) == self.start:
                    fill = (255, 0, 0)#it fills the start position with red color

                # Goal
                elif (i, j) == self.goal:
                    fill = (0, 171, 28)#it fills the goal position with green color

                # Solution
                elif solution is not None and show_solution and (i, j) in solution:
                    fill = (220, 235, 113)#it fills the solution path with yellow color

                # Explored
                elif solution is not None and show_explored and (i, j) in self.explored:
                    fill = (212, 97, 85)#it fills the explored path with red color

                # Empty cell
                else:
                    fill = (237, 240, 252)#it fills the empty cells with white color

                # Draw cell
                draw.rectangle(
                    ([(j * cell_size + cell_border, i * cell_size + cell_border),
                      ((j + 1) * cell_size - cell_border, (i + 1) * cell_size - cell_border)]),
                    fill=fill
                )

        img.save(filename)


if len(sys.argv) != 2:
    sys.exit("Usage: python3 mazef.py maze.txt")

m = Maze(sys.argv[1])
print("Maze:")
m.print()
print("Solving...")
m.solve_greedy()
print("States Explored:", m.num_explored)
print("Solution:")
m.print()
m.output_image("maze"+ sys.argv[1].replace("maze","").replace(".txt","")+".png", show_explored=True)

     