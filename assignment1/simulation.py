"""Run a simulation of the Multi-Feedback Queue Scheduling algorithm.

Script Name: simulation.py
Author: Conor Fox 119322236
"""

from scheduler import Scheduler
from process import Process


class Simulation:
    def __init__(self, base_quantum, num_queues, processes):
        """Initialise the simulation.

        Args:
            base_quantum (int): Base quantum of the CPU
            num_queues (int): Number of queues to create
            processes (list): List of Process objects to add to the scheduler
        """
        self._scheduler = Scheduler(base_quantum, num_queues)
        self.add_processes(processes)
    
    def add_processes(self, processes):
        """Loop over the input processes and put them in the correct queues.
        
        Args:
            processes (list): List of Process objects to run
        """
        print("Processes\n" + "-" * 25)
        for process in processes:
            name = process.get_name()
            priority = process.get_priority()
            out = "Process {} - Priority: {}".format(name, priority)
            if process.has_io():
                io_time = process.get_io_time()
                out += "\n`----> Has IO for {} quanta".format(io_time)
            self._scheduler.add_process(process, priority)
            print(out)
    
    def start(self):
        """Start the simulation."""
        self._scheduler.run()


def main():
    process_a = Process("A", 3, 20)
    process_b = Process("B", 7, 340)
    process_c = Process("C", 0, 12)
    process_d = Process("D", 1, 50, True, 600)
    process_e = Process("E", 6, 100)
    process_f = Process("F", 3, 20)
    process_g = Process("G", 2, 54, True, 350)
    process_h = Process("H", 0, 30)

    processes = [process_a, process_b, process_c, process_d,
                 process_e, process_f, process_g, process_h]

    sim = Simulation(5, 8, processes)
    sim.start()


if __name__ == "__main__":
    main()
