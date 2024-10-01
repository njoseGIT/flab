from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_StopStirring'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_StopStirring',
        'long_name': 'Stops stirring on IkaRCTDigital ',
        'description': 'Stops stirring on IkaRCTDigital.',
        'parameters': {}
    }

    def run(self):
        try:
            self.flab.display(f'Setting IkaRCTDigital temperature to: {speed}', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]
            if ika.get('is_connected'):
                ika.stop_stirring()
            else:
                self.flab.display('Cannot start stirring. IkaRCTDigital is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
