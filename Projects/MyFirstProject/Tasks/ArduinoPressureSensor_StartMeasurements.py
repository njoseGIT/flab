import time

from flab.Templates import DeviceTemplate
#A class for testing analog pressure sensors from an Arduino

class Task(DeviceTemplate.Device):

    task_name = 'ArduinoPressureSensor_StartMeasurements'
    task_stopped = False

    #run the task with a default channel pin of 1
    def run(self, channel_pin = 1):
        try:
            # create a flag to stop the task on demand
            self.flab.vars['stop_pressure_measurements'] = False

            # create a local reference to the device
            p = self.flab.devices['ArduinoPressureSensor']

            # set the port
            p.set_port('COM5')

            #connect the sensors with appropriate constants
            p.connect_sensors([0,1,2,3,4,5,6,7,8,9],[1.724,1.724,1.724,1.724,1.724,1.724,1.724,1.724,1.724,1.724],[0,0,0,0,0,0,0,0,0,0])

            #create a variable to represent the pressures
            self.flab.add_var(0,'p_channel')

            #wait 0.5 seconds
            time.sleep(0.5)

            if p.get('is_sensor_connected'):

                while not self.flab.vars['stop_pressure_measurements']:
                    # get the pressures
                    #pres = p.get_pressure_all()
                    all_pressures = p.get_avg_pressure_all(1,5)

                    # output all pressures on the console command line
                    self.flab.display(all_pressures)

                    #assign the p_channel variable to the pressure of a particular pin
                    self.flab.vars['p_channel']=all_pressures[channel_pin]

                    #output the pressure on the console command line
                    self.flab.display(self.flab.vars['p_channel'])

                    #wait for 0.25 seconds
                    time.sleep(0.25)
            else:
                self.flab.display('PressureMeasurements not started, PressureSensor not connected')

        except Exception as e:
            self.flab.display('Error in PressureMeasurements')
            self.flab.display(e)
        finally:
            pass

    def stop(self):
        self.flab.vars['stop_pressure_measurements'] = True #a flag to stop recording
