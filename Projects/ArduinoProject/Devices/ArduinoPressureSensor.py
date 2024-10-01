from Projects.ArduinoProject.Devices import ArduinoMegaDriver
import time
import numpy as np

class Device(ArduinoMegaDriver.Device):
    """
    A class for getting pressure data using with an ArduinoMega. Upon creating an object, define the analog input pins,
    the voltage multipliers (A) and offsets (B).

    Pressure = A * voltage + B. A and B are given in numpy arrays so that for each transducer a multiplier and offset
    can be defined.
    """

    device_name = 'PressureSensor'

    is_sensor_connected = False #if the sensor is connected
    print_status = True #if the status of the pressure sensors should be displayed
    n_pins = None # Total number of pins
    p_pins = []  # Pressure transducer analog pins
    p_mult = []  # Pressure range (Bar)
    p_off = []  # Voltage multiplier (1/V)


    def check_configuration(self):
        """
        Checks if the sensor has been correctly configured for measurements.

        :returns: boolean
        """
        try:
            is_configured = False
            is_configured = (self.n_pins!=None and len(self.p_pins) != 0 and len(self.p_mult) and len(self.p_off))
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in pressure sensor configuration (set_config)')
        return is_configured

    def connect_sensors(self,pins,multipliers,offsets):
        """
        Connects arduino,sets pins and calibration parameters for pressure measurement

        :param pins: a list of the pins that sensors are connected to
        :type pins: [int]

        :param multipliers: a list of the multiplier (A) parameters, with indicies corresponding to the indicies in pins
        :type multipliers: [int], [double] or [float]

        :param offsets: a list of the offset (B) parameters, with indicies corresponding to the indicies in pins
        :type offsets: [int], [double] or [float]

        :returns: 0 if successful, -1 if not successful
        """
        try:
            self.connect_arduino()
            self.set_config(pins, multipliers, offsets)
            if self.get_arduino_connected():
                for i in self.p_pins:
                    time.sleep(0.1)
                    self.ard.analog[i].enable_reporting()
                self.is_sensor_connected = True
                if self.print_status:
                    self.flab.display('Pressure sensor(s) connected')
                    return 0
            else:
                self.is_sensor_connected = False
                if self.print_status:
                    self.flab.display('Failure to connect pressure sensor. Check connection')
                    return -1
        except Exception as e:
            if self.print_status:
                self.flab.display('Failure to connect sensors (connect_sensors)')
                self.flab.display(e)
            return -1
        finally:
            pass

    def set_config(self,pins,multipliers,offsets):
        """
        Sets pins and calibration parameters for pressure measurement

        :param pins: a list of the pins that sensors are connected to
        :type pins: [int]

        :param multipliers: a list of the multiplier (A) parameters, with indicies corresponding to the indicies in pins
        :type multipliers: [int], [double] or [float]

        :param offsets: a list of the offset (B) parameters, with indicies corresponding to the indicies in pins
        :type offsets: [int], [double] or [float]

        :returns: None
        """
        try:
            self.n_pins = len(pins)
            self.p_pins = pins  # Pressure transducer analog pins
            self.p_mult = multipliers  # Pressure range (Bar)
            self.p_off = offsets # Voltage multiplier (1/V)
        except Exception as e:
            self.flab.display('Failure in pin configuration (set_config)')
            self.flab.display(e)
        finally:
            pass

    def get_pressure(self, pin_index):
        """
        Calculates the measured pressure at a given pin index (corresponding to the pins array given in a set_config or
        connect sensors.

        :param pin_index: index of the pin to be measured
        :type pin_index: int

        :returns: int, double or float. An output of -1.0 indicates an error has occurred.
        """
        try:
            pressure = -1.0
            if self.is_sensor_connected:
                voltage = self.get_voltage(self.p_pins[pin_index])
                pressure = self.p_mult[pin_index]*voltage + self.p_off[pin_index]
        except Exception as e:
            self.flab.display('Failure in pressure measurement (get_pressure)')
            self.flab.display(e)
        finally:
            return pressure

    def get_pressure_all(self):
        """
        Calculates the measured pressure for all pins given in set_config or connect_sensors.

        :returns: numpy array. An output of -1 indicates an error has occurred.
        """
        try:
            pressures = np.ones(self.n_pins)*-1
            if self.is_sensor_connected:
                for i in range(0, self.n_pins):
                    voltage = self.get_voltage(self.p_pins[i])
                    pressures[i] = self.p_mult[i] * voltage + self.p_off[i]
        except Exception as e:
            self.flab.display('Failure in pressure measurement (get_pressure_all)')
            self.flab.display(e)
        finally:
            return pressures

    def get_avg_pressure(self, sampling_time, sampling_frequency, pin_index):
        """
        Gets the average pressure over a given sampling time at a given sampling frequency for a single pin.

        :param time_seconds: time to record pressure
        :type time_seconds: int

        :param pin_index: index of the pin to measure
        :type pin_index: int

        :returns: int, double or float. -1 if there is an error in measurement
        """
        try:
            avg_pressure = -1
            sample_points = int(sampling_time*sampling_frequency)
            temp_pressure = np.ones(sample_points)*-1
            for i in range(0, sample_points):
                temp_pressure[i] = self.get_pressure(pin_index)
                time.sleep(1/sampling_frequency)
            avg_pressure = np.mean(temp_pressure)
        except Exception as e:
            self.flab.display('Failure in pressure measurement (get_avg_pressure)')
            self.flab.display(e)
        finally:
            return avg_pressure

    def get_avg_pressure_all(self, sampling_time, sampling_frequency):
        """
        Gets the average pressure over a given sampling time (in seconds) and sampling frequency f (in 1/seconds) for all given pins

        :param time_seconds: time to record pressure
        :type time_seconds: int

        :param pin_index: index of the pin to measure
        :type pin_index: int

        :returns: int, double or float. -1 if there is an error in measurement
        """
        try:
            avg_pressures = -1
            sample_points = int(sampling_time*sampling_frequency)
            temp_pres = np.ones([self.n_pins, sample_points])*-1
            for i in range(0, sample_points):
                for j in range(0,self.n_pins):
                    temp_pres[j,i] = self.get_pressure(self.p_pins[j])
                time.sleep(1/sampling_frequency)
            avg_pressures = np.mean(temp_pres,1)
        except Exception as e:
            self.flab.display('Failure in pressure measurement (get_avg_pressure_all)')
            self.flab.display(e)
        finally:
            return avg_pressures