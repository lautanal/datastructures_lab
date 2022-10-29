import random
from math import sqrt
from node import Node


class Map:
    """Luokka, joka mallintaa karttaruudukon

    Attributes:
        nrows: Rivien lukumäärä
        ncols: Sarakkeiden lukumäärä
        gsize: Karttaruudun koko pikseleinä
        nodes: Karttaruudut taulukkona
        start: Lähtöruutu
        goal: Maaliruutu
    """

    def __init__(self, nrows, ncols, gsize):
        """Luokan konstruktori, joka luo uuden karttaruudukon.

        Args:
            nrows: Rivien lukumäärä
            ncols: Sarakkeiden lukumäärä
            gsize: Karttaruudun koko pikseleinä
        """
        self.nrows = nrows
        self.ncols = ncols
        self.gsize = gsize
        self.nodes = []
        self.start = None
        self.goal = None
        self.weighted = True
        self.make()


    def make(self):
        """ Solmujen luonti
        """
        for i in range(self.nrows):
            self.nodes.append([])
            for j in range(self.ncols):
                node = Node(i, j, self.gsize)
                self.nodes[i].append(node)


    def generate_costs(self):
        """ Kartan random-generointi (solmujen painot)
        """
        self.weighted = True
        costmap = [[random.randrange(1, 10, 1) for _ in range(self.ncols)] for _ in range(self.nrows)]
        for row in self.nodes:
            for node in row:
                node.cost = costmap[node.row][node.col]


    def generate_obstacles(self):
        """ Kartan random-generointi (esteiden paikat)
        """
        self.weighted = False
        costmap = [[random.randrange(1, 6, 1) for _ in range(self.ncols)] for _ in range(self.nrows)]
        for row in self.nodes:
            for node in row:
                if costmap[node.row][node.col] == 5:
                    node.blocked = True


    def on_map(self, row, col):
        """ Tarkastetaan, onko ruutu kartalla
        """
        return row >= 0 and row < self.nrows and col >= 0 and col < self.ncols


    def set_costs(self, maparray):
        """ Kartan solmujen painoarvot (kartta luettu tiedostosta)
        """
        self.weighted = False
        for row in self.nodes:
            for node in row:
                if maparray[node.row][node.col] == 'B' or maparray[node.row][node.col] == '@':
                    node.cost = 1
                    node.set_blocked()
                elif maparray[node.row][node.col] == '.' or maparray[node.row][node.col] == '1':
                    node.cost = 1
                else:
                    self.weighted = True
                    try:
                        node.cost = int(maparray[node.row][node.col])
                    except:
                        node.cost = 1
                        node.set_blocked()


    def set_start(self, start):
        """ Lähtöpiste
        """
        # Isompi starttimerkki
        if self.gsize < 10:
            if start:
                if self.on_map(start.row-1, start.col): 
                    self.nodes[start.row-1][start.col].startmark = True        
                if self.on_map(start.row+1, start.col): 
                    self.nodes[start.row+1][start.col].startmark = True        
                if self.on_map(start.row, start.col-1): 
                    self.nodes[start.row][start.col-1].startmark = True        
                if self.on_map(start.row, start.col+1): 
                    self.nodes[start.row][start.col+1].startmark = True
            else:        
                if self.on_map(self.start.row-1, self.start.col): 
                    self.nodes[self.start.row-1][self.start.col].startmark = False        
                if self.on_map(self.start.row+1, self.start.col): 
                    self.nodes[self.start.row+1][self.start.col].startmark = False        
                if self.on_map(self.start.row, self.start.col-1): 
                    self.nodes[self.start.row][self.start.col-1].startmark = False        
                if self.on_map(self.start.row, self.start.col+1): 
                    self.nodes[self.start.row][self.start.col+1].startmark = False

        # Uusi lähtöpiste
        self.start = start


    def set_goal(self, goal):
        """ Maalipiste
        """
        # Suurempi maalimerkki
        if self.gsize < 10:
            if goal:
                if self.on_map(goal.row-1, goal.col): 
                    self.nodes[goal.row-1][goal.col].goalmark = True        
                if self.on_map(goal.row+1, goal.col): 
                    self.nodes[goal.row+1][goal.col].goalmark = True        
                if self.on_map(goal.row, goal.col-1): 
                    self.nodes[goal.row][goal.col-1].goalmark = True        
                if self.on_map(goal.row, goal.col+1): 
                    self.nodes[goal.row][goal.col+1].goalmark = True
            else:        
                if self.on_map(self.goal.row-1, self.goal.col): 
                    self.nodes[self.goal.row-1][self.goal.col].goalmark = False        
                if self.on_map(self.goal.row+1, self.goal.col): 
                    self.nodes[self.goal.row+1][self.goal.col].goalmark = False        
                if self.on_map(self.goal.row, self.goal.col-1): 
                    self.nodes[self.goal.row][self.goal.col-1].goalmark = False        
                if self.on_map(self.goal.row, self.goal.col+1): 
                    self.nodes[self.goal.row][self.goal.col+1].goalmark = False
                    
        # Uusi maalipiste
        self.goal = goal


    def neighbors_xy(self):
        """ Solmujen naapurit, xy-polku
        """
        for row in self.nodes:
            for node in row:
                node.costsum = float("inf")

                node.neighbors = []
                if node.row < self.nrows - 1 and not self.nodes[node.row + 1][node.col].blocked:
                    node.neighbors.append(self.nodes[node.row + 1][node.col])

                if node.row > 0 and not self.nodes[node.row - 1][node.col].blocked:
                    node.neighbors.append(self.nodes[node.row - 1][node.col])

                if node.col < self.ncols - 1 and not self.nodes[node.row][node.col + 1].blocked:
                    node.neighbors.append(self.nodes[node.row][node.col + 1])

                if node.col > 0 and not self.nodes[node.row][node.col - 1].blocked:
                    node.neighbors.append(self.nodes[node.row][node.col - 1])


    def neighbors_diag(self):
        """ Solmujen naapurit, viisto polku
        """
        for row in self.nodes:
            for node in row:
                node.costsum = float("inf")

                node.neighbors = []
                if node.row < self.nrows - 1:
                    if not self.nodes[node.row + 1][node.col].blocked:
                        node.neighbors.append(self.nodes[node.row + 1][node.col])
                    if node.col < self.ncols - 1 and not self.nodes[node.row + 1][node.col + 1].blocked:
                        node.neighbors.append(self.nodes[node.row + 1][node.col + 1])
                    if node.col > 0 and not self.nodes[node.row + 1][node.col - 1].blocked:
                        node.neighbors.append(self.nodes[node.row + 1][node.col - 1])

                if node.row > 0:
                    if not self.nodes[node.row - 1][node.col].blocked:
                        node.neighbors.append(self.nodes[node.row - 1][node.col])
                    if node.col < self.ncols - 1 and not self.nodes[node.row - 1][node.col + 1].blocked:
                        node.neighbors.append(self.nodes[node.row - 1][node.col + 1])
                    if node.col > 0 and not self.nodes[node.row - 1][node.col - 1].blocked:
                        node.neighbors.append(self.nodes[node.row - 1][node.col - 1])

                if node.col < self.ncols - 1 and not self.nodes[node.row][node.col + 1].blocked:
                    node.neighbors.append(self.nodes[node.row][node.col + 1])

                if node.col > 0 and not self.nodes[node.row][node.col - 1].blocked:
                    node.neighbors.append(self.nodes[node.row][node.col - 1])


    def heuristic_manhattan(self, goal):
        """ Manhattan heuristiikka
        """
        for row in self.nodes:
            for node in row:
                y1, x1 = node.get_pos()
                y2, x2 = goal.get_pos()
                node.heuristic = abs(x1 - x2) + abs(y1 - y2)


    def heuristic_euclidian(self, goal):
        """ Eukliidinen heuristiikka
        """
        for row in self.nodes:
            for node in row:
                y1, x1 = node.get_pos()
                y2, x2 = goal.get_pos()
                node.heuristic = sqrt((x1 - x2)**2 + (y1 - y2)**2)


    def heuristic_chebyshev(self, goal):
        """ Chebyshev heuristiikka
        """
        for row in self.nodes:
            for node in row:
                y1, x1 = node.get_pos()
                y2, x2 = goal.get_pos()
                node.heuristic = max(abs(x1 - x2), abs(y1 - y2))


    def track_path(self, diagonal):
        """ Polun track
        """
        node = self.goal.previous
        count = 0
        while node != self.start:
            count += 1
            node.mark_path()
            node = node.previous
        costsum = self.goal.costsum
        if not diagonal:
            costsum = self.goal.costsum - self.goal.cost
        return count, costsum


    def track_path_jps(self, path):
        """ Polun track JPS
        """
        for i in range(len(path)-1):
            node0 = path[i]
            col0 = node0.col
            row0 = node0.row
            node1 = path[i+1]
            col1 = node1.col
            row1 = node1.row
            if col0 == col1:
                nn = abs(row1 - row0)
            else:
                nn = abs(col1 - col0)
            ic = (col1 - col0) // nn
            ir = (row1 - row0) // nn
            col = col0
            row = row0
            while col != col1 or row != row1:
                node = self.nodes[row][col]
                if node != self.start:
                    node.mark_path()
                col += ic
                row += ir


    def reset(self):
        """Karttaruudukon reset
        """
        for row in self.nodes:
            for node in row:
                node.visited = False
                node.visited_jps = [0,0,0,0,0,0,0,0]
                node.path = False
