from flab3.Templates import TaskTemplate
import asyncio

class Task(TaskTemplate.Task):

    task_name = 'HelloWorld_asyncio'
    task_type = 'asyncio'
    task_stopped = False
    argument_descriptions = {'optional_argument': 'an optional argument', 'mandatory_argument': 'a mandatory argument'}

    async def run(self):
        try:
            self.flab.vars['HelloWorld_asyncio_stopped'] = False # a flag to stop the script
            # loop the display of 'Hello World' until the user stops the task.
            while not self.flab.vars['HelloWorld_asyncio_stopped']:
                self.flab.display('Hello World')
                await asyncio.sleep(1)
        except Exception as e:
            self.flab.display('Error in ' + self.task_name)
            self.flab.display(e)

    async def stop(self):
        self.flab.vars['HelloWorld_asyncio_stopped'] = True #a flag to stop the script
        self.flab.display('HelloWorld_asyncio stopped')
