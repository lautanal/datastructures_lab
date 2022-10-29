from math import sqrt
from timeit import default_timer as timer
from heapq import heappush, heappop

class IdastarMixin:
#    def idastar(map, diagonal, animate, drawnode):
    def idastar(self):
        """IDA* -algoritmi

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
    #       self.map.heuristic_chebyshev(self.map.goal)
        else:
            self.map.neighbors_xy()
            self.map.heuristic_manhattan(self.map.goal)

        # Alustukset
        self.map.start.costsum = 0
        threshold = self.map.start.heuristic
        paths = []
        heappush(paths, (0, [self.map.start]))
        drawcount = 0
        update = False

        # Hakulooppi
        while paths:
            # Edetään polkuja kunnes kynnys ylittyy
            tmin = float("inf")
            newpaths = []
            while paths:
                path = heappop(paths)[1]
                if drawcount < 200:
                    update = False
                    drawcount += 1
                else:
                    update = True
                    drawcount = 0

                # Syvyyshaku kynnykseen asti
                res = self.idastar_search(path, threshold, newpaths, update)

                # Maali löytyi
                if res < 0:
                    return True, timer() - tstart

                # Uusi hakukynnys
                elif res < tmin:
                    tmin = res

            # Uudet hakupolut ja uusi kynnys
            paths = newpaths
            threshold = tmin


        # Reittiä ei löytynyt
        return False, timer() - tstart


    def idastar_search(self, path, threshold, paths, update):
        """IDA* -syvyyshakurutiini

        Attributes:
            path: Polku ruutuun
            threshold: Etsintäkynnys
            goal: Maaliruutu
            paths: Etsintäpolut
            diagonal: Polun tyyppi (diagonal / xy)
            animate: Animaatio päällä
            drawnode: Karttaruudun piirtofunktio

        Returns:
            tmin: Uusi kynnysarvo etsinnälle
        """
        node = path[-1]
        costsum = node.costsum

        # Maali löytyi
        if node == self.map.goal:
            return -1

        # Animaatio
        node.set_visited()
        if self.animate:
            self.drawfunc(node, update)

        # Hakukynnys ylittyi
        estimate = costsum + node.heuristic
        if estimate > threshold:
            heappush(paths, (estimate, path.copy()))
            return estimate

        # Käydään läpi naapurit
        tmin = float("inf")
        for neighbor in node.neighbors:
            if neighbor not in path:
                deltacost = neighbor.cost
                # Viisto polku
                if self.diagonal:
                    deltacost = sqrt((node.row - neighbor.row)**2 + \
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost)/2
                newcostsum = costsum + deltacost

                # Jatketaan syvyyshakua
                if newcostsum < neighbor.costsum:
                    neighbor.costsum = newcostsum
                    neighbor.previous = node
                    path.append(neighbor)
                    res = self.idastar_search(path, threshold, paths, update)
                    if res < 0:
                        return res
                    elif res < tmin:
                        tmin = res
                    path.pop()

        return tmin
