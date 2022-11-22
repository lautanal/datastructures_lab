from math import sqrt
from timeit import default_timer as timer
from heapq import heappush, heappop

class IdastarMixin:
#    def idastar(map, diagonal, animate, drawnode):
    def idastar(self):
        """IDA* -algorithm

        Attributes:
            map: Map grid
            diagonal: Path type (diagonal / xy)
            animate: Animation on/off
            drawnode: Grid node draw function

        Returns:
            True: Returns True if route found
            time: Time used for route calculation
        """
        tstart = timer()

        # Neighbours and heuristics
        if self.diagonal:
            self.map.neighbors_diag()
            self.map.heuristic_euclidian(self.map.goal)
    #       self.map.heuristic_chebyshev(self.map.goal)
        else:
            self.map.neighbors_xy()
            self.map.heuristic_manhattan(self.map.goal)

        # Initial settings
        self.map.start.costsum = 0
        threshold = self.map.start.heuristic
        paths = []
        heappush(paths, (0, [self.map.start]))
        drawcount = 0
        update = False

        # Search loop
        while paths:
            # Advance paths until threshold
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

                # Deep search until threshold
                res = self.idastar_search(path, threshold, newpaths, update)

                # Goal found
                if res < 0:
                    return True, timer() - tstart

                # New search threshold
                elif res < tmin:
                    tmin = res

            # New paths and threshold
            paths = newpaths
            threshold = tmin


        # No route found
        return False, timer() - tstart


    def idastar_search(self, path, threshold, paths, update):
        """IDA* -deep search routine

        Attributes:
            path: Path to node
            threshold: Search threshold
            goal: Goal node
            paths: Search paths
            diagonal: Path type (diagonal / xy)
            animate: Animation on/off
            drawnode: Grid node drawing function

        Returns:
            tmin: New search threshold
        """

        node = path[-1]
        costsum = node.costsum

        # Goal found
        if node == self.map.goal:
            return -1

        # Animation
        node.set_visited()
        if self.animate:
            self.drawfunc(node, update)

        # Search threshold exceeded
        estimate = costsum + node.heuristic
        if estimate > threshold:
            heappush(paths, (estimate, path.copy()))
            return estimate

        # Neighbours
        tmin = float("inf")
        for neighbor in node.neighbors:
            if neighbor not in path:
                deltacost = neighbor.cost
                # Diagonal path
                if self.diagonal:
                    deltacost = sqrt((node.row - neighbor.row)**2 + \
                        (node.col - neighbor.col)**2) * (node.cost + neighbor.cost)/2
                newcostsum = costsum + deltacost

                # Continue deep search
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
