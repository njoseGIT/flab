from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'KnauerPump_DoseVolume'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'KnauerPump_DoseVolume',
        'long_name': 'Dose volume with KnauerPump ',
        'description': 'Doses a given volume with a given flowrate by calculating the time required. '
                       'Ensure the device is on, connected, reagents are topped up, lines are primed'
                       ' and inlets/outlets are properly secured',
        'parameters': {
            'flowrate': {
                'description': 'The flowrate setpoint',
                'unit': 'uL/min',
                'type': 'int',
                'default': 0,
            },
            'dosing_volume': {
                'description': 'The amount of volume to pump',
                'unit': 'uL',
                'type': 'int',
                'default': 0,
            },
        }
    }

    def run(self, flowrate = 0, dosing_volume = 0):
        try:
            if not self.flab.vars['KnauerPump_is_running']:
                device = self.flab.devices["KnauerPump"]
                self.flab.vars['KnauerPump_stop_dose_volume'] = False
                if device.get('is_connected'):
                    self.flab.display(
                        f'Starting KnauerPump volume dosing program at {flowrate} uL/min for {dosing_volume} uL',
                        output_list='output_queue')
                    self.flab.vars['KnauerPump_is_running'] = True
                    pumping_time = dosing_volume / flowrate * 60
                    self.flab.display(f'Calculated dosing time = {pumping_time}', output_list = 'output_queue')
                    start_time = time.time()
                    current_time = 0
                    device.set_flowrate(flowrate)
                    time.sleep(0.5)
                    device.start_pumping()
                    self.flab.vars['KnauerPump_stop_pumping'] = False
                    while current_time <= pumping_time and not self.flab.vars['KnauerPump_stop_pumping']:
                        time.sleep(0.5)
                        current_time = time.time() - start_time
                    device.stop_pumping()
                    self.flab.display('KnauerPump dosing complete', output_list = 'output_queue')
                    self.flab.vars['KnauerPump_is_running'] = False
                else:
                    self.flab.display('Cannot start KnauerPump. KnauerPump is not connected', output_list = 'output_queue')
            else:
                self.flab.display('Warning: could not start KnauerPump dosing - another pumping program is already running', output_list = 'output_queue')
        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}')

        self.flab.display(f'Task {self.task_name} completed.')

    def stop(self):
        self.task_stopped = True
        self.flab.vars['KnauerPump_stop_pumping'] = True

