from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_StartStirring'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_StartStirring',
        'long_name': 'Starts stirring on IkaRCTDigital ',
        'description': 'Starts stirring on IkaRCTDigital according to the current setpoint.',
        'parameters': {}
    }

    def run(self, speed=0):
        try:
            self.flab.display(f'Setting IkaRCTDigital temperature to: {speed}', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]
            if ika.get('is_connected'):
                ika.start_stirring()
            else:
                self.flab.display('Cannot start stirring. IkaRCTDigital is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
