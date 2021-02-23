"""Class to implement a Multi-Feedback Process Scheduler.

Script Name: scheduler.py
Author: Conor Fox 119322236
"""

from queue import Queue, FeedbackQueue
from process import Process


class Scheduler:
    def __init__(self, base_quantum, num_queues=8):
        """Initialise the scheduler with the specified number of queues.

        Args:
            base_quantum (int): Base quantum of the CPU in miliseconds
            base_clock (int): Base CPU clock frequency in MHz
            num_queues (int): Number of queues to create (Default: 8)
        """
        self._base_quantum = base_quantum
        self._blocked_queue = Queue()
        self._ready_queues = []
        for i in range(num_queues):
            quantum = (2 ** i) * self._base_quantum
            self._ready_queues.append(FeedbackQueue(quantum))
    
    def _update_quanta(self, new_quantum):
        """Change the base quantum and update queue time slices accordingly.

        Args:
            new_quantum (int): The base quantum in miliseconds
        """
        self._base_quantum = new_quantum
        for i, current_queue in enumerate(self._ready_queues):
            quantum = (2 ** i) * self._base_quantum
            current_queue.set_quantum(quantum)

    def sleep(self):
        print("Sleeping")

    def run(self, processes):
        """Simulate the running of a series of processes.

        Args:
            processes (list): List of Process objects to run.
        """
        pass


def main():
    example = Scheduler(5)
    example.update_quanta(10)


if __name__ == "__main__":
    main()
