class Node:
    """Class to model a map grid node

    Attributes:
        row: Row number
        col: Column number
        x: Node x-coordinate (top left corner)
        y: Node y-coordinate (top left corner)
        cost: Node weight (or cost)
        neighbors; Node neighbours
        start: Node is start node
        goal: Node is goal node
        blocked: Ruutu on este
        visited: Node has been visited
        visited_jps: Path through node has been checked (JPS)
        previous: Previous node on route
        path: Node is on the calculated route
        costsum: Route cost (or time)
        heuristic: Node calculated heuristics
    """


    def __init__(self, row, col, gsize):
        """Class constructor to create a new node.

        Args:
            row: Row number
            col: Column number
            gsize: Grid node size in pixels
        """
        self.row = row
        self.col = col
        self.x = col * gsize
        self.y = row * gsize
        self.neighbors = []
        self.cost = 1
        self.start = False
        self.startmark = False
        self.goal = False
        self.goalmark = False
        self.blocked = False
        self.visited = False
        self.visited_jps = [0,0,0,0,0,0,0,0]
        self.previous = None
        self.path = False
        self.costsum = float("inf")
        self.heuristic = float("inf")


    def __lt__(self, other):
        return self.costsum + self.heuristic < other.costsum + other.heuristic


    def clear(self):
        """ Node reset
        """
        self.start = False
        self.goal = False
        self.blocked = False


    def get_pos(self):
        """ Node position

        Returns:
            row, col (Tuple): Node row and column
        """
        return self.row, self.col


    def mark_path(self):
        """ Route node
        """
        self.path = True


    def set_blocked(self):
        """ Obstacle node
        """
        self.blocked = True


    def set_goal(self):
        """ Goal node
        """
        self.goal = True
        self.blocked = False


    def set_start(self):
        """ Start node
        """
        self.start = True
        self.blocked = False


    def set_visited(self):
        """ Visited node
        """
        self.visited = True


    def set_visited_jps(self, dir):
        """ Record scanning direction (JPS)
        """
        if dir == (1,0):
            self.visited_jps[0] = 1
        elif dir == (1,1):
            self.visited_jps[1] = 1
        elif dir == (0,1):
            self.visited_jps[2] = 1
        elif dir == (-1,1):
            self.visited_jps[3] = 1
        elif dir == (-1,0):
            self.visited_jps[4] = 1
        elif dir == (-1,-1):
            self.visited_jps[5] = 1
        elif dir == (0,-1):
            self.visited_jps[6] = 1
        elif dir == (1,-1):
            self.visited_jps[7] = 1


    def check_visited_jps(self, dir):
        """ Check if route already examined (JPS)
        """
        if dir == (1,0):
            return self.visited_jps[0] == 1
        elif dir == (1,1):
            return self.visited_jps[1] == 1
        elif dir == (0,1):
            return self.visited_jps[2] == 1
        elif dir == (-1,1):
            return self.visited_jps[3] == 1
        elif dir == (-1,0):
            return self.visited_jps[4] == 1
        elif dir == (-1,-1):
            return self.visited_jps[5] == 1
        elif dir == (0,-1):
            return self.visited_jps[6] == 1
        elif dir == (1,-1):
            return self.visited_jps[7] == 1
