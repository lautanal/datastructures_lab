import dijkstra
import astar
import idastar
import jps


class Algorithm(dijkstra.DijkstraMixin, astar.AstarMixin, idastar.IdastarMixin, jps.JpsMixin):
    """Class that starts different algorithms

    Attributes:
        map: Map grid
        drawfunc: Drawing function
        method: Method used
        diagonal: Path type (diagonal / xy)
        animate: Animation on/off
    """


    def __init__(self, map, drawfunc):
        """Constructor to create a new algorithm instance

        Args:
            map: Grid map
            drawfunc: Drawing function
        """
        self.drawfunc = drawfunc
        self.map = map
        self.method = 'D'
        self.diagonal = False
        self.animate = False


    def set_method(self):
        """Method selection
        """
        if self.method == 'D':
            self.method = 'A'
        elif self.method == 'A':
            self.method = 'I'
        elif self.method == 'I':
            if self.map.weighted:
                self.method = 'D'
            else:
                self.method = 'J'
                self.diagonal = True
        elif self.method == 'J':
            self.method = 'D'


    def set_diagonal(self):
        """Path type (diagonal / xy)
        """
        if not self.method == 'J':
            if self.diagonal:
                self.diagonal = False
            else:
                self.diagonal = True


    def set_animate(self):
        """Animation on / off
        """
        if self.animate:
            self.animate = False
        else:
            self.animate = True


    def set_map(self, map):
        """New map
        """
        self.map = map
        self.method = 'D'
        self.diagonal = False
        self.animate = False


    def calculate(self):
        """Route calculation
        """
        if self.method == 'D':
            result, time = self.dijkstra()
        elif self.method == 'A':
            result, time = self.astar()
        elif self.method == 'I':
            result, time = self.idastar()
        elif self.method == 'J':
            result, time, npath, costsum, path = self.jps()
        if result:
            if self.method == 'J':
                self.map.track_path_jps(path)
            else:
                npath, costsum = self.map.track_path(self.diagonal)
            print(f'\n*** ROUTE FOUND ***')
            if self.method == 'D':
                print('Dijkstra method')
            elif self.method == 'A':
                print('A* -method')
            elif self.method == 'I':
                print('IDA* -method')
            elif self.method == 'J':
                print('Jump Point Search -method')
            print(f'Calculation took {time:.3f} seconds\n' \
                f'Route node count {npath}\nRoute weighted length {costsum}')
            return True, npath, costsum, time
        else:
            print(f'\n*** ROUTE NOT FOUND ***')
            return False, 0, 0, 0
