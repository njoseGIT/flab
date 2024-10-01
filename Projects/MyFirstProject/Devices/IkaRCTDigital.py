#Nicholas Jose 2022
#A class for IKA RCT Digital hotplates

from Projects.AMLearn.Devices import SerialDevice
from serial.tools import list_ports
import serial

class Device(SerialDevice.Device):

    device_name = 'IkaRCTDigital'

    #Default parameters
    print_status = True
    is_connected = False  # is IKA connected (serial port)
    is_initialized = False  # is IKA initialized
    port = 'NA'
    beg_char = '/' #ASCII character at the beginning of a transmission
    end_char = ' \r \n' #ASCII character at ending of a transmission
    pause_time = 0.1 #time to pause after sending a transmission
    bd = 9600
    to = 1
    default_temperature = 100
    max_temperature = 310
    max_stirring_rate = 1500

    # user information
    info = {
        'long_name': 'IKA RCT Digital Hotplate',
        'description': 'Methods to control a IKA RCT Digital Hotplate',
        'guide': 'Ensure device is on, and USB printer cable is connected before using any methods',
        'version': '1.0.0',
        'author': 'Nicholas Jose',
        'last update': '20240918',
        'configuration': {
            'default_temperature': {
                'unit': 'Celsius',
                'description': 'the default setpoint temperature',
                'default':100,
                'type': 'float'
            },
            'max_temperature': {
                'unit': 'Celsius',
                'description': 'The maximum setpoint temperature allowed',
                'default': 310,
                'type': 'float'
            },
            'max_stirring_rate': {
                'unit': 'RPM',
                'description': 'The maximum stirring rate allowed',
                'default': 1500,
                'type': 'number'
            },
        },
        'methods': {
            'connect': {
                'description': 'This method connects AMLearn to the IKA RCT Digital Hotplate via a serial usb connection',
                'guide': 'Run this method to establish a connection to the device to begin experiments. ',
                'parameters': {},
            },
            'disconnect': {
                'description': 'This method disconnects AMLearn from the IKA RCT Digital Hotplate',
                'guide': 'Run this method to break the connection to the Vapourtec. Note that running experiments on the '
                         'hotplate will continue regardless of disconnecting.',
                'parameters': {}
            },
            'set_temperature': {
                'description': 'This method sets the current temperature setpoint',
                'guide': 'Run this method to change the temperature setpoint. This method does not start the heater.',
                'parameters': {
                    'temperature': {
                        'description': 'The temperature setpoint',
                        'unit': 'Celsius',
                        'type': 'float'
                    }
                },
            },
            'set_stirring_speed': {
                'description': 'This method sets the current stirring speed setpoint',
                'guide': 'Run this method to change the stirring speed setpoint. This method does not start the stirrer.',
                'parameters': {
                    'speed': {
                        'description': 'The stirring speed setpoint',
                        'unit': 'RPM',
                        'type': 'integer'
                    }
                },
            },
            'start_heater': {
                'description': 'This method starts the heater',
                'guide': 'Run this method to start the heater. Ensure area is clear of hazards before running.',
                'parameters': {},
            },
            'stop_heater': {
                'description': 'This method stops the heater',
                'guide': 'Run this method to stops the heater. Ensure area is clear of hazards before running.',
                'parameters': {},
            },
            'start_stirring': {
                'description': 'This method starts the stirrer',
                'guide': 'Run this method to start the stirrer. Ensure area is clear of hazards before running.',
                'parameters': {},
            },
            'stop_stirring': {
                'description': 'This method stops the stirrer',
                'guide': 'Run this method to stops the stirrer. Ensure area is clear of hazards before running.',
                'parameters': {},
            },
        }
    }



    def read_name(self):
        s = 'IN_NAME'
        r = self.write_read(s, 80)
        return r

    def read_external_sensor(self):
        s = 'IN_PV_1'
        r = self.write_read(s, 80)
        del s
        return r[:len(r)-4]

    def read_hotplate_sensor(self):
        s = 'IN_PV_2'
        r = self.write_read(s, 80)
        return r[:len(r)-4]

    def read_stirring_speed(self):
        s = 'IN_PV_4'
        r = self.write_read(s, 80)
        return r

    def read_temperature_setpoint(self):
        s = 'IN_SP_1'
        r = self.write_read(s, 80)
        del s
        return r[:len(r)-4]

    def read_safety_temperature_setpoint(self):
        s = 'IN_SP_3'
        r = self.write_read(s, 80)
        return r

    def read_stirring_speed_setpoint(self):
        s = 'IN_SP_4'
        r = self.write_read(s, 80)
        return r[:len(r)-4]

    def set_temperature(self, temperature):
        try:
            s = 'OUT_SP_1 ' + str(temperature)
            r = self.write(s)
        except Exception as e:
            self.flab.display(f'Error in IkaRCTDigital-set_temperature: {e}')

    def set_stirring_speed(self, speed):
        s = 'OUT_SP_4 ' + str(speed)
        r = self.write(s)

    def start_heater(self):
        s = 'START_1'
        r = self.write(s)

    def stop_heater(self):
        s = 'STOP_1'
        r = self.write(s)

    def start_stirring(self):
        s = 'START_4'
        r = self.write(s)

    def stop_stirring(self):
        s = 'STOP_4'
        r = self.write(s)

    def reset(self):
        s = 'RESET'
        r = self.write(s)

    def set_operating_mode(self, mode):
        if mode == 'A' or mode == 'B' or mode == 'D':
            s = 'SET_MODE_' + mode
            r = self.write(s)
            return mode
        else:
            return -1

    def set_echo_safety_temperature(self,t):
        s = 'OUT_SP_12@' + str(t)
        r = self.write_read(s, 80)
        return r

    def set_echo_safety_stirring_speed(self,rpm):
        s = 'OUT_SP_42@' + str(rpm)
        r = self.write_read(s, 80)
        return r

    def watchdog_one(self, m):
        s = 'OUT_WD1@' + str(m)
        r = self.write(s)

    def watchdog_two(self, m):
        s = 'OUT_WD2@m' + str(m)
        r = self.write(s)

    def connect_port(self, port = ''):
        """
        Connects device serial port
        :returns: None
        """
        try:
            if self.is_connected:
                self.flab.display(f'{self.device_name} is already connected. Please disconnect and try again if necessary.')

            elif port == 'NA' or port == '' or port == None:
                self.display_status(f'Error in opening serial connection for {self.device_name}: port not assigned')

            else:
                try:
                    self.port = port
                    self.open_ser()
                    if self.check_ser():
                        self.is_connected = True
                        self.flab.display(f"{self.device_name} connected successfully.")
                except Exception as e:
                    self.is_connected = False
                    self.display_status(f'Error in opening serial connection for {self.device_name}: {e}')

        except Exception as e:
            self.flab.display(f"Failure to connect {self.device_name}: {e}")

        finally:
            return self.is_connected

    def find_port(self):
        """
        Iterates over available ports to find the one corresponding to the device by
        sending the get_model_information command.

        Returns:
            str: port if the device is found, None otherwise.
        """
        self.flab.display("Finding available ports...")
        ports = list_ports.comports()
        for port in ports:
            try:
                self.flab.display(f"Checking port {port.device}...")
                ser = serial.Serial(port.device, baudrate=self.bd, timeout=self.to)
                self.ser = ser
                response = self.read_name()
                ser.close()
                if response:
                    self.flab.display(f"IkaRCTDigital found on port {port.device}")
                    self.port = port.device
                    return port.device
            except Exception:
                continue

        self.flab.display("IkaRCTDigital device not found.")
        return None

    def connect(self):
        """
        Finds the port corresponding to the device and opens the serial connection.

        Returns:
            str: COM port if successful, None otherwise.
        """
        try:
            port = self.find_port()
            if port:
                connected = self.connect_port(port)
                if connected:
                    self.flab.display(f"Successfully connected {self.device_name}", output_list='output_queue')
                    self.is_connected = True
                    return True
                else:
                    self.flab.display(f"Error finding and connecting {self.device_name}",
                                      output_list='output_queue')
                    self.is_connected = False
                    return False
            else:
                self.flab.display(f"Could not find {self.device_name}. Make sure device is on and connected.",
                                  output_list='output_queue')
        except Exception as e:
            self.flab.display(f"Error finding and connecting {self.device_name}: {e}", output_list = 'output_queue')
            self.is_connected = False
            return False

    #Initialize the hotplate by reading its name
    def initialize(self):
        ini_err = ''
        if self.is_connected:
            if not self.is_initialized:
                try:
                    name = self.read_name()
                    if name == '':
                        self.is_initialized = False
                        self.display_status("Ika initialization faiulre: check device")
                    else:
                        self.is_initialized = True
                        self.display_status("Ika initialized successfully")
                        self.display_status(name)
                except Exception as e:
                    ini_err = "Ika initialization failure: check serial connection."
                    self.display_status(str(e))
                    self.is_initialized = False
        else:
            ini_err = 'Ika initialization failure: not connected.'
            self.display_status(ini_err)
            self.is_initialized = False

        return self.is_initialized

    def disconnect(self):
        """
        Disconnects the serial connection and updates the connection status.
        """
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.is_connected = False
            self.flab.display(f"Disconnected from {self.device_name}", output_list = 'output_queue')
        except Exception as e:
            self.flab.display(f"Error disconnecting from {self.device_name}: {e}", output_list = 'output_queue')

    def display_status(self, s):
        if self.print_status:
            self.flab.display(s)

    def set_default_temperature(self, new_default):
        self.default_temperature = new_default

    def get_default_temperature(self):
        return self.default_temperature