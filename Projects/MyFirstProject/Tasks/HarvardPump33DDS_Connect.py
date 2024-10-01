from flab.Templates import TaskTemplate


class Task(TaskTemplate.Task):
    task_name = 'HarvardPump33DDS_Connect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'HarvardPump33DDS_Connect',
        'long_name': 'Connect to HarvardPump33DS System',
        'description': 'Establish a connection to the HarvardPump33DS.',
    }

    def run(self):
        try:
            self.flab.display('Connecting to the HarvardPump33DDS', output_list = 'output_queue')
            hp = self.flab.devices["HarvardPump33DDS"]

            if hp.get('is_connected'):
                self.flab.display("Error: already connected to the HarvardPump33DDS.", output_list = 'output_queue')

            else:
                hp.connect()
                if hp.get('is_connected'):
                    self.flab.display('Successfully connected to the HarvardPump33DDS', output_list='output_queue')
                else:
                    self.flab.display("Error: could not connect to the HarvardPump33DDS.", output_list='output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
