from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_SetTemperature'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_SetTemperature',
        'long_name': 'Sets temperature setpoint of IkaRCTDigital ',
        'description': 'Sets temperature setpoint of IkaRCTDigital ',
        'parameters': {
            'temperature': {
                'description': 'the setpoint',
                'unit': 'Celsius',
                'type': 'float',
            }
        }
    }

    def run(self, temperature=''):
        try:
            self.flab.display(f'Setting IkaRCTDigital temperature to: {temperature}', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]

            if ika.get('is_connected'):
                ika.set_temperature(temperature=float(temperature))
            else:
                self.flab.display('Cannot set temperature. IkaRCTDigital is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
