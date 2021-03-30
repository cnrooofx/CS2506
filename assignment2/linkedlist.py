
class LinkedList:
    def __init__(self):
        self._head = ListNode(None, None, None)
        self._tail = ListNode(None, self._head, None)
        self._head.next = self._tail
        self._selected = None
        self._length = 0

    def length(self):
        return self._length

    def add(self, track):
        self._add_node(track, self._tail.prev)

    def get_selected(self):
        if self._selected is None:
            return None
        return self._selected.item

    def next(self):
        if self._selected is not None:
            if self._selected.next is self._tail:
                self._selected = self._head.next
            else:
                self._selected = self._selected.next

    def prev(self):
        if self._selected is not None:
            if self._selected.prev is self._head:
                self._selected = self._tail.prev
            else:
                self._selected = self._selected.prev

    def reset(self):
        if self._length != 0:
            self._selected = self._head.next

    def remove_current(self):
        if self._selected is not None:
            previous = self._selected.prev
            next_node = self._selected.next

            previous.next = next_node
            next_node.prev = previous

            self._selected.item = None
            self._selected.next = None
            self._selected.prev = None

            self._length -= 1
            if self._length == 0:
                self._selected = None
            elif next_node is self._tail:
                self._selected = previous
            else:
                self._selected = next_node

    def _add_node(self, track, previous):
        new_node = ListNode(track, None, None)
        next_node = previous.next

        new_node.next = next_node
        next_node.prev = new_node
        previous.next = new_node
        new_node.prev = previous

        if self._length == 0:
            self._selected = new_node
        self._length += 1


class ListNode:
    def __init__(self, item, prevnode, nextnode):
        self.item = item
        self.next = nextnode
        self.prev = prevnode
