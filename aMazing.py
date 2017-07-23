class MinHeap:
    """Defines an instance of a minimum heap data structure"""

    def __init__(self):
        self.heap = []

    def insert(self, item):
        """Inserts an item into the heap"""

        self.heap.append(item)
        self.sift_up(len(self.heap) - 1)

    def sift_up(self, index):
        """Sifts an item upwards until it reaches it's correct position"""

        #Using fact that children of node n are nodes 2n + 1 and 2n + 2
        parentIndex = int((index - 2 + (index % 2)) / 2)

        if parentIndex >= 0 and self.heap[index] < self.heap[parentIndex]:
            temp = self.heap[parentIndex]
            self.heap[parentIndex] = self.heap[index]
            self.heap[index] = temp

            self.sift_up(parentIndex)

    def sift_down(self, index):
        """Sifts an item downwards until it reaches it's correct position"""

        child1 = 2 * index + 1
        if child1 < len(self.heap):
            if child1 + 1 < len(self.heap):
                if self.heap[index] > min(self.heap[child1], self.heap[child1 + 1]):
                    if (self.heap[child1] < self.heap[child1 + 1]):
                        temp = self.heap[child1]
                        self.heap[child1] = self.heap[index]
                        self.heap[index] = temp

                        self.sift_down(child1)

                    else:
                        temp = self.heap[child1 + 1]
                        self.heap[child1 + 1] = self.heap[index]
                        self.heap[index] = temp

                        self.sift_down(child1 + 1)

            else:
                if self.heap[index] > self.heap[child1]:
                    temp = self.heap[child1]
                    self.heap[child1] = self.heap[index]
                    self.heap[index] = temp

                    self.sift_down(child1)

    def extract_min(self):
        """Pops the root node from the heap"""

        root = self.heap[0]

        self.heap[0] = self.heap[-1]
        del self.heap[-1]
        self.sift_down(0)

        return root
