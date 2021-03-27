
class Page:

    def __init__(self, page_size):
        self._size = page_size
        self._allocated = False
    
    def __str__(self):
        return "Page Size: {} - Allocated: {}".format(self._size, self._allocated)
    
    def allocate(self):
        self._allocated = True
    
    def deallocate(self):
        self._allocated = False
