#Console2FlabProcess.py
#A task for running flab in Console 2
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

class Task():
    task_name = 'ConsoleFlabProcess'
    task_type = 'process'

    def __init__(self, flab):
        self.flab = flab

    #method called when process is running
    def run(self, flab, in_queue, out_queue):
        try:
            self.flab = flab
            self.in_queue = in_queue
            self.out_queue = out_queue
            while self.flab.is_running:
                command = self.in_queue.get(block=True)
                try:
                    if command == 'close':
                        self.flab.is_running = False
                    elif command != '':
                        if command[0:6] == 'start ':
                            task_info = command[6:]
                            eval('self.flab.start_task("' + task_info +'")')
                        elif command[0:7] == 'rstart ':
                            task_info = command[7:]
                            eval('self.flab.reload_start_task("' + task_info +'")')
                        elif command[0:5] == 'stop ':
                            task_info = command[5:]
                            eval('self.flab.stop_task("' + task_info +'")')
                        else:
                            eval('self.flab.' + command)
                    else:
                        pass
                except Exception as e:
                    self.out_queue.put(str(e))
                    self.out_queue.put('error in flab command')

        except Exception as e:
            self.flab.display('Error in ConsoleFlabProcess')
            self.flab.display(e)






