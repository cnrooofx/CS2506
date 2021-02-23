"""Class to represent a Process to be executed.

Script Name: process.py
Author: Conor Fox 119322236
"""

class Process:
    """A Process to be executed by a scheduler."""

    def __init__(self, name, priority, exec_time, io=False, io_duration=0):
        """Initialise a new Process.

        Args:
            name (str): The name of the process
            priority (int): Value for the process priority
            exec_time (int): Value for the process execution time
            io (bool): True if the process has IO operations
            io_duration (int): Amount of IO time
        """
        self._name = name
        self._priority = priority
        self._exec_time = exec_time
        self._io = io
        self._io_time = io_duration
    
    def get_name(self):
        """Return the name of the process."""
        return self._name
    
    def get_priority(self):
        """Return the current priority of the process."""
        return self._priority
    
    def set_priority(self, priority):
        """Update the priority to the specified value."""
        self._priority = priority
    
    def increase_priority(self):
        """Increase the priority of the process by 1."""
        if self._priority > 0:
            self._priority -= 1
    
    def decrease_priority(self):
        """Decrease the priority of the process by 1."""
        self._priority += 1
    
    def has_io(self):
        """Return True if the process has IO operations, otherwise False."""
        return self._io
    
    def get_io_time(self):
        """Return the remaining time for IO operations."""
        return self._io_time
    
    def execute(self, time):
        """Execute the process and update the execution time.

        Returns:
            True if the process has completed, otherwise False
        """
        self._exec_time -= time
    
    def get_exec_time(self):
        """Return the remaining execution time left."""
        return self._exec_time
    
    def io_operation(self, time):
        """Execute the IO operation.
        
        Returns:
            True if the IO has finished, otherwise False"""
        self._io_time -= time
        if self._io_time <= 0:
            self._io = False
            return True
        return False
