from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_Initialize'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_Initialize',
        'long_name': 'Initializes the IKA RCT Digital Hotplate',
        'description': 'Initializes IKA RCT Digital program variables',
        'parameters': {}
    }

    def run(self):
        try:
            vapourtec_vars = {'IkaRCTDigital_is_connected': False, # Indicates if the K1 is connected. To be changed to k1start_is_connected
                            'IkaRCTDigital_is_running': False, # Indicates if the Vapourtec is running a reaction.
                            'IkaRCTDigital_status': '' # The current status of the vapourtec
                            }
            self.flab.vars['user_task_names'] += ['IkaRCTDigital_Connect',
                                                  'IkaRCTDigital_Disconnect',
                                                  'IkaRCTDigital_SetTemperature',
                                                  'IkaRCTDigital_SetStirringSpeed',
                                                  'IkaRCTDigital_StartHeater',
                                                  'IkaRCTDigital_StartStirring',
                                                  'IkaRCTDigital_StopHeater',
                                                  'IkaRCTDigital_StopStirring',
                                                  'IkaRCTDigital_StartHeatingAndStirring',
                                                  'IkaRCTDigital_StartMeasurements']
                                                  #'IkaRCTDigital_TemperatureRamp',
                                                  #'IkaRCTDigital_TemperatureSoak']
            self.flab.vars.update(vapourtec_vars)
            self.flab.vars['user_device_names'] += ['IkaRCTDigital']

            user_variables_to_add = \
            {
            'IkaRCTDigital_measurement_interval': {
                'description': 'Frequency of IkaRCTDigital measurements in seconds.',
                'unit': 'seconds',
                'variable_type': 'numeric',
                'value': -1,
            },
            'IkaRCTDigital_external_temperature_measured': {
                'description': 'Measured temperature from IkaRCTDigital external temperature sensor. Value = -1 if not operational or in error state..',
                'unit': 'bar',
                'variable_type': 'float',
                'value': -1,

            },
            'IkaRCTDigital_plate_temperature_measured': {
                'description': 'Measured temperature from IkaRCTDigital plate temperature sensor. Value = -1 if not operational or in error state..',
                'unit': 'bar',
                'variable_type': 'float',
                'value': -1,
            },
            'IkaRCTDigital_temperature_setpoint': {
                'description': 'IkaRCTDigital temperature setpoint. Value = -1 if not operational or in error state..',
                'unit': 'bar',
                'variable_type': 'float',
                'value': -1,
            },
            'IkaRCTDigital_stirring_speed_measured': {
                'description': 'Measured stirring speed from IkaRCTDigital. Value = -1 if not operational or in error state..',
                'unit': 'bar',
                'variable_type': 'float',
                'value': -1,
            },
            'IkaRCTDigital_stirring_speed_setpoint': {
                'description': 'IkaRCTDigital stirring speed setpoint. Value = -1 if not operational or in error state..',
                'unit': 'bar',
                'variable_type': 'float',
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
