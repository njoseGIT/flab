from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):

    task_name = 'KnauerPump_Disconnect'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_Disconnect',
        'long_name': 'Disconnect from KnauerPump System',
        'description': 'Safely stops and disconnects from the KnauerPump.',
        'parameters': {}
    }

    def run(self):
        try:
            kp = self.flab.devices["KnauerPump"]

            if kp.is_connected == False:
                self.flab.display("Error: KnauerPump is not connected.", output_list = 'output_queue')

            else:

                kp.disconnect()
                if not kp.get('is_connected'):
                    self.flab.display("Successfully disconnected from the KnauerPump system.", output_list = 'output_queue')
                else:
                    self.flab.display("Failed to disconnect from the KnauerPump system. Try again", output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
