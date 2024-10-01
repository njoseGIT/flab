from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'HarvardPump33DDS_Initialize'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'HarvardPump33DDS_Initialize',
        'long_name': 'Initializes the IKA RCT Digital Hotplate',
        'description': 'Initializes IKA RCT Digital program variables',
        'parameters': {}
    }

    def run(self):
        try:
            vars = {'HarvardPump33DDS_is_connected': False, # Indicates if the K1 is connected. To be changed to k1start_is_connected
                            'HarvardPump33DDS_is_running': False, # Indicates if the Vapourtec is running a reaction.
                            'HarvardPump33DDS_status': '' # The current status of the vapourtec
                            }
            self.flab.vars['user_task_names'] += ['HarvardPump33DDS_Connect',
                                                  'HarvardPump33DDS_Disconnect',
                                                  'HarvardPump33DDS_StartInfusing',
                                                  'HarvardPump33DDS_StopPumping']

            self.flab.vars['user_device_names'] += ['HarvardPump33DDS']

            self.flab.vars.update(vars)

            user_variables_to_add = {}

            for v in user_variables_to_add:
                self.flab.start_task('AddVariable',
                                     v,
                                     user_variables_to_add[v]['description'],
                                     user_variables_to_add[v]['unit'],
                                     variable_type =  user_variables_to_add[v]['variable_type'],
                                     value =  user_variables_to_add[v]['value'],
                                     blocking= True)

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
