from math import sqrt
from heapq import heappush, heappop
from timeit import default_timer as timer

class AstarMixin:
#    def astar(map, diagonal, animate, drawnode):
    def astar(self):
        """A* -algorithm

        Attributes:
            map: Map grid
            diagonal: Path type (diagonal / xy)
            animate: Animation on/off
            drawnode: Grid node draw function

        Returns:
            True: If route found
            time: Time used for route calculation
        """
        tstart = timer()

        # Neighbours and heuristics
        if self.diagonal:
            self.map.neighbors_diag()
            self.map.heuristic_euclidian(self.map.goal)
    #       self.map.heuristic_chebyshev(map.goal)
        else:
            self.map.neighbors_xy()
            self.map.heuristic_manhattan(self.map.goal)

        # Initial settings
        self.map.start.costsum = 0
        queue = []
        heappush(queue, (0, 0, self.map.start))
        count = 0
        drawcount = 0

        # Priority queue-loop
        while queue:
            # Nex node from stack
            node = heappop(queue)[2]

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
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost)/2
                newcostsum = node.costsum + deltacost

                # A better route found
                if newcostsum < neighbor.costsum:
                    count += 1
                    neighbor.previous = node
                    neighbor.costsum = newcostsum
                    heappush(queue,(newcostsum + neighbor.heuristic, count, neighbor))

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
