from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_Initialize'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_Initialize',
        'long_name': 'Initialize KnauerPump',
        'description': 'Initializes KnauerPump program variables',
        'parameters': {}
    }

    def run(self):
        try:
            vars = {'KnauerPump_is_connected': False, # Indicates if the KnauerPump is connected.
                    'KnauerPump_is_running': False, # Indicates if the KnauerPump is running a reaction.
                    'KnauerPump_status': '', # The current status of the KnauerPump,
                    'KnauerPump_stop_timed_pump': False
                    }
            self.flab.vars['user_task_names'] += ['KnauerPump_Connect',
                                                  'KnauerPump_Disconnect',
                                                  'KnauerPump_DoseVolume',
                                                  'KnauerPump_ReadFlowrateSetpoint',
                                                  'KnauerPump_SetFlowrate',
                                                  'KnauerPump_StartPumping',
                                                  'KnauerPump_StartTimedPump',
                                                  'KnauerPump_StopPumping']
            self.flab.vars['user_device_names'] += ['KnauerPump']
            self.flab.vars.update(vars)

            user_variables_to_add = \
            {
            'Vapourtec_measurement_interval': {
                'description': 'Frequency of measurements in seconds.',
                'unit': 'seconds',
                'variable_type': 'numeric',
                'value': -1,
            },
            }

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
