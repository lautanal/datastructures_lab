import pygame
from map import Map

class Perftest:
    """Luokka, joka käynnistää suorituskykytestauksen

    Attributes:
        WIDTH: Ikkunan maksimileveys pikseleinä
        TEXTAREA: Ikkunan tekstiosan koko pikseleinä
        nrows: Rivien lukumäärä
        ncols: Sarakkeiden lukumäärä
        gsize: Karttaruudun koko pikseleinä
        win: Pygame-ikkuna
        width: Pygame-ikkunan leveys pikseleinä
        height: Pygame-ikkunan korkeus pikseleinä
        map: Karttaruudukko
        drawfunc: Piirtorutiini
        algorithm: Algoritmien käynnistysrutiini
    """

    def __init__(self, WIDTH, HEIGHT, TEXTAREA, TEXTPOS, win, map, algorithm, drawfunc):
        """Konstruktori, joka luo uuden Perftest-alkion

        Args:
        WIDTH: Ikkunan maksimileveys pikseleinä
        TEXTAREA: Ikkunan tekstiosan koko pikseleinä
        TEXTPOS: True -> Tekstialue ruudun alallaidassa
        win: Pygame-ikkuna
        map: Karttaruudukko
        drawfunc: Piirtorutiini
        algorithm: Algoritmien käynnistysrutiini
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
        """Suorituskyvyn testausrutiini.
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
        """Suorituskyvyn testausrutiini.
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
        """Uusi kartta ja Pygame-ikkuna.
        """
        # Kartan parametrit
        self.gsize = min(self.WIDTH // self.ncols, self.HEIGHT // self.nrows)
        if self.TEXTPOS:
            self.width = self.gsize * self.ncols
            self.height = self.gsize * self.nrows + self.TEXTAREA
        else:
            self.width = self.gsize * self.ncols + self.TEXTAREA
            self.height = self.gsize * self.nrows

        # Uusi Pygame-ikkuna
        oldwin = self.win
        self.win = pygame.display.set_mode((self.width, self.height))
        del oldwin

        # Uusi kartta
        oldmap = self.map
        self.map = Map(self.nrows, self.ncols, self.gsize)
        del oldmap

        # Ruutujen cost-arvot tai esteet
        if obstacles:
            self.map.generate_obstacles()
        else:
            self.map.generate_costs()

        # Algoritmin ja piirtofunktion asetukset
        self.algorithm.set_map(self.map)
        self.drawfunc.set_win(self.win, self.width, self.height, self.map)
        if obstacles:
            self.algorithm.diagonal = True
        self.drawfunc.set_texts(self.algorithm)
