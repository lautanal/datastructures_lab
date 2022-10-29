class Node:
    """Luokka, joka mallintaa karttaruudun

    Attributes:
        row: Rivinumero
        col: Sarakenumero
        x: Ruudun x-koordinaatti (vasen ylänurkka)
        y: Ruudun y-koordinaatti (vasen ylänurkka)
        cost: Ruudun painoarvo
        neighbors; Ruudun naapuriruudut
        start: Ruutu on lähtöruutu
        goal: Ruutu on maaliruutu
        blocked: Ruutu on este
        visited: Ruudussa on vierailtu
        visited_jps: Ruudun kautta kulkeva reitti on tutkittu (JPS)
        previous: Edellinen ruutu reitillä
        path: Ruutu on lasketulla polulla
        costsum: Reitin hinta (tai aika)
        heuristic: Ruudulle laskettu heuristiikka
    """


    def __init__(self, row, col, gsize):
        """Luokan konstruktori, joka luo uuden karttaruudun.

        Args:
            row: Rivinumero
            col: Sarakenumero
            gsize: Karttaruudun koko pikseleinä
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
        """ Ruudun reset
        """
        self.start = False
        self.goal = False
        self.blocked = False


    def get_pos(self):
        """ Ruudun paikka

        Returns:
            row, col (Tuple): Ruudun rivi ja sarake
        """
        return self.row, self.col


    def mark_path(self):
        """ Reittiruutu
        """
        self.path = True


    def set_blocked(self):
        """ Esteruutu
        """
        self.blocked = True


    def set_goal(self):
        """ Maaliruutu
        """
        self.goal = True
        self.blocked = False


    def set_start(self):
        """ Lähtöruutu
        """
        self.start = True
        self.blocked = False


    def set_visited(self):
        """ Vierailtu ruutu
        """
        self.visited = True


    def set_visited_jps(self, dir):
        """ Talletetaan vierailu skannaussuunta
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
        """ Tarkistetaan onko reitti jo tutkittu
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
