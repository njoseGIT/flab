#Import the required libraries
import time

#Import the task template from flab.Templates
from flab3.Templates import TaskTemplate

#Create the Task class, inheriting TaskTemplate.Task
class Task(TaskTemplate.Task):

    #Define the name of the task. This should match the filename
    task_name = 'Count'

    #Define the type of the task. This is either 'thread' , 'process' or 'asyncio'
    task_type = 'thread'

    #define the run method, with any necessary and optional arguments (i.e. args, kwargs)
    def run(self):
        try:
            #create a variable called 'Count_stopped'. This is a flag to stop the task.
            self.flab.vars['Count_stopped'] = False

            #create a variable called 'count'
            self.flab.vars['count'] = 0

            #create a list called 'count_list'
            self.flab.vars['count_list'] = [0]

            #start a loop that increases the count every second
            while not self.flab.vars['Count_stopped']:
                # increase the count by 1
                self.flab.vars['count'] += 1

                # append the new count to the list
                self.flab.vars['count_list'] = self.flab.vars['count_list'] + [self.flab.vars['count']]

                #sleep for one second
                time.sleep(1)

        except Exception as e:
            self.flab.display('Error in ' + self.task_name)
            self.flab.display(e)

        finally:

            pass

    #define the method to be called when the task is stopped
    def stop(self):
        #set the variable 'Count_stopped' to True
        self.flab.vars['Count_stopped'] = True
