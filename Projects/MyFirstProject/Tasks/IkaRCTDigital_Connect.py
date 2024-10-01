from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_Connect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_Connect',
        'long_name': 'Connect IKA RCT Digital hotplate',
        'description': 'Establishes serial connection to IkaRCTDigital ',
        'parameters': {},
        }

    def run(self, temperature=''):
        try:
            self.flab.display(f'Connecting IKA RCT Digital hotplate', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]
            ika.connect()
            if ika.get('is_connected'):
                self.flab.display('IkaRCTDigital successfully connected', output_list = 'output_queue')
            else:
                self.flab.display('IkaRCTDigital unsuccessfully connected. Check connection.', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
