from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'IkaRCTDigital_Disconnect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'IkaRCTDigital_Disconnect',
        'long_name': 'Disconnect IKA RCT Digital hotplate',
        'description': 'Establishes serial connection to IkaRCTDigital ',
        'parameters': {},
        }

    def run(self, temperature=''):
        try:
            self.flab.display(f'Disconnecting IKA RCT Digital hotplate', output_list='output_queue')
            ika = self.flab.devices["IkaRCTDigital"]
            ika.disconnect()
            if not ika.get('is_connected'):
                self.flab.display('IkaRCTDigital successfully discconnected', output_list = 'output_queue')
            else:
                self.flab.display('IkaRCTDigital unsuccessfully disconnected. Check connection.', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True