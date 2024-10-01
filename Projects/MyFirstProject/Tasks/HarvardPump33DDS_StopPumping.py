from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'HarvardPump33DDS_StopPumping'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'HarvardPump33DDS_StopPumping',
        'long_name': 'Stops pumping on HarvardPump33DDS ',
        'description': 'Stops pumping on HarvardPump33DDS according to the current setpoint. Ensure the device is on, connected, reagents are topped up,'
                       ' and inlets/outlets are properly secured',
        'parameters': {}
    }

    def run(self):
        try:
            self.flab.display(f'Stopping HarvardPump33DDS', output_list='output_queue')
            device = self.flab.devices["HarvardPump33DDS"]
            if device.get('is_connected'):
                device.stop_pumps()
            else:
                self.flab.display('Cannot stop HarvardPump33DDS. HarvardPump33DDS is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
