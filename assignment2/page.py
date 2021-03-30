"""Memory Page.

Script Name: page.py
Author: Conor Fox 119322236
"""

class Page:
    """A Page of Memory."""

    def __init__(self, page_size):
        """Initialise a new page."""
        self._size = page_size
        self._accessed = False

    def __str__(self):
        return "Page Size: {} - Accessed: {}".format(self._size, self._allocated)
    
    def acess_bit(self):
        """Return whether the page has been accessed."""
        return self._accessed

    def access(self):
        """Access the page."""
        self._accessed = True

    def reset_access(self):
        """Reset the accessed indicator."""
        self._accessed = False
