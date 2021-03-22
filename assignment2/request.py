
class Request:
    def __init__(self, pid, size):
        self._pid = pid
        self._size = size

    def get_pid(self):
        return self._pid

    def get_size(self):
        return self._size
