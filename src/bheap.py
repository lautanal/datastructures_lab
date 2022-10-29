class Bheap:
    """Luokka, joka mallintaa binäärikeon

    Attributes:
        heap: Keko
        size: Keon koko
        maxsize: Maksimikoko
    """

    def __init__(self, size):
        """Luokan konstruktori, joka luo uuden binääriminimikeon.

        Args:
            size: Keon maksimikoko
        """
        self.heap = [None] * (size+1)
        self.size = 0
        self.maxsize = size + 1


    def empty(self):
        """Tarkistus, onko keko tyhjä.

        Returns:
            True, jos keko tyhjä.
        """
        return self.size == 0


    def put(self, value):
        """Uuden alkion tallennus kekoon.
        """
        if self.size + 1 == self.maxsize:
            return
        self.heap[self.size + 1] = value
        self.size += 1
        self.heapify_put(self.size)


    def get(self):
        """Pienin alkio ulos keosta.

        Returns:
            Pienin alkio keossa.
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
        """Korjataan keon rakenne minimikeoksi uuden alkion lisäämisen jälkeen.
        """
        parent = index // 2
        if index <= 1:
            return
        if self.heap[index] < self.heap[parent]:
            self.swap(index, parent)
        self.heapify_put(parent)


    def heapify_get(self, index):
        """Korjataan keon rakenne minimikeoksi alkion poiston jälkeen.
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
        """Alkioiden paikan vaihto keossa.
        """
        temp = self.heap[index1]
        self.heap[index1] = self.heap[index2]
        self.heap[index2] = temp
