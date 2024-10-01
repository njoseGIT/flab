from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):

    task_name = 'HelloWorldDeviceTask'
    task_type = 'thread'

    def run(self):
        """
        An example task which shows the functionality of flab device classes.

        :returns: None
        """
        try:
            self.flab.display('Using device method')
            self.flab.devices['HelloWorldDevice'].display_hello_world()

            self.flab.display('Getting device attribute')
            x = self.flab.devices['HelloWorldDevice'].get('hello')
            self.flab.display(x)

            self.flab.display('Setting device attribute')
            self.flab.devices['HelloWorldDevice'].set('hello','goodbye')
            self.flab.display(self.flab.devices['HelloWorldDevice'].get('hello'))

        except Exception as e:
            self.flab.display('Error in ' + self.task_name)
            self.flab.display(str(e))

        finally:
            pass

    def stop(self):
        self.flab.vars['DataTestTask_stopped'] = True #a flag to stop the script. This is unused in this example.