from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_StopPumping'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_StopPumping',
        'long_name': 'Stops pumping on KnauerPump ',
        'description': 'Stops pumping on KnauerPump according to the current setpoint. Ensure the device is on, connected, reagents are topped up,'
                       ' and inlets/outlets are properly secured',
        'parameters': {}
    }

    def run(self):
        try:
            self.flab.display(f'Stopping KnauerPump', output_list='output_queue')
            device = self.flab.devices["KnauerPump"]
            if device.get('is_connected'):
                device.stop_pumping()
            else:
                self.flab.display('Cannot stop KnauerPump. KnauerPump is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
