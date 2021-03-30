from linkedlist import LinkedList
from queue import Queue
from block import Block
from request import Request

"""Kernel Memory Manager.

Script Name: kernel.py
Author: Conor Fox 119322236
"""

class Kernel:
    """Kernel Memory Management process."""

    def __init__(self, page_size, memory_blocks):
        self._page_size = page_size
        self._free = LinkedList()
        self._fill_memory(memory_blocks)
        self._allocated = Queue()

    def allocation(self, requests):
        """First-Fit Memory Allocation."""
        for request in requests:
            request_size = request.get_size()
            pid = request.get_pid()
            print("Process {} - Requesting {} kB".format(pid, request_size))

            block_size = self._free.get_selected().get_size()
            while block_size < request_size:
                self._free.next()
                block_size = self._free.get_selected().get_size()
            print("|--> Allocating block of size {} kB".format(block_size))
            block = self._free.get_selected()
            self._free.remove_current()
            self._allocated.add(block)
            self._free.reset()

    def page_replacement(self):
        length = self._allocated.length()
        while length > 0:
            block = self._allocated.remove()
            for page in block._pages:
                if page.access_bit() == False:
                    print("Swapping page")
                else:
                    page.reset_access()
            length -= 1

    def _fill_memory(self, memory_blocks):
        for count, num_pages in memory_blocks:
            for _ in range(count):
                new_block = Block(num_pages, self._page_size)
                self._free.add(new_block)


def main():
    blocks = [(32, 2), (16, 4), (16, 8), (16, 16), (16, 32)]
    page_size = 4

    k = Kernel(page_size, blocks)
    
    r1 = Request(1, 20)
    r2 = Request(2, 100)
    r3 = Request(3, 128)
    r4 = Request(4, 45)
    r5 = Request(5, 60)
    r6 = Request(6, 10)
    r7 = Request(7, 2)
    r8 = Request(8, 59)

    requests = [r1, r2, r3, r4, r5, r6, r7, r8]

    k.allocation(requests)


if __name__ == "__main__":
    main()
