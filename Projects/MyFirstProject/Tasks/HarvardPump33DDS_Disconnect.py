from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):

    task_name = 'HarvardPump33DDS_Disconnect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'HarvardPump33DDS_Disconnect',
        'long_name': 'Disconnect from HarvardPump33DDS System',
        'description': 'Safely disconnects from the HarvardPump33DDS.',
        'parameters': {}
    }

    def run(self):
        try:
            hp = self.flab.devices["HarvardPump33DDS"]

            if hp.is_connected == False:
                self.flab.display("Error: HarvardPump33DDS is not connected.", output_list = 'output_queue')

            else:
                hp.disconnect()
                if not hp.get('is_connected'):
                    self.flab.display("Successfully disconnected from the HarvardPump33DDS system.", output_list = 'output_queue')
                else:
                    self.flab.display("Failed to disconnect from the HarvardPump33DDS system. Try again", output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
