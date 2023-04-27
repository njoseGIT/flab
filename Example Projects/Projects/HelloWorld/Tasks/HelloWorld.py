import time

class Task():

    task_name = 'HelloWorld'
    task_type = 'thread'
    task_stopped = False
    argument_descriptions = {'optional_argument': 'an optional argument', 'mandatory_argument': 'a mandatory argument'}

    def __init__(self, flab):
        self.flab = flab

    def run(self, mandatory_argument, optional_argument = 'optional argument'):
        print(mandatory_argument)
        self.flab.add_var('Hello', 'World')
        self.task_stopped = False
        self.flab.display('Hello World')
        self.flab.display(self.flab.vars['World'])

        while True:
            self.flab.display('Hello')
            time.sleep(1)

    def stop(self):
        self.flab.tasks['HelloWorld'].task_stopped = True #a flag to stop the script
