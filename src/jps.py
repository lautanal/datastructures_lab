from math import sqrt
from heapq import heappush, heappop
from timeit import default_timer as timer

class JpsMixin:
#    def jps(map, animate, drawnode):
    def jps(self):
        """JPS -algorithm

        Attributes:
            map: Grid map
            animate: Animation on
            drawnode: Grid node draw function

        Returns:
            True: rRime elapsed
            nn: Number of route nodes
            dist: Path length
            path: Path jump point nodes
        """
        tstart = timer()

        # Heuristics
        self.map.heuristic_euclidian(self.map.goal)
    #        self.map.heuristic_chebyshev(self.map.goal)

        # Initial settings, scan all directions
        queue = []
        heappush(queue, (0, 0, 0, self.map.start, (1,1), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (1,0), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (0,1), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (-1,1), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (-1,0), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (-1,-1), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (0,-1), [self.map.start]))
        heappush(queue, (0, 0, 0, self.map.start, (1,-1), [self.map.start]))
        drawcount = 0

        # Priority queue loop
        while queue:
            # Next node from heap
            est, dist, nn, node, dir, path = heappop(queue)
    #        print(f'ROW: {node.row} COL: {node.col} DIR: {dir} NN: {nn} DIST:{dist}')

            # Goal found
            if node == self.map.goal:
                return True, timer() - tstart, nn, dist, path

            # Node has been visited
            if node.check_visited_jps(dir):
                continue

            # Scan all directions
            if dir == (1,0) or dir == (-1,0):
                self.search_horizontal(node, dir[0], nn, dist, path, queue)
            elif dir == (0,1) or dir == (0,-1):  
                self.search_vertical(node, dir[1], nn, dist, path, queue)
            else:
                self.search_diagonal(node, dir, nn, dist, path, queue)
            node.set_visited_jps(dir)

            # Animation
            node.set_visited()
            if self.animate:
                if drawcount < 200:
                    drawcount += 1
                    self.drawfunc(node, False)
                else:
                    self.drawfunc(node, True)
                    drawcount = 0

        # Path not found
        tend = timer()
        return False, timer() - tstart, 0, 0, 0


    def search_horizontal(self, node0, hor_dir, nn, dist, path, queue): 
        """ Horizontal search
        """ 

        row0 = node0.row
        col0 = node0.col

        # Scan loop
        while True: 
            col1 = col0 + hor_dir

            # Node coordinates outside map
            if not self.map.on_map(row0, col1):
                return False

            # Next node
            node1 = self.map.nodes[row0][col1]

            # Blocked node        
            if node1.blocked: 
                return False

            # Add node to path
            path = path.copy()
            path.append(node1)

            # Goal
            if node1 == self.map.goal:
                self.addheap(queue, dist+1, nn, node1, (hor_dir, 0), path)
                return True 

            # Scan forward
            nn += 1        
            dist += 1
            col2 = col1 + hor_dir 
            jumppoint = False

            # Check if node is a jump point       
            if self.map.on_map(row0-1, col2) and not self.map.nodes[row0-1][col2].blocked and self.map.nodes[row0-1][col1].blocked:
                jumppoint = True
                self.addheap(queue, dist, nn, node1, (hor_dir, -1), path)
            
            if self.map.on_map(row0+1, col2) and not self.map.nodes[row0+1][col2].blocked and self.map.nodes[row0+1][col1].blocked:
                jumppoint = True
                self.addheap(queue, dist, nn, node1, (hor_dir, 1), path)
            
            if jumppoint:
                self.addheap(queue, dist, nn, node1, (hor_dir, 0), path)
                return True

            # Next node           
            col0 = col1


    def search_vertical(self, node0, vert_dir, nn, dist, path, queue): 
        """ Vertical search
        """ 

        row0 = node0.row
        col0 = node0.col

        # Scan loop
        while True: 
            row1 = row0 + vert_dir

            # Node coordinates outside map
            if not self.map.on_map(row1, col0):
                return False

            #Next node        
            node1 = self.map.nodes[row1][col0]

            # Blocked node
            if node1.blocked: 
                return False

            # Add node to path
            path = path.copy()
            path.append(node1)

            #Goal
            if node1 == self.map.goal:
                self.addheap(queue, dist+1, nn, node1, (vert_dir, 0), path)
                return True 

            # Scan forward
            nn += 1        
            dist += 1
            row2 = row1 + vert_dir 
            jumppoint = False

            # Check if node is a jump point        
            if self.map.on_map(row2, col0-1) and not self.map.nodes[row2][col0-1].blocked and self.map.nodes[row1][col0-1].blocked:
                jumppoint = True
                self.addheap(queue, dist, nn, node1, (-1, vert_dir), path)
            
            if self.map.on_map(row2, col0+1) and not self.map.nodes[row2][col0+1].blocked and self.map.nodes[row1][col0+1].blocked:
                jumppoint = True
                self.addheap(queue, dist, nn, node1, (1, vert_dir), path)
            
            if jumppoint:
                self.addheap(queue, dist, nn, node1, (0, vert_dir), path)
                return True

            # Seuraava ruutu            
            row0 = row1


    def search_diagonal(self, node0, dir, nn, dist, path, queue): 
        """ Diagonal search.
        """ 

        row0 = node0.row
        col0 = node0.col
        hor_dir = dir[0]
        vert_dir = dir[1]

        # Scan loop
        while True: 
            row1 = row0 + vert_dir 
            col1 = col0 + hor_dir

            # Next node coordinates outside map       
            if not self.map.on_map(row1, col1):
                return False 

            # Next node
            node1 = self.map.nodes[row1][col1]

            # Blocked node       
            if node1.blocked: 
                return False 

            # Add node to path
            path = path.copy()
            path.append(node1)

            #Goal
            if node1 == self.map.goal:
                self.addheap(queue, dist+sqrt(2), nn, node1, (hor_dir, 0), path)
                return True

            # Scan forward
            nn += 1        
            dist += sqrt(2)
            col2 = col1 + hor_dir
            row2 = row1 + vert_dir 

            # Forced neighbours       
            if self.map.on_map(row2, col0) and not self.map.nodes[row2][col0].blocked and self.map.nodes[row1][col0].blocked:
                self.addheap(queue, dist, nn, node1, (-hor_dir, vert_dir), path)
            
            if self.map.on_map(row0, col2) and not self.map.nodes[row0][col2].blocked and self.map.nodes[row0][col1].blocked:
                self.addheap(queue, dist, nn, node1, (hor_dir, -vert_dir), path)

            # Horizontal and vertical scan        
            hsearch = self.search_horizontal(node1, hor_dir, nn, dist, path, queue)
            vsearch = self.search_vertical(node1, vert_dir, nn, dist, path, queue)

            # Jump point found
            if hsearch or vsearch:
                self.addheap(queue, dist, nn, node1, (hor_dir, vert_dir), path)
                return True

            # Next node
            row0 = row1
            col0 = col1


    def addheap(self, queue, dist, nn, node, dir, path):
        """ Add node and direction to heap
        """ 
        if node.check_visited_jps(dir):
            return
        heappush(queue, (dist+node.heuristic, dist, nn, node, dir, path))

