from math import sqrt
from timeit import default_timer as timer
from bheap import Bheap

class DijkstraMixin:
#    def dijkstra(map, diagonal, animate, drawnode):
    def dijkstra(self):
        """Dijkstran algoritmi

        Attributes:
            map: Karttaruudukko
            diagonal: Polun tyyppi (diagonal / xy)
            animate: Animaatio päällä
            drawnode: Karttaruudun piirtofunktio

        Returns:
            True: Palauttaa arvon True, jos reitti löytyi
            time: laskentaan kulunut aika
        """
        tstart = timer()

        # Naapurit
        if self.diagonal:
            self.map.neighbors_diag()
        else:
            self.map.neighbors_xy()

        # Alkuasetukset
        self.map.start.costsum = 0
        bheap = Bheap(self.map.nrows*self.map.ncols)
        bheap.put((0, 0, self.map.start))
        count = 0
        drawcount = 0

        # Binäärikeko-looppi
        while not bheap.empty():
            # Seuraava solmu keosta
            node = bheap.get()[2]

            # Maali löytyi
            if node == self.map.goal:
                return True, timer() - tstart

            # Käydään läpi naapurit
            for neighbor in node.neighbors:
                if neighbor.visited:
                    continue
                deltacost = neighbor.cost
                # Vino reitti
                if self.diagonal:
                    deltacost = sqrt((node.row - neighbor.row)**2 + \
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost) / 2
                newcostsum = node.costsum + deltacost

                # Löytyi parempi reitti
                if newcostsum < neighbor.costsum:
                    count += 1
                    neighbor.previous = node
                    neighbor.costsum = newcostsum
                    bheap.put((newcostsum, count, neighbor))

            # Merkitään solmu käsitellyksi
            node.set_visited()

            # Animaatio
            if self.animate:
                if drawcount < 200:
                    drawcount += 1
                    self.drawfunc(node, False)
                else:
                    self.drawfunc(node, True)
                    drawcount = 0

        # Polkua ei löytynyt
        return False, timer() - tstart
