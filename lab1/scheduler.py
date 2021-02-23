"""Class to implement a Multi-Feedback Process Scheduler.

Script Name: scheduler.py
Author: Conor Fox 119322236
"""

from queue import FeedbackQueue
from process import Process


class Scheduler:
    def __init__(self, base_quantum, num_queues=8):
        """Initialise the scheduler with the specified number of queues.

        Args:
            base_quantum (int): Base quantum of the CPU in miliseconds
            num_queues (int): Number of queues to create (Default: 8)
        """
        self._base_quantum = base_quantum
        self._num_queues = num_queues
        self._ready_queues = []
        self._blocked_queue = []
        for i in range(self._num_queues):
            quantum = (2 ** i) * self._base_quantum
            self._ready_queues.append(FeedbackQueue(quantum))

    def run(self):
        """Simulate the running of a series of processes."""
        print("-" * 25 + "\nRunning\n" + "-" * 25)
        q = 0
        idle_count = 0
        while q < 10000:
            exec_time = self._base_quantum
            out = ""
            for priority, queue in enumerate(self._ready_queues):
                if queue.first:
                    process = queue.remove()
                    out = "Process {} ".format(process.get_name())
                    if process.has_io():
                        out += "has IO, moving to blocked queue"
                        self._blocked_queue.append(process)
                    else:
                        exec_time = queue.get_quantum()
                        time_remaining = process.exec_remaining()
                        if time_remaining > exec_time:
                            process.execute(exec_time)
                            if priority < self._num_queues-1:
                                process.decrease_priority()
                                new_priority = process.get_priority()
                                self._ready_queues[new_priority].add(process)
                                out += "didn't finish, moving to priority {}".format(new_priority)
                            else:
                                self._ready_queues[-1].add(process)
                                out += "didn't finish, staying at lowest priority"
                        else:
                            exec_time = time_remaining
                            process.execute(exec_time)
                            out += "has finished execution"
                    break
            
            if len(self._blocked_queue) != 0:
                for process in self._blocked_queue:
                    exec_status = process.io_operation(exec_time)
                    if exec_status:
                        process.increase_priority()
                        self._ready_queues[process.get_priority()].add(process)
                        self._blocked_queue.remove(process)

            if out == "":
                out = "Idle"
                if idle_count > 100:
                    print("--- Execution Finished ---")
                    break
                else:
                    idle_count += 1
            else:
                idle_count = 0

            q += exec_time
            print("[q{}] - {}".format(q, out))
        
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
                out += "\n|___ Has IO for {} quanta".format(io_time)
            self._ready_queues[priority].add(process)
            print(out)


def main():
    sched = Scheduler(base_quantum=2, num_queues=8)
    
    process_a = Process("A", 3, 20)
    process_b = Process("B", 7, 20)
    process_c = Process("C", 0, 30)
    process_d = Process("D", 1, 5, True, 250)
    process_e = Process("E", 6, 100)
    # processes = [processA]
    processes = [process_a, process_b, process_c, process_d, process_e]

    # for i, item in enumerate(processes):
    #     print(i, item.get_name())
    sched.add_processes(processes)
    sched.run()


if __name__ == "__main__":
    main()
