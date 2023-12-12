import pygame
from map import Map

class Perftest:
    """Class to start performance test

    Attributes:
        WIDTH: window max width in pixels
        TEXTAREA: window text panel width in pixels
        nrows: row count
        ncols: column count
        gsize: grid size in pixels
        win: Pygame-window
        width: Pygame-window width in pixels
        height: Pygame-window height in pixels
        map: map array
        drawfunc: draw function
        algorithm: algorithms
    """

    def __init__(self, WIDTH, HEIGHT, TEXTAREA, TEXTPOS, win, map, algorithm, drawfunc):
        """Konstruktori, joka luo uuden Perftest-alkion

        Args:
        WIDTH: window max width in pixels
        TEXTAREA: window text panel width in pixels
        TEXTPOS: True -> Text area in bottom part of the window
        win: Pygame-window
        map: map array
        drawfunc: draw function
        algorithm: algorithms
        """

        if TEXTPOS:
            self.WIDTH = WIDTH
            self.HEIGHT = HEIGHT - TEXTAREA
        else:
            self.WIDTH = WIDTH - TEXTAREA
            self.HEIGHT = HEIGHT
        self.TEXTAREA = TEXTAREA
        self.TEXTPOS = TEXTPOS
        self.ncols = 100
        self.nrows = 100
        self.gsize = min(self.WIDTH // self.ncols, self.HEIGHT // self.nrows)
        if self.TEXTPOS:
            self.width = self.gsize * self.ncols
            self.height = self.gsize * self.nrows + self.TEXTAREA
        else:
            self.width = self.gsize * self.ncols + self.TEXTAREA
            self.height = self.gsize * self.nrows

        self.win = win
        self.map = map
        self.algorithm = algorithm
        self.drawfunc = drawfunc


    def test3(self):
        """Performance test.
        """
        results = [0, 0, 0, 0]
        self.ncols = 150
        self.nrows = 100
        ntests = 5
        for _ in range(ntests):
            self.newmap(False)
            node = self.map.nodes[0][0]
            node.set_start()
            self.map.set_start(node)
            node = self.map.nodes[self.nrows-1][self.ncols-1]
            node.set_goal()
            self.map.set_goal(node)
            for i in range(3):
                self.map.reset()
                result = self.algorithm.calculate()
                self.drawfunc.drawmap(False, False)
                results[i] += result[3]
                self.algorithm.set_method()
        results[0] /= ntests
        results[1] /= ntests
        results[2] /= ntests
        self.drawfunc.test3_results(results)


    def test4(self):
        """Performance test.
        """
        results = [0, 0, 0, 0]
        self.ncols = 150
        self.nrows = 100
        ntests = 5
        for _ in range(ntests):
            self.newmap(True)
            node = self.map.nodes[0][0]
            node.set_start()
            self.map.set_start(node)
            node = self.map.nodes[self.nrows-1][self.ncols-1]
            node.set_goal()
            self.map.set_goal(node)
            node = self.map.nodes[self.nrows-2][self.ncols-1]
            node.clear()
            node = self.map.nodes[self.nrows-2][self.ncols-2]
            node.clear()
            node = self.map.nodes[self.nrows-1][self.ncols-2]
            node.clear()
            for i in range(4):
                self.map.reset()
                result = self.algorithm.calculate()
                self.drawfunc.drawmap(False, False)
                results[i] += result[3]
                self.algorithm.set_method()
        results[0] /= ntests
        results[1] /= ntests
        results[2] /= ntests
        results[3] /= ntests
        self.drawfunc.test4_results(results)


    def newmap(self, obstacles):
        """New map and Pygame-window.
        """
        # Map parameters
        self.gsize = min(self.WIDTH // self.ncols, self.HEIGHT // self.nrows)
        if self.TEXTPOS:
            self.width = self.gsize * self.ncols
            self.height = self.gsize * self.nrows + self.TEXTAREA
        else:
            self.width = self.gsize * self.ncols + self.TEXTAREA
            self.height = self.gsize * self.nrows

        # New Pygame-window
        oldwin = self.win
        self.win = pygame.display.set_mode((self.width, self.height))
        del oldwin

        # New map
        oldmap = self.map
        self.map = Map(self.nrows, self.ncols, self.gsize)
        del oldmap

        # Grid weights and obstacles
        if obstacles:
            self.map.generate_obstacles()
        else:
            self.map.generate_costs()

        # Algorithm and draw function settings
        self.algorithm.set_map(self.map)
        self.drawfunc.set_win(self.win, self.width, self.height, self.map)
        if obstacles:
            self.algorithm.diagonal = True
        self.drawfunc.set_texts(self.algorithm)
