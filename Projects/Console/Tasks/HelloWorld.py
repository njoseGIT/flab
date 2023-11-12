import time

#A scratch class
class Task():

    task_name = 'HelloWorld'
    task_type = 'thread'
    task_stopped = False

    def __init__(self,flab):
        self.flab = flab

    def run(self):
        self.task_stopped = False
        self.flab.display('Hello World')
        while True:
            self.flab.display('Hello World')
            time.sleep(1)

    def stop(self):
        self.flab.tasks['HelloWorld'].task_stopped = True #a flag to stop the script
