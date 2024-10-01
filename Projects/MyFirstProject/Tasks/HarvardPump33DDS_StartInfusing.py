from flab.Templates import TaskTemplate
import time

class Task(TaskTemplate.Task):
    task_name = 'HarvardPump33DDS_StartInfusing'
    task_type = 'thread'
    task_stopped = False

    info = {
        'name': 'HarvardPump33DDS_StartInfusing',
        'long_name': 'Starts infusing both pumps on HarvardPump33DDS ',
        'description': 'Starts pumping on HarvardPump33DDS according to the current setpoint.',
        'guide': 'Ensure the device is on, connected, reagents are topped up,'
                       ' and inlets/outlets are properly secured',
        'parameters': {
            'flowrate_a': {
                'description': 'the setpoint infusion flowrate of syringe a',
                'unit': 'ul/min',
                'type': 'int'
            },
            'flowrate_b': {
                'description': 'the setpoint infusion flowrate of syringe a',
                'unit': 'ul/min',
                'type': 'int'
            },
            'target_volume_a': {
                'description': 'the setpoint infusion volume of syringe a',
                'unit': 'ul',
                'type': 'int'
            },
            'target_volume_b': {
                'description': 'the setpoint infusion volume of syringe b',
                'unit': 'ul',
                'type': 'int'
            },
        }
    }

    def run(self, flowrate_a, flowrate_b, target_volume_a, target_volume_b):
        try:
            device = self.flab.devices["HarvardPump33DDS"]
            if device.get('is_connected'):
                self.flab.display(f'Setting infusion flowrates on HarvardPump33DDS', output_list='output_queue')
                device.set_infusion_flowrate(flowrate_a, 'a')
                time.sleep(0.5)
                device.set_infusion_flowrate(flowrate_b, 'b')
                time.sleep(0.5)
                device.set_target_volume(target_volume_a, 'a')
                time.sleep(0.5)
                device.set_target_volume(target_volume_b, 'b')
                time.sleep(0.5)
                self.flab.display(f'Starting infusion on HarvardPump33DDS', output_list='output_queue')
                device.start_infuse_all()
            else:
                self.flab.display('Cannot start infusion on HarvardPump33DDS. HarvardPump33DDS is not connected', output_list = 'output_queue')

        except Exception as e:
            self.flab.display(f'An error occurred in task {self.task_name}: {str(e)}', output_list = 'output_queue')

        self.flab.display(f'Task {self.task_name} completed.', output_list = 'output_queue')

    def stop(self):
        self.task_stopped = True
