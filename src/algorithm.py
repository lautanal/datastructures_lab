import dijkstra
import astar
import idastar
import jps


class Algorithm(dijkstra.DijkstraMixin, astar.AstarMixin, idastar.IdastarMixin, jps.JpsMixin):
    """Luokka, joka käynnistää eri algoritmit

    Attributes:
        map: Karttaruudukko
        drawfunc: Piirtofunktio
        method: Käytetty metodi
        diagonal: Polun tyyppi (diagonal / xy)
        animate: Animaatio päällä
    """


    def __init__(self, map, drawfunc):
        """Konstruktori, joka luo uuden Algorithm-alkion

        Args:
            map: Karttaruudukko
            drawfunc: Piirtofunktio
        """
        self.drawfunc = drawfunc
        self.map = map
        self.method = 'D'
        self.diagonal = False
        self.animate = False


    def set_method(self):
        """Metodin vaihto
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
        """Polun tyyppi (diagonal / xy)
        """
        if not self.method == 'J':
            if self.diagonal:
                self.diagonal = False
            else:
                self.diagonal = True


    def set_animate(self):
        """Animaatio päällä / pois
        """
        if self.animate:
            self.animate = False
        else:
            self.animate = True


    def set_map(self, map):
        """Uusi kartta
        """
        self.map = map
        self.method = 'D'
        self.diagonal = False
        self.animate = False


    def calculate(self):
        """Laskennan käynnistys
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
            print(f'\n*** REITTI LÖYTYI ***')
            if self.method == 'D':
                print('Dijkstran menetelmä')
            elif self.method == 'A':
                print('A* -menetelmä')
            elif self.method == 'I':
                print('IDA* -menetelmä')
            elif self.method == 'J':
                print('Jump Point Search -menetelmä')
            print(f'Laskenta vei {time:.3f} sekuntia\n' \
                f'Polun solmujen lukumäärä {npath}\nPolun painotettu pituus {costsum}')
            return True, npath, costsum, time
        else:
            print(f'\n*** REITTIÄ EI LÖYTYNYT ***')
            return False, 0, 0, 0
