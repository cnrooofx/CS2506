"""Queue ADT.

Script Name: queue.py
Author: Conor Fox 119322236
"""

class Queue:
    """A First-In, First-Out Queue."""

    def __init__(self):
        """Initialise the queue."""
        self._body = [None] * 10
        self._front = 0
        self._size = 0

    def add(self, item):
        """Add item to the queue."""
        if self._size == 0:
            self._body[0] = item
            self._size = 1
        else:
            self._body[(self._front + self._size) % len(self._body)] = item
            self._size += 1
            if self._size == len(self._body):
                self.__requeue()

    def remove(self):
        """Remove and return the item in the queue for longest."""
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

    def length(self):
        """Return the number of items in the queue."""
        return self._size

    def first(self):
        """Return the first item in the queue."""
        if self._size == 0:
            return None
        return self._body[self._front]

    def __requeue(self):
        """Grow and shrink the internal queue to save space."""
        oldbody = self._body
        oldlength = len(self._body)
        self._body = [None] * (2 * self._size)
        oldpos = self._front
        pos = 0
        for _ in range(self._size):
            self._body[pos] = oldbody[oldpos]
            oldbody[oldpos] = None
            pos += 1
            oldpos = (oldpos + 1) % oldlength
        self._front = 0
        self._tail = self._size
