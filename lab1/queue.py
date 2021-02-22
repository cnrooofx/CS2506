"""Multi-level Feedback Queue.

Script Name: queue.py
Author: Conor Fox 119322236
"""

class Queue:
    def __init__(self):
        """Initialise the queue."""
        self._body = [None] * 10
        self._front = 0
        self._size = 0
    
    def __str__(self):
        output = '<-'
        if self._size > 0:
            i = self._front
            for _ in range(self._size):
                output += str(self._body[i]) + '-'
                i = (i + 1) % len(self._body)
        output += '<' + '     '
        return output

    def enqueue(self, item):
        """Add an item to the queue."""
        if self._size == 0:
            self._body[0] = item  # assumes an empty queue has head at 0
            self._size = 1
        else:
            self._body[(self._front + self._size) % len(self._body)] = item
            self._size += 1
            if self._size == len(self._body):
                self.__requeue()

    def dequeue(self):
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
        if (self._size / len(self._body)) < 0.25:
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
    
    def __requeue(self):
        """Grow/shrink the internal representation of the queue."""
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
