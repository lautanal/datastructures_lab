import os
import pygame
from map import Map
from draw import Draw
from algorithm import Algorithm
from files import Files
from perftest import Perftest


# Käyttöliittymä
class Ui:
    """User interface class

    Attributes:
        MAXWIDTH: Max window width in pixels
        MAXHEIGHT: Max window height in pixels
        TEXTAREA: Window text part size in pixels
        TEXTPOS: Text window position
        nrows: Row number
        ncols: Column number
        gsize: Grid square size in pixels
        win: Pygame-window
        width: Pygame-window size in pixels
        height: Pygame-iwindow height in pixels
        map: grid map
        costmap: Map type (costmap is with weighted nodes)
        drawfunc: Draw function
        algorithm: Algorithm routines
        files = File handler
        edit: Map edit in operation
        run: Pygame is running
    """

    def __init__(self, MAXWIDTH, MAXHEIGHT, nrows, ncols, TEXTAREA, TEXTPOS):
        """The constructor that creates a user interface.

        Args:
            MAXWIDTH: Max window width in pixels
            MAXHEIGHT: Max window height in pixels
            TEXTAREA: Window text part size in pixels
            TEXTPOS: Text window position, True -> bottom, False -> right side
            nrows: Row number
            ncols: Column number
        """

        # IWindow parameters
        if TEXTPOS:
            self.MAXWIDTH = MAXWIDTH
            self.MAXHEIGHT = MAXHEIGHT - TEXTAREA
        else:
            self.MAXWIDTH = MAXWIDTH - TEXTAREA
            self.MAXHEIGHT = MAXHEIGHT
        self.TEXTAREA = TEXTAREA
        self.gsize = min(self.MAXWIDTH // ncols, self.MAXHEIGHT // nrows)
        if TEXTPOS:
            self.width = self.gsize * ncols
            self.height = self.gsize * nrows + TEXTAREA
        else:
            self.width = self.gsize * ncols + TEXTAREA
            self.height = self.gsize * nrows
        self.TEXTPOS = TEXTPOS
        self.nrows = nrows
        self.ncols = ncols

        # Pygame-window
        pygame.display.set_caption('Best route')
        self.win = pygame.display.set_mode((self.width, self.height))

        # Map init
        self.map = Map(self.nrows, self.ncols, self.gsize)
        self.costmap = True
        self.map.generate_costs()

        # Algorithm and draw function init
        self.drawfunc = Draw(self.win, self.width, self.height, self.map, self.TEXTPOS)
        self.algorithm = Algorithm(self.map, self.drawfunc.drawnode)
        self.drawfunc.set_texts(self.algorithm)
        self.files = Files()

        # Program run status
        self.edit = False
        self.run = True


    def start(self):
        """User interface start.
        """

        # Event loop
        while self.run:
            self.drawfunc.drawmap(self.edit, self.algorithm.animate)
            for event in pygame.event.get():
                # Lopetus
                if event.type == pygame.QUIT:
                    self.run = False

            # Mouse commands
                # Alku-, loppupisteet, esteiden syöttö  ja editointi (hiiren vasen näppäin)
                if pygame.mouse.get_pressed()[0]:
                    self.leftclick()

                # Pisteiden pyyhkiminen (hiiren oikea näppäin)
                elif pygame.mouse.get_pressed()[2]:
                    self.rightclick()

            # Keyboard commands
                if event.type == pygame.KEYDOWN:
                    self.keyboard(event)

        pygame.quit()


    def leftclick(self):
        """Mouse left click.
        """
        pos = pygame.mouse.get_pos()
        row, col = self.get_clickpos(pos)
        if row < self.nrows and col < self.ncols:
            node = self.map.nodes[row][col]
            if self.edit:
                if not node.blocked and node.cost < 9:
                    node.cost += 1
            else:
                if not self.map.start:
                    node.set_start()
                    self.map.set_start(node)
                    self.drawfunc.set_texts(self.algorithm)
                elif not self.map.goal and node != self.map.start:
                    node.set_goal()
                    self.map.set_goal(node)
                    self.drawfunc.set_texts(self.algorithm)
                elif node != self.map.goal and node != self.map.start:
                    node.set_blocked()


    def rightclick(self):
        """Mouse right click.
        """
        pos = pygame.mouse.get_pos()
        row, col = self.get_clickpos(pos)
        if row < self.nrows and col < self.ncols:
            node = self.map.nodes[row][col]
            if self.edit:
                if not node.blocked and node.cost > 1:
                    node.cost -= 1
            else:
                if node == self.map.start:
                    self.map.set_start(None)
                elif node == self.map.goal:
                    self.map.set_goal(None)
                self.map.reset()
                self.drawfunc.set_texts(self.algorithm)
                node.clear()


    def get_clickpos(self, pos):
        """Click position.

        Args:
            pos: Click position in pixels

        Returns:
            row: Click row
            col: Click column
        """
        col = pos[0] // self.gsize
        row = pos[1] // self.gsize
        return row, col


    def keyboard(self, event):
        """Keyboard commands.
        """
        # A: Animation, animation on / off
        if event.key == pygame.K_a:
            self.algorithm.set_animate()
            self.drawfunc.set_texts_animation(self.algorithm)

        # C: Clear, clear start and goal positions
        if event.key == pygame.K_c:
            if self.map.goal:
                self.map.goal.clear()
                self.map.set_goal(None)
            elif self.map.start:
                self.map.start.clear()
                self.map.set_start(None)
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # D: Diagonal, path type
        if event.key == pygame.K_d:
            self.algorithm.set_diagonal()
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # E: Edit, start editing grid nodes
        if event.key == pygame.K_e:
            print('Editointi aloitus')
            self.edit = True

        # F: File read, read map file f.map
        if event.key == pygame.K_f:
            self.files.fname = 'f.map'
            maparray = self.files.read()
            if maparray:
                self.newmap(maparray)

        # G: Generate, new randow map (without node weights)
        if event.key == pygame.K_g:
            self.costmap = False
            self.newmap(None)

        # M: Method, method selection
        if event.key == pygame.K_m:
            self.algorithm.set_method()
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # N: New, new random map with weights
        if event.key == pygame.K_n:
            self.costmap = True
            self.newmap(None)

        # Q: Quit, quit editing
        if event.key == pygame.K_q:
            print('Editointi lopetus')
            self.edit = False

        # R: Reset, erase calculated route
        if event.key == pygame.K_r:
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # S: Start, start calculation
        if event.key == pygame.K_s:
            if self.map.start and self.map.goal:
                self.map.reset()
                result = self.algorithm.calculate()
                self.drawfunc.set_results(result)

        # T: Test, performance test, 3 methods, weighted nodes
        if event.key == pygame.K_t:
            self.edit = False
            self.drawfunc.set_texts(self.algorithm)
            perftest = Perftest(self.MAXWIDTH, self.MAXHEIGHT, self.TEXTAREA, self.TEXTPOS, self.win, self.map, self.algorithm, self.drawfunc)
            perftest.test3()
            del perftest

        # P: performance test, 3 methods, weighless nodes, diagonal path
        if event.key == pygame.K_p:
            self.edit = False
            self.drawfunc.set_texts(self.algorithm)
            perftest = Perftest(self.MAXWIDTH, self.MAXHEIGHT, self.TEXTAREA, self.TEXTPOS, self.win, self.map, self.algorithm, self.drawfunc)
            perftest.test4()
            del perftest

        # W: Write, write map to file f.map
        if event.key == pygame.K_w:
            self.files.fname = 'f.map'
            self.files.write(self.map)

        # 1,2,3,4,5,6,7,8,9: New map from file 1.map .... 9.map
        if event.key >= pygame.K_1 and event.key <= pygame.K_9:
            fname = str(event.key-48) + '.map'
            self.files.fname = fname
            maparray = self.files.read()
            if maparray:
                self.newmap(maparray)

        # +: New map, increase node count (+10 in both directions)
        if event.key == pygame.K_PLUS and self.ncols < 500:
            self.ncols += self.ncols // 10
            self.nrows += self.nrows // 10
            self.newmap(None)

        # -: New map, decrease node count (-10 in both directions)
        if event.key == pygame.K_MINUS and self.ncols > 10:
            self.ncols -= self.ncols // 10
            self.nrows -= self.nrows // 10
            self.newmap(None)


    def newmap(self, maparray):
        """New map and Pygame window.

        Args:
            maparray: map as an array
        """
        # Map parameters
        if maparray:
            self.ncols = len(maparray[0])
            self.nrows = len(maparray)

        self.gsize = min(self.MAXWIDTH // self.ncols, self.MAXHEIGHT // self.nrows)
        if self.TEXTPOS:
            self.width = self.gsize * self.ncols
            self.height = self.gsize * self.nrows + self.TEXTAREA
        else:
            self.width = self.gsize * self.ncols + self.TEXTAREA
            self.height = self.gsize * self.nrows

        # New Pygame window
        oldwin = self.win
        self.win = pygame.display.set_mode((self.width, self.height))
        del oldwin

        # New map
        oldmap = self.map
        self.map = Map(self.nrows, self.ncols, self.gsize)
        del oldmap

        # Node costs generation
        if maparray:
            self.map.set_costs(maparray)
        elif self.costmap:
            self.map.generate_costs()
        else:
            self.map.generate_obstacles()


        # Algorithm and draw function settings
        self.algorithm.set_map(self.map)
        self.drawfunc.set_win(self.win, self.width, self.height, self.map)
        self.drawfunc.set_texts(self.algorithm)
        self.edit = False
