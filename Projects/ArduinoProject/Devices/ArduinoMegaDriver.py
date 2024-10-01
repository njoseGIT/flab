from pyfirmata import Arduino, util, ArduinoMega
from flab.Templates import DeviceTemplate

class Device(DeviceTemplate.Device):
    """
    A class for driving Arduino Mega using the pyfirmata library (https://pypi.org/project/pyFirmata/)
    """

    port = 'NA' #arduino serial port [str]
    is_arduino_connected = False #boolean indicating if the arduino is connected [str]
    print_status = True #boolean indicating if the status of the arduino should be printed [str]
    driver_name = 'ArduinoMega' #name of the driver [str]
    mega = {'digital': tuple(x for x in range(56)),
            'analog': tuple(x for x in range(16)),
            'pwm': tuple(x for x in range(2, 14)),
            'use_ports': True,
            'disabled': (0, 1, 14, 15)} #properties of the arduino

    def set_port(self,port):
        """
        Sets the serial port

        :param port: the serial port
        :type port: str
        :returns: None
        """
        self.port = port


    def get_port(self):
        """
        Returns the serial port

        :returns: str
        """
        return self.port

    def connect_arduino(self):
        """
        Initializes communication with the arduino. the serial port must be set.

        :returns: 0 if the arduino connects successfully, exception if it doesn't
        """
        if not self.is_arduino_connected and self.port != 'NA':
            try:
                self.ard = Arduino(self.port)
                self.ard.setup_layout(self.mega)
                self.it = util.Iterator(self.ard)
                self.it.start()
                self.is_arduino_connected = True
                if self.print_status:
                    self.flab.display('Arduino connected successfully')
                return 0
            except Exception as e:
                if self.print_status:
                    self.flab.display(str(e))
                    self.flab.display('Error connecting Arduino Mega. Check connection')
                return e
            finally:
                pass
        else:
            return 0

    def get_voltage(self, pin):
        """
        returns the voltage of an analog pin. If there is an error, the voltage returned is 0.

        :param pin: pin number (between 1 and 16)
        :type pin: int

        :returns: double
        """
        try:
            v = self.ard.analog[pin].read() * 5.0
        except Exception as e:
            v = -1
        finally:
            pass
        return v

    def get_arduino_connected(self):
        """
        Checks if the arduino is communicating

        :returns: boolean
        """
        return self.is_arduino_connected

