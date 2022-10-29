import pygame

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 128, 255)
YELLOW = (255, 255, 0)
ORANGE = (255, 165, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
GRAYSHADES = [(240,240,240),(220,220,220),(200,200,200),(180,180,180),(160,160,160),(140,140,140),(120,120,120),(100,100,100),(80,80,80),(60,60,60),(0,0,0)]

class Draw:
    """Luokka, jossa on Pygame-piirtorutiinit

    Attributes:
        win = Pygame-ikkuna
        map = Karttaruudukko
        width = Pygame-ikkunan leveys
        height = Pygame-ikkunan korkeus
        nrows = Karttaruudukon rivien lukumäärä
        ncols = Karttaruudukon sarakkeiden lukumäärä
        gsize = Ruudun koko pikseleinä
        textpos = Tekstialueen paikka
        t1 = Tekstin 1 paikka
        t7 = Tekstin 7 paikka
        text1 = Teksti 1
        text2 = Teksti 2
        text3 = Teksti 3
        text4 = Teksti 4
        text5 = Teksti 5
        text6 = Teksti 6
        text7 = Teksti 7
        text8 = Teksti 8
        text9 = Teksti 9
        text10 = Teksti 10
        text11 = Teksti 11
    """


    def __init__(self, win, width, height, map, textpos):
        """Konstruktori, joka luo uuden Draw-alkion

        Attributes:
            win = Pygame-ikkuna
            width = Pygame-ikkunan leveys
            height = Pygame-ikkunan korkeus
            map = Karttaruudukko
            textpos = Tekstialueen paikka
        """
        self.win = win
        self.map = map
        self.width = width
        self.height = height
        self.textpos = textpos
        self.nrows = map.nrows
        self.ncols = map.ncols
        self.gsize = map.gsize
        if self.textpos:
            self.t1 = (40, self.nrows*self.gsize + 20)
            self.t7 = (self.t1[0] + 250, self.t1[1])
        else:
            self.t1 = (self.ncols*self.gsize + 20, 20)
            self.t7 = (self.t1[0], self.t1[1] + 200)
        self.text1 = ''
        self.text2 = ''
        self.text3 = ''
        self.text4 = ''
        self.text5 = ''
        self.text6 = ''
        self.text7 = ''
        self.text8 = ''
        self.text9 = ''
        self.text10 = ''
        self.text11 = ''


    def drawmap(self, numbers, animate):
        """Koko karttaruudukon piirto
        """
        font = pygame.font.SysFont('Arial', self.gsize // 2)
        for row in self.map.nodes:
            for node in row:

                # Väritetään ruutu
                color = GRAYSHADES[node.cost]
                if node.blocked:
                    color = BLACK
                elif node.path:
                    color = RED
                elif node.start or node.startmark:
                    color = BLUE
                elif node.goal or node.goalmark:
                    color = ORANGE
                elif animate and node.visited:
                    color = GREEN

                pygame.draw.rect(self.win, color, (node.x, node.y, self.gsize, self.gsize))

                # Ruutujen numerot
                if numbers:
                    if not node.blocked:
                        if node.cost < 10:
                            self.win.blit(font.render(str(node.cost), True, (128, 128, 128)),
                                    (node.x+2*(self.gsize//5), node.y+self.gsize//4))
                        else:
                            self.win.blit(font.render(str(node.cost), True, (128, 128, 128)),
                                    (node.x+self.gsize//3, node.y+self.gsize//4))

        # Tekstipaneeli
        if self.textpos:
            pygame.draw.rect(self.win, (180, 180, 180), (0, self.nrows*self.gsize, self.width, self.height-self.nrows*self.gsize))
            pygame.draw.line(self.win, (60, 60, 60), (0, self.nrows*self.gsize), (self.width, self.nrows*self.gsize))
        else:
            pygame.draw.rect(self.win, (180, 180, 180), (self.ncols*self.gsize, 0, self.width-self.ncols*self.gsize, self.height))
            pygame.draw.line(self.win, (60, 60, 60), (self.ncols*self.gsize, 0), (self.ncols*self.gsize, self.height))

        font = pygame.font.SysFont('Arial', 15)
        self.win.blit(font.render(str(self.text1), True, (64, 64, 64)), self.t1)
        self.win.blit(font.render(str(self.text2), True, (64, 64, 64)), (self.t1[0], self.t1[1] + 20))
        self.win.blit(font.render(str(self.text3), True, (64, 64, 64)), (self.t1[0], self.t1[1] + 40))
        self.win.blit(font.render(str(self.text4), True, (64, 64, 64)), (self.t1[0], self.t1[1] + 60))
        self.win.blit(font.render(str(self.text5), True, (64, 64, 64)), (self.t1[0], self.t1[1] + 80))
        self.win.blit(font.render(str(self.text6), True, (64, 64, 64)), (self.t1[0], self.t1[1] + 100))
        self.win.blit(font.render(str(self.text7), True, (64, 64, 64)), self.t7)
        self.win.blit(font.render(str(self.text8), True, (64, 64, 64)), (self.t7[0], self.t7[1] + 20))
        self.win.blit(font.render(str(self.text9), True, (64, 64, 64)), (self.t7[0], self.t7[1] + 40))
        self.win.blit(font.render(str(self.text10), True, (64, 64, 64)), (self.t7[0], self.t7[1] + 60))
        self.win.blit(font.render(str(self.text11), True, (64, 64, 64)), (self.t7[0], self.t7[1] + 80))

        # Ikkunan päivitys
        pygame.display.update()


    def drawnode(self, node, update):
        """Yhden karttaruudun piirto
        """
        if not node.start:
            pygame.draw.rect(self.win, GREEN, (node.x, node.y, self.gsize, self.gsize))

            # Update
            if update:
                pygame.display.update()


    def set_win(self, win, width, height, map):
        """Pygame-ikkunan asetukset
        """
        self.win = win
        self.map = map
        self.width = width
        self.height = height
        self.nrows = map.nrows
        self.ncols = map.ncols
        self.gsize = map.gsize
        if self.textpos:
            self.t1 = (40, self.nrows*self.gsize + 20)
            self.t7 = (self.t1[0] + 250, self.t1[1])
        else:
            self.t1 = (self.ncols*self.gsize + 20, 20)
            self.t7 = (self.t1[0], self.t1[1] + 200)


    def set_texts(self, algorithm):
        """Pygame-ikkunan tekstit
        """
        if algorithm.method == 'D':
            self.text1 = 'Metodi (m): Dijkstra'
        elif algorithm.method == 'A':
            self.text1 = 'Metodi (m): A*'
        elif algorithm.method == 'I':
            self.text1 = 'Metodi (m): IDA*'
        elif algorithm.method == 'J':
            self.text1 = 'Metodi (m): Jump Point Search'
        if algorithm.diagonal:
            self.text2 = 'Polun tyyppi (d): viisto'
        else:
            self.text2 = 'Polun tyyppi (d): xy'
        if algorithm.animate:
            self.text3 = 'Animaatio (a): kyllä'
        else:
            self.text3 = 'Animaatio (a): ei'
        self.text4 = f'Kartan koko: {self.nrows} x {self.ncols}'
        self.text5 = ''
        if self.map.start:
            self.text5 = f'Lähtö x,y: {str(self.map.start.col)}, {str(self.map.start.row)}'
        self.text6 = ''
        if self.map.goal:
            self.text6 = f'Maali x,y: {str(self.map.goal.col)}, {str(self.map.goal.row)}'
        self.text7 = ''
        self.text8 = ''
        self.text9 = ''
        self.text10 = ''


    def set_texts_animation(self, algorithm):
        """Pygame-ikkunan teksti, animaatio
        """
        if algorithm.animate:
            self.text3 = 'Animaatio (a): kyllä'
        else:
            self.text3 = 'Animaatio (a): ei'


    def set_results(self, result):
        """Laskennan tulokset näkyville
        """
        if result[0]:
            self.text7 = '*** TULOKSET ***'
            self.text8 = f'Polun solmujen lukumäärä {result[1]}'
            self.text9 = f'Polun painotettu pituus {result[2]:.1f}'
            self.text10 = f'Laskenta vei {result[3]:.3f} sekuntia'
            self.text11 = ''
            self.text11 = ''
        else:
            self.text7 = '*** REITTIÄ EI LÖYTYNYT ***'
            self.text8 = ''
            self.text9 = ''
            self.text10 = ''
            self.text11 = ''


    def test3_results(self, result):
        """Suoritusarvovertailun tulokset näkyville
        """
        self.text7 = '*** TULOKSET ***'
        self.text8 = f'Dijkstra keskimäärin: {result[0]:.3f} s'
        self.text9 = f'A* keskimäärin : {result[1]:.3f} s'
        self.text10 = f'IDA* keskimäärin: {result[2]:.3f} s'
        self.text11 = ''


    def test4_results(self, result):
        """Suoritusarvovertailun tulokset näkyville
        """
        self.text7 = '*** TULOKSET ***'
        self.text8 = f'Dijkstra keskimäärin: {result[0]:.3f} s'
        self.text9 = f'A* keskimäärin : {result[1]:.3f} s'
        self.text10 = f'IDA* keskimäärin: {result[2]:.3f} s'
        self.text11 = f'JPS keskimäärin: {result[3]:.3f} s'
