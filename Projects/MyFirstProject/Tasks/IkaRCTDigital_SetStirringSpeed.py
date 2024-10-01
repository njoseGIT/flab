from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_SetStirringSpeed'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_SetStirringSpeed',
        'long_name': 'Sets stirring speed setpoint of IkaRCTDigital ',
        'description': 'Sets stirring speed setpoint of IkaRCTDigital ',
        'parameters': {
            'speed': {
                'description': 'the stirring speed setpoint',
                'unit': 'RPM',
                'type': 'integer',
            }
        }
    }

    def run(self, speed=0):
        try:
            self.flab.display(f'Setting IkaRCTDigital temperature to: {speed}', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]
            if ika.get('is_connected'):
                ika.set_stirring_speed(rpm=float(speed))
            else:
                self.flab.display('Cannot set stirring speed. IkaRCTDigital is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
