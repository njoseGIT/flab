from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_SetFlowrate'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_SetFlowrate',
        'long_name': 'Sets flowrate setpoint of KnauerPump ',
        'description': 'Sets flowrate setpoint of KnauerPump ',
        'parameters': {
            'flowrate': {
                'description': 'The flowrate setpoint. Please note that only three decimal points are allowed.',
                'unit': 'uL/min',
                'type': 'int',
                'default': 0,
            },
        }
    }

    def run(self, flowrate=0):
        try:
            self.flab.display(f'Setting KnauerPump flowrate to: {flowrate}', output_list='output_queue')
            kp = self.flab.devices["KnauerPump"]
            if kp.get('is_connected'):
                kp.set_flowrate(flowrate=flowrate)
            else:
                self.flab.display('Cannot set flowrate. KnauerPump is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
