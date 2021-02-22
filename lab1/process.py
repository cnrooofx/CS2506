"""Class to represent a Process to be executed.

Script Name: process.py
Author: Conor Fox 119322236
"""

class Process:
    def __init__(self, execution_time, priority, io=False, io_duration=0):
        self._priority = priority
        self._exec_time = execution_time
        self._io = io
        self._io_time = io_duration
    
    def get_priority(self):
        """Return the current priority of the process."""
        return self._priority
    
    def set_priority(self, priority):
        """Update the priority to the specified value."""
        self._priority = priority
    
    def increase_priority(self):
        """Increase the priority of the process by 1."""
        self._priority -= 1
    
    def decrease_priority(self):
        """Decrease the priority of the process by 1."""
        self._priority += 1
    
    def execute(self, time):
        """Execute the process and update the execution time.

        Returns True if the process has completed, otherwise False
        """
        self._exec_time -= time
        if self._exec_time <= 0:
            return True
        return False
