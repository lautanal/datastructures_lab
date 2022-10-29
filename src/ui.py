import os
import pygame
from map import Map
from draw import Draw
from algorithm import Algorithm
from files import Files
from perftest import Perftest


# Käyttöliittymä
class Ui:
    """Käyttöliittymän luokka

    Attributes:
        MAXWIDTH: Ikkunan maksimileveys pikseleinä
        MAXHEIGHT: Ikkunan maksimileveys pikseleinä
        TEXTAREA: Ikkunan tekstiosan koko
        TEXTPOS: Ikkunan tekstiosan paikka
        nrows: Rivien lukumäärä
        ncols: Sarakkeiden lukumäärä
        gsize: Karttaruudun koko pikseleinä
        win: Pygame-ikkuna
        width: Pygame-ikkunan leveys pikseleinä
        height: Pygame-ikkunan korkeus pikseleinä
        map: Karttaruudukko
        costmap: Kartan tyyppi, costmap=True -> painotettu ruutukartta
        drawfunc: Piirtorutiini
        algorithm: Algoritmien käynnistysrutiini
        files = Tiedostojen käsittelijä
        edit: Kartan editointi käynnissä
        run: Pygame-käynnissä
    """

    def __init__(self, MAXWIDTH, MAXHEIGHT, nrows, ncols, TEXTAREA, TEXTPOS):
        """Luokan konstruktori, joka luo uuden käyttöliittymän.

        Args:
            MAXWIDTH: Ikkunan maksimileveys pikseleinä
            MAXHEIGHT: Ikkunan maksimileveys pikseleinä
            TEXTAREA: Ikkunan tekstiosan koko pikseleinä
            TEXTPOS: Ikkunan tekstiosan paikka, True -> alalaita, False -> oikea sivu
            nrows: Rivien lukumäärä
            ncols: Sarakkeiden lukumäärä
        """

        # Ikkunan kokoparametrit
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

        # Pygame-ikkunan luonti
        pygame.display.set_caption('Paras reitti')
        self.win = pygame.display.set_mode((self.width, self.height))

        # Kartan alustus
        self.map = Map(self.nrows, self.ncols, self.gsize)
        self.costmap = True
        self.map.generate_costs()

        # Algoritmi- ja piirtofunktioiden alustus
        self.drawfunc = Draw(self.win, self.width, self.height, self.map, self.TEXTPOS)
        self.algorithm = Algorithm(self.map, self.drawfunc.drawnode)
        self.drawfunc.set_texts(self.algorithm)
        self.files = Files()

        # Ohjelman tilat
        self.edit = False
        self.run = True


    def start(self):
        """Käyttöliittymän käynnistys.
        """

        # Event loop
        while self.run:
            self.drawfunc.drawmap(self.edit, self.algorithm.animate)
            for event in pygame.event.get():
                # Lopetus
                if event.type == pygame.QUIT:
                    self.run = False

            # Hiirikomennot
                # Alku-, loppupisteet, esteiden syöttö  ja editointi (hiiren vasen näppäin)
                if pygame.mouse.get_pressed()[0]:
                    self.leftclick()

                # Pisteiden pyyhkiminen (hiiren oikea näppäin)
                elif pygame.mouse.get_pressed()[2]:
                    self.rightclick()

            # Näppäinkomennot
                if event.type == pygame.KEYDOWN:
                    self.keyboard(event)

        pygame.quit()


    def leftclick(self):
        """Hiiren vasemman näppäimen klikkaus.
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
        """Hiiren oikean näppäimen klikkaus.
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
        """Klikkauksen koordinaatit.

        Args:
            pos: Klikkauksen positio pikseleinä

        Returns:
            row: Klikatun ruudun rivi
            col: Klikatun ruudun sarake
        """
        col = pos[0] // self.gsize
        row = pos[1] // self.gsize
        return row, col


    def keyboard(self, event):
        """Näppäinkomennot.
        """
        # A: Animation, animaatio päälle / pois
        if event.key == pygame.K_a:
            self.algorithm.set_animate()
            self.drawfunc.set_texts_animation(self.algorithm)

        # C: Clear, Lähtö- ja maalipisteiden pyyhkiminen
        if event.key == pygame.K_c:
            if self.map.goal:
                self.map.goal.clear()
                self.map.set_goal(None)
            elif self.map.start:
                self.map.start.clear()
                self.map.set_start(None)
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # D: Diagonal, polun tyyppi
        if event.key == pygame.K_d:
            self.algorithm.set_diagonal()
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # E: Edit, ruutujen editoinnin aloitus
        if event.key == pygame.K_e:
            print('Editointi aloitus')
            self.edit = True

        # F: Kartan luku tiedostosta f.map
        if event.key == pygame.K_f:
            self.files.fname = 'f.map'
            maparray = self.files.read()
            if maparray:
                self.newmap(maparray)

        # G: Generate, uusi painottamaton random-kartta
        if event.key == pygame.K_g:
            self.costmap = False
            self.newmap(None)

        # M: Method, metodin valinta
        if event.key == pygame.K_m:
            self.algorithm.set_method()
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # N: New, uusi painotettu random-kartta
        if event.key == pygame.K_n:
            self.costmap = True
            self.newmap(None)

        # Q: Quit, ruutujen editoinnin lopetus
        if event.key == pygame.K_q:
            print('Editointi lopetus')
            self.edit = False

        # R: Reset, lasketun reitin pyyhkiminen
        if event.key == pygame.K_r:
            self.map.reset()
            self.drawfunc.set_texts(self.algorithm)

        # S: Start, laskennan aloitus
        if event.key == pygame.K_s:
            if self.map.start and self.map.goal:
                self.map.reset()
                result = self.algorithm.calculate()
                self.drawfunc.set_results(result)

        # T: Test, suorituskykytesti, 3 menetelmää, painotetut ruudut
        if event.key == pygame.K_t:
            self.edit = False
            self.drawfunc.set_texts(self.algorithm)
            perftest = Perftest(self.MAXWIDTH, self.MAXHEIGHT, self.TEXTAREA, self.TEXTPOS, self.win, self.map, self.algorithm, self.drawfunc)
            perftest.test3()
            del perftest

        # P: Suorituskykytesti 4 menetelmää, painottamattomat ruudut, diagonaalireitti
        if event.key == pygame.K_p:
            self.edit = False
            self.drawfunc.set_texts(self.algorithm)
            perftest = Perftest(self.MAXWIDTH, self.MAXHEIGHT, self.TEXTAREA, self.TEXTPOS, self.win, self.map, self.algorithm, self.drawfunc)
            perftest.test4()
            del perftest

        # W: Write, kartan kirjoitus tiedostoon f.map
        if event.key == pygame.K_w:
            self.files.fname = 'f.map'
            self.files.write(self.map)

        # 1,2,3,4,5,6,7,8,9: Uusi kartta tiedostosta 1.map .... 9.map
        if event.key >= pygame.K_1 and event.key <= pygame.K_9:
            fname = str(event.key-48) + '.map'
            self.files.fname = fname
            maparray = self.files.read()
            if maparray:
                self.newmap(maparray)

        # +: Uusi kartta, ruutujen määrän lisäys (+10 molemmissa suunnissa)
        if event.key == pygame.K_PLUS and self.ncols < 500:
            self.ncols += self.ncols // 10
            self.nrows += self.nrows // 10
            self.newmap(None)

        # -: Uusi kartta, ruutujen määrän vähennys (-10 molemmissa suunnissa)
        if event.key == pygame.K_MINUS and self.ncols > 10:
            self.ncols -= self.ncols // 10
            self.nrows -= self.nrows // 10
            self.newmap(None)


    def newmap(self, maparray):
        """Uusi kartta ja Pygame-ikkuna.

        Args:
            maparray: Kartta kirjaintaulukkona
        """
        # Kartan parametrit
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

        # Uusi Pygame-ikkuna
        oldwin = self.win
        self.win = pygame.display.set_mode((self.width, self.height))
        del oldwin

        # Uusi kartta
        oldmap = self.map
        self.map = Map(self.nrows, self.ncols, self.gsize)
        del oldmap

        # Ruutujen cost-arvot
        if maparray:
            self.map.set_costs(maparray)
        elif self.costmap:
            self.map.generate_costs()
        else:
            self.map.generate_obstacles()


        # Algoritmin ja piirtofunktion asetukset
        self.algorithm.set_map(self.map)
        self.drawfunc.set_win(self.win, self.width, self.height, self.map)
        self.drawfunc.set_texts(self.algorithm)
        self.edit = False
