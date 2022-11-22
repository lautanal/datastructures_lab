from math import sqrt
from timeit import default_timer as timer
from bheap import Bheap

class DijkstraMixin:
#    def dijkstra(map, diagonal, animate, drawnode):
    def dijkstra(self):
        """Dijkstra algorithm

        Attributes:
            map: Map grid
            diagonal: Path type (diagonal / xy)
            animate: Animation on/off
            drawnode: Grid node drawing function

        Returns:
            True: If route found
            time: Time used for route calculation
        """
        tstart = timer()

        # Neighbours
        if self.diagonal:
            self.map.neighbors_diag()
        else:
            self.map.neighbors_xy()

        # Initial settings
        self.map.start.costsum = 0
        bheap = Bheap(self.map.nrows*self.map.ncols)
        bheap.put((0, 0, self.map.start))
        count = 0
        drawcount = 0

        # Binary heap loop
        while not bheap.empty():
            # Next node from heap
            node = bheap.get()[2]

            # Goal found
            if node == self.map.goal:
                return True, timer() - tstart

            # Neighbours
            for neighbor in node.neighbors:
                if neighbor.visited:
                    continue
                deltacost = neighbor.cost
                # Diagonal path
                if self.diagonal:
                    deltacost = sqrt((node.row - neighbor.row)**2 + \
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost) / 2
                newcostsum = node.costsum + deltacost

                # A better route found
                if newcostsum < neighbor.costsum:
                    count += 1
                    neighbor.previous = node
                    neighbor.costsum = newcostsum
                    bheap.put((newcostsum, count, neighbor))

            # Mark node visited
            node.set_visited()

            # Animation
            if self.animate:
                if drawcount < 200:
                    drawcount += 1
                    self.drawfunc(node, False)
                else:
                    self.drawfunc(node, True)
                    drawcount = 0

        # Route not found
        return False, timer() - tstart
