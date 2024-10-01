from flab.Templates import TaskTemplate

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_ReadFlowrateSetpoint'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_ReadFlowrateSetpoint',
        'long_name': 'Read the flowrate setpoint of KnauerPump',
        'description': 'Displays the flowrate setpoint on the KnauerPump in uL/min. Note that the flowrate setpoint on the KnauerPump is not necessarily the actual'
                       'flowrate of liquid.',
        'parameters': {}
    }

    def run(self):
        try:
            self.flab.display(f'Reading KnauerPump flowrate..', output_list='output_queue')
            kp = self.flab.devices["KnauerPump"]
            if kp.get('is_connected'):
                flowrate = kp.read_flowrate()
                self.flab.display(f'Knauer flowrate = {flowrate} uL/min')
            else:
                self.flab.display('Cannot read flowrate. KnauerPump is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
