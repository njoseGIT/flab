import time

#A class for running the main flab process
class Task():
    taskname = 'ConsoleFlabProcess'
    task_type = 'process'

    def __init__(self, flab):
        self.flab = flab

    #method called when process is running
    def run(self, flab, in_queue, out_queue):
        self.flab = flab
        self.in_queue = in_queue
        self.out_queue = out_queue
        while self.flab.is_running:
            command = self.in_queue.get(block=True)
            try:
                if command == 'close':
                    self.flab.is_running = False
                else:
                    eval('self.flab.' + command)
            except Exception as e:
                self.out_queue.put(str(e))
                self.out_queue.put('error in flab command')






