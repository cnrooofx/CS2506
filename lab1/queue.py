"""Multi-level Feedback Queue.

Script Name: queue.py
Author: Conor Fox 119322236
"""

class FeedbackQueue:
    def __init__(self, quantum):
        """Initialise the queue."""
        self._body = [None] * 10
        self._front = 0
        self._size = 0
        self._quantum = quantum
    
    def __str__(self):
        """Return a string representation of the queue."""
        output = '<-'
        if self._size > 0:
            i = self._front
            for _ in range(self._size):
                output += str(self._body[i]) + '-'
                i = (i + 1) % len(self._body)
        output += '<'
        return output

    def add(self, item):
        """Add an item to the queue."""
        if self._size == 0:
            self._body[0] = item
            self._size = 1
        else:
            self._body[(self._front + self._size) % len(self._body)] = item
            self._size += 1
            if self._size == len(self._body):
                self.__requeue()

    def remove(self):
        """Return (and remove) the item in the queue for longest."""
        if self._size == 0:
            return None
        item = self._body[self._front]
        self._body[self._front] = None
        if self._size == 1:
            self._front = 0
            self._size = 0
        else:
            self._front = (self._front + 1) % len(self._body)
            self._size -= 1
        if ((self._size / len(self._body)) < 0.25) and len(self._body) > 10:
            self.__requeue()
        return item

    @property
    def length(self):
        """Return the number of items in the queue."""
        return self._size

    @property
    def first(self):
        """Return the first item in the queue."""
        if self._size == 0:
            return None
        return self._body[self._front]
    
    def get_quantum(self):
        return self._quantum

    def set_quantum(self, quantum):
        self._quantum = quantum
    
    def __requeue(self):
        """Grow and shrink the internal queue to save space."""
        oldbody = self._body
        oldlength = len(self._body)
        self._body = [None] * (2*self._size)
        oldpos = self._front
        pos = 0
        for _ in range(self._size):
            self._body[pos] = oldbody[oldpos]
            oldbody[oldpos] = None
            pos += 1
            oldpos = (oldpos + 1) % oldlength
        self._front = 0
        self._tail = self._size


def main():
    testqueue = FeedbackQueue(1)
    for i in range(50):
        testqueue.add(i)
    for i in range(51):
        testqueue.remove()
    testqueue.add("A")


if __name__ == "__main__":
    main()
