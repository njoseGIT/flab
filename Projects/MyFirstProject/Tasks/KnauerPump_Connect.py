from flab.Templates import TaskTemplate


class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_Connect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_Connect',
        'long_name': 'Connect to KnauerPump System',
        'description': 'Establish a connection to the KnauerPump.',
        'parmaeters': {}
    }

    def run(self):
        try:
            self.flab.display('Connecting to the KnauerPump', output_list = 'output_queue')
            device = self.flab.devices["KnauerPump"]

            if device.get('is_connected'):
                self.flab.display("Error: already connected to the KnauerPump.", output_list = 'output_queue')

            else:
                device.connect()
                if device.get('is_connected'):
                    self.flab.display('Successfully connected to the KnauerPump', output_list='output_queue')
                else:
                    self.flab.display("Error: could not connect to the KnauerPump.", output_list='output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
