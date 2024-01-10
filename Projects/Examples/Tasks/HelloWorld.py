#Import the required libraries
import time

#Import the task template from flab.Templates
from flab3.Templates import TaskTemplate

#Create the Task class, inheriting TaskTemplate.Task
class Task(TaskTemplate.Task):

    #Define the name of the task. This should match the filename
    task_name = 'HelloWorld'

    #Define the type of the task. This is either 'thread' , 'process' or 'asyncio'
    task_type = 'thread'

    #Define the descriptions of each argument being entered into the task (optional)
    argument_descriptions = {'optional_argument': 'an optional argument',
                             'mandatory_argument': 'a mandatory argument'}

    #define the run method, with any necessary and optional arguments (i.e. args, kwargs)
    def run(self, mandatory_argument, optional_argument = 'optional argument'):
        try:

            #print out Hello World + the mandatory argument in the system command line/terminal
            print('1. Hello World: ' + str(mandatory_argument))

            #display Hello World + the mandatory argument in the console command line
            self.flab.display('2. Hello World: ' + str(mandatory_argument) + ' ' + str(optional_argument))

            #create a shared variable called 'World' with the value 'Hello'
            self.flab.add_var('Hello', 'World')

            #display the shared variable called 'World' in the console command line
            self.flab.vars['count'] = 0
            self.flab.display('3. ' + str(self.flab.vars['count']))

            #create a shared variable called 'HelloWorld_stopped' with the value False
            self.flab.vars['HelloWorld_stopped'] = False

            #while the variable 'HelloWorld_stopped' is False, loop over a section of code
            while not self.flab.vars['HelloWorld_stopped']:
                #display 'Hello World' + mandatory argument in the console
                self.flab.display('4. Hello World: ' + str(mandatory_argument))
                #sleep for a second
                time.sleep(1)
        except Exception as e:
            self.flab.display('Error in HelloWorld')
            self.flab.display(e)
        finally:
            pass

    #define the method to be called when the task is stopped
    def stop(self):
        #set the variable 'HelloWorld_stopped' to True
        self.flab.vars['HelloWorld_stopped'] = True #a flag to stop the script
