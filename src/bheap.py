class Bheap:
    """Class that creates a binary heap

    Attributes:
        heap: Heap
        size: Heap size
        maxsize: Heap max size
    """

    def __init__(self, size):
        """Constructor to create a new heap

        Args:
            size: max size
        """
        self.heap = [None] * (size+1)
        self.size = 0
        self.maxsize = size + 1


    def empty(self):
        """Check if heap is empty

        Returns:
            True, if empty.
        """
        return self.size == 0


    def put(self, value):
        """New element in heap
        """
        if self.size + 1 == self.maxsize:
            return
        self.heap[self.size + 1] = value
        self.size += 1
        self.heapify_put(self.size)


    def get(self):
        """Smallest element in heap out

        Returns:
            Smallest element in heap
        """
        if self.size == 0:
            return None
        else:
            res = self.heap[1]
            self.heap[1] = self.heap[self.size]
            self.heap[self.size] = None
            self.size -= 1
            self.heapify_get(1)
            return res


    def heapify_put(self, index):
        """Modify heap after new element in
        """
        parent = index // 2
        if index <= 1:
            return
        if self.heap[index] < self.heap[parent]:
            self.swap(index, parent)
        self.heapify_put(parent)


    def heapify_get(self, index):
        """Modify heap after element out
        """
        left = index * 2
        right = index * 2 + 1
        swap = 0

        if self.size < left:
            return
        elif self.size == left:
            if self.heap[index] > self.heap[left]:
                self.swap(index, left)
            return
        else:
            if self.heap[left] < self.heap[right]:
                swap = left
            else:
                swap = right
            if self.heap[index] > self.heap[swap]:
                self.swap(index, swap)

        self.heapify_get(swap)


    def swap(self, index1, index2):
        """Swap elements in heap
        """
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp
