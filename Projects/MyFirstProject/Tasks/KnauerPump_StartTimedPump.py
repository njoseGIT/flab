from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_StartTimedPump'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_StartPumping',
        'long_name': 'Starts pumping on KnauerPump ',
        'description': 'Starts pumping on KnauerPump according to the current setpoint. Ensure the device is on, connected, reagents are topped up,'
                       ' and inlets/outlets are properly secured',
        'parameters': {
            'flowrate': {
                'description': 'The flowrate setpoint',
                'unit': 'uL/min',
                'type': 'int',
                'default': 0,
            },
            'pumping_time': {
                'description': 'The amount of time to pump',
                'unit': 'seconds',
                'type': 'int',
                'default': 0,
            },
        }
    }

    def run(self, flowrate = 0, pumping_time = 0):
        try:
            if not self.flab.vars['KnauerPump_is_running']:
                device = self.flab.devices["KnauerPump"]
                if device.get('is_connected'):
                    self.flab.display(f'Starting KnauerPump timed pumping program', output_list='output_queue')
                    self.flab.vars['KnauerPump_is_running'] = True
                    device.set_flowrate(flowrate)
                    time.sleep(0.5)
                    device.start_pumping()
                    start_time = time.time()
                    current_time = 0
                    self.flab.vars['KnauerPump_stop_pumping'] = False
                    while current_time <= pumping_time and not self.flab.vars['KnauerPump_stop_pumping']:
                        time.sleep(0.5)
                        current_time = time.time() - start_time
                    device.stop_pumping()
                    self.flab.vars['KnauerPump_is_running'] = False
                else:
                    self.flab.display('Cannot start KnauerPump. KnauerPump is not connected', output_list = 'output_queue')
            else:
                self.flab.display(
                    'Warning: could not start KnauerPump dosing - another pumping program is already running',
                    output_list='output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
        self.flab.vars['KnauerPump_stop_pumping'] = True

