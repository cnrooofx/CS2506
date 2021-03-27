from bst import BinaryTree
from block import Block


class Kernel:
    """Kernel Memory Management process."""

    def __init__(self, page_size, memory_blocks):
        self._page_size = page_size
        self._free = BinaryTree()
        self._fill_memory(memory_blocks)
    
    def request_block(self, size):
        """Request a block of the specified size.

        Returns:
            A block or None if there is no free block of the right size.
        """
        return self._free.remove(Block(size))

    def _fill_memory(self, memory_blocks):
        for count, num_pages in memory_blocks:
            for _ in range(count):
                new_block = Block(num_pages, self._page_size)
                self._free.add(new_block)
