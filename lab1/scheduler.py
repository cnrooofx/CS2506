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
            cur_quantum = self._base_quantum
            out = ""
            for queue in self._ready_queues:
                if queue.first:
                    process = queue.remove()
                    quantum = queue.get_quantum()
                    cur_quantum, out = self._exec_handler(process, quantum)
                    break
            
            if len(self._blocked_queue) != 0:
                # If there are processes in the blocked queue, run them
                self._blocked_handler(cur_quantum)

            if out == "":
                out = "Idle"
                if idle_count > 100:
                    print("--- Execution Finished ---")
                    break
                idle_count += 1
            else:
                idle_count = 0

            q += cur_quantum
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
                out += "\n`----> Has IO for {} quanta".format(io_time)
            self._ready_queues[priority].add(process)
            print(out)
    
    def _exec_handler(self, process, quantum):
        """Execute the process, then put it into the appropriate queue.

        Args:
            process (Process object): Process to be executed
            quantum (int): The time quantum of the current queue
        
        Returns:
            exec_time (int): The time it took to execute the process
            out (str): Description of state of the process after execution
        """
        out = "Process {} ".format(process.get_name())
        time_remaining = process.get_exec_time()
        if process.has_io():
            out += "has IO, moving to blocked queue"
            process.increase_priority()
            self._blocked_queue.append(process)
            exec_time = self._base_quantum
        elif time_remaining > quantum:
            exec_time = quantum
            process.execute(exec_time)
            priority = process.get_priority()
            if priority < self._num_queues-1:
                process.decrease_priority()
                new_priority = process.get_priority()
                self._ready_queues[new_priority].add(process)
                out += "didn't finish, moving to priority {}".format(
                    new_priority)
            else:
                self._ready_queues[-1].add(process)
                out += "didn't finish, staying at lowest priority"
        else:
            exec_time = time_remaining
            process.execute(exec_time)
            out += "has finished execution"
        return exec_time, out
    
    def _blocked_handler(self, quantum):
        """
        """
        for process in self._blocked_queue:
            exec_status = process.io_operation(quantum)
            # If the IO has finished, move it back to ready queue
            if exec_status:
                self._ready_queues[process.get_priority()].add(process)
                self._blocked_queue.remove(process)


def main():
    sched = Scheduler(base_quantum=2, num_queues=8)
    
    process_a = Process("A", 3, 20)
    process_b = Process("B", 7, 20)
    process_c = Process("C", 0, 30)
    process_d = Process("D", 1, 5, True, 250)
    process_e = Process("E", 6, 100)

    process_f = Process("F", 3, 20)
    process_g = Process("G", 2, 54, True, 250)
    process_h = Process("H", 0, 30)

    processes = [process_a, process_b, process_c, process_d,
                 process_e, process_f, process_g, process_h]

    sched.add_processes(processes)
    sched.run()


if __name__ == "__main__":
    main()
