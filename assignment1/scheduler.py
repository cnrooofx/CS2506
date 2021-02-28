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
            base_quantum (int): Base quantum of the CPU
            num_queues (int): Number of queues to create (Default: 8)
        """
        self._base_quantum = base_quantum
        self._num_queues = num_queues
        self._ready_queues = []
        self._blocked_queue = Queue()

        for i in range(self._num_queues):
            quantum = (2 ** i) * self._base_quantum
            self._ready_queues.append(FeedbackQueue(quantum))
    
    def add_process(self, process, priority):
        """Add the process at the specified priority.
        
        Args:
            process (Process object): Process to add to scheduler
            priority (int): The priority of the process
        """
        self._ready_queues[priority].add(process)

    def run(self):
        """Run the scheduling algorithm."""
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
                    if process.has_io():
                        out = "Process {} ".format(process.get_name())
                        out += "has IO, moving to blocked queue"
                        process.increase_priority()
                        self._blocked_queue.add(process)
                        cur_quantum = 0
                    else:
                        cur_quantum, out = self._exec_handler(process, quantum)
                    break
            
            if self._blocked_queue.length != 0:
                # If there are processes in the blocked queue, run them
                outcome = self._blocked_handler(cur_quantum)
                if outcome and not out:
                    out += outcome
                elif outcome and out:
                    out += "\n\t" + outcome

            # Cut off the scheduler if it's idle for too long
            if out == "":
                out = "Idle"
                if idle_count > 25:
                    print("--- Execution Finished ---")
                    break
                idle_count += 1
            else:
                idle_count = 0

            q += cur_quantum
            print("[q{}] - {}".format(q, out))
    
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
        if time_remaining > quantum:
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
        """Check if IO operation has finished and move process back to ready.

        Args:
            quantum (int): The current value of CPU quantum
        """
        for i in range(self._blocked_queue.length):
            process = self._blocked_queue.remove()
            exec_status = process.io_operation(quantum)
            # If the IO has finished, move it back to ready queue
            if exec_status:
                name = process.get_name()
                out = "IO for Process {} finished".format(name)
                priority = process.get_priority()
                out += ", returning at priority {}".format(priority)
                self._ready_queues[process.get_priority()].add(process)
                return out
            self._blocked_queue.add(process)
