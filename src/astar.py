from math import sqrt
from heapq import heappush, heappop
from timeit import default_timer as timer

class AstarMixin:
#    def astar(map, diagonal, animate, drawnode):
    def astar(self):
        """A* -algoritmi

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

        # Naapurit ja heuristiikka
        if self.diagonal:
            self.map.neighbors_diag()
            self.map.heuristic_euclidian(self.map.goal)
    #       self.map.heuristic_chebyshev(map.goal)
        else:
            self.map.neighbors_xy()
            self.map.heuristic_manhattan(self.map.goal)

        # Alkuasetukset
        self.map.start.costsum = 0
        queue = []
        heappush(queue, (0, 0, self.map.start))
        count = 0
        drawcount = 0

        # Prioriteettijono-looppi
        while queue:
            # Seuraava solmu keosta
            node = heappop(queue)[2]

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
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost)/2
                newcostsum = node.costsum + deltacost

                # Parempi reitti löytyi
                if newcostsum < neighbor.costsum:
                    count += 1
                    neighbor.previous = node
                    neighbor.costsum = newcostsum
                    heappush(queue,(newcostsum + neighbor.heuristic, count, neighbor))

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

        # Reittiä ei löytynyt
        return False, timer() - tstart
