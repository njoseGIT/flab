import serial
from serial.tools import list_ports
from Projects.MyFirstProject.Devices import SerialDevice

class Device(SerialDevice.Device):
    device_name = 'HarvardPump33DDS'
    port = 'NA'
    #ASCII character at the beginning of a transmission
    beg_char = ''
    #ASCII character at ending of a transmission
    end_char = '\r'
    #time to pause after sending a transmission
    pause_time = 0.1
    bd = 9600
    to = 1

    is_connected = False
    status = None

    info = {
        'long_name': 'Harvard Pump33DDS',
        'description': 'Methods to control a single Harvard Pump33DDS configured with independent control over both axes (a and b)',
        'guide': 'Ensure the device is powered on and properly connected before using any methods.',
        'version': '1.0.0',
        'author': 'Nicholas Jose',
        'last update': '20240918',
        'configuration': {},
        'methods': {
            'read_ver': {
                'description': 'Reads the firmware version of the syringe pump.',
                'guide': 'Run this method to retrieve the current firmware version.',
                'parameters': {}
            },

            'set_infusion_flowrate': {
                'description': 'Sets the infusion flow rate for the specified axis.',
                'guide': 'Run this method to set the flow rate for infusion. Ensure that the flow rate is within the allowed range.',
                'parameters': {
                    'flowrate': {
                        'description': 'The desired infusion flow rate.',
                        'unit': 'ul/min',
                        'type': 'float'
                    },
                    'axis': {
                        'description': 'The axis to set the infusion flow rate (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'set_withdraw_flowrate': {
                'description': 'Sets the withdrawal flow rate for the specified axis.',
                'guide': 'Run this method to set the flow rate for withdrawal. Ensure that the flow rate is within the allowed range.',
                'parameters': {
                    'flowrate': {
                        'description': 'The desired withdrawal flow rate.',
                        'unit': 'ul/min',
                        'type': 'float'
                    },
                    'axis': {
                        'description': 'The axis to set the withdrawal flow rate (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'set_target_volume': {
                'description': 'Sets the target volume to be infused or withdrawn for the specified axis.',
                'guide': 'Run this method to set the volume target. Ensure that the volume is within the syringe capacity.',
                'parameters': {
                    'volume': {
                        'description': 'The desired target volume.',
                        'unit': 'ul',
                        'type': 'int'
                    },
                    'axis': {
                        'description': 'The axis to set the target volume (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'set_syringe_volume': {
                'description': 'Sets the total syringe volume for the specified axis.',
                'guide': 'Run this method to set the syringe volume. This helps in calculating the remaining volume during operations.',
                'parameters': {
                    'volume': {
                        'description': 'The syringe volume.',
                        'unit': 'ul',
                        'type': 'int'
                    },
                    'axis': {
                        'description': 'The axis to set the syringe volume (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'set_syringe_diameter': {
                'description': 'Sets the syringe diameter for the specified axis.',
                'guide': 'Run this method to set the syringe diameter. This is used to calibrate the pump’s flow rate calculations.',
                'parameters': {
                    'diameter': {
                        'description': 'The diameter of the syringe.',
                        'unit': 'mm',
                        'type': 'float'
                    },
                    'axis': {
                        'description': 'The axis to set the syringe diameter (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'start_infuse': {
                'description': 'Starts the infusion process for the specified axis.',
                'guide': 'Run this method to start the infusion. Ensure the syringe and tubing are correctly set up.',
                'parameters': {
                    'axis': {
                        'description': 'The axis to start infusion (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'start_infuse_all': {
                'description': 'Starts the infusion process for all axes.',
                'guide': 'Run this method to start infusion on both axes simultaneously. Ensure all syringes and tubing are correctly set up.',
                'parameters': {}
            },
            'start_withdraw': {
                'description': 'Starts the withdrawal process for the specified axis.',
                'guide': 'Run this method to start the withdrawal. Ensure the syringe and tubing are correctly set up.',
                'parameters': {
                    'axis': {
                        'description': 'The axis to start withdrawal (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'start_withdraw_all': {
                'description': 'Starts the withdrawal process for all axes.',
                'guide': 'Run this method to start withdrawal on both axes simultaneously. Ensure all syringes and tubing are correctly set up.',
                'parameters': {}
            },
            'stop_pump': {
                'description': 'Stops the pump for the specified axis.',
                'guide': 'Run this method to stop the pump on the specified axis.',
                'parameters': {
                    'axis': {
                        'description': 'The axis to stop the pump (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'stop_pumps': {
                'description': 'Stops all pumps.',
                'guide': 'Run this method to stop all pumps on both axes.',
                'parameters': {}
            },

            'get_infused_volume': {
                'description': 'Retrieves the total infused volume for the specified axis.',
                'guide': 'Run this method to get the total volume that has been infused.',
                'parameters': {
                    'axis': {
                        'description': 'The axis to retrieve the infused volume (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            },
            'get_withdrawn_volume': {
                'description': 'Retrieves the total withdrawn volume for the specified axis.',
                'guide': 'Run this method to get the total volume that has been withdrawn.',
                'parameters': {
                    'axis': {
                        'description': 'The axis to retrieve the withdrawn volume (e.g., "a" or "b").',
                        'unit': 'None',
                        'type': 'string'
                    }
                }
            }
        }
    }

    def find_com_port(self):
        """
        Iterates over available COM ports to find the one corresponding to the device by
        sending the get_model_information command.

        Returns:
            str: COM port if the device is found, None otherwise.
        """
        self.flab.display("Finding available COM ports...")
        ports = list_ports.comports()
        for port in ports:
            try:
                self.flab.display(f"Checking port {port.device}...")
                ser = serial.Serial(port.device, baudrate=self.bd, timeout=self.to)
                self.ser = ser
                response = self.read_ver()
                ser.close()
                if response:
                    self.flab.display(f"HarvardPump33DDS device found on port {port.device}")
                    return port.device
            except Exception:
                continue
        self.flab.display("HarvardPump33DDS device not found.")
        return None

    def connect(self):
        """
        Finds the COM port corresponding to the device and opens the serial connection.

        Returns:
            str: COM port if successful, None otherwise.
        """
        try:
            com_port = self.find_com_port()
            if com_port:
                self.set_port(com_port)
                self.open_ser()
                if self.check_ser():
                    ver = self.read_ver()
                    if ver != '':
                        self.is_connected = True
                        self.flab.display(f"Connected {self.device_name} device on port {com_port}")
                    else:
                        self.flab.display(f"Failed to connect to {self.device_name}: Cound not read version")
                else:
                    self.flab.display(f"Failed to connect to {self.device_name}: could not create serial connection")
            else:
                self.is_connected = False
                self.flab.display(f"Failed to connect to {self.device_name}: could not find serial port")

            return self.is_connected

        except Exception as e:
            self.flab.display(f"Error finding and opening COM port for {self.device_name}: {e}")
            self.is_connected = False

            return self.is_connected

    def disconnect(self):
        """
        Disconnects the serial connection and updates the connection status.
        """
        try:
            if self.ser and self.ser.is_open:
                self.ser.close()
            self.is_connected = False
            self.flab.display(f"Disconnected from {self.device_name}.")
        except Exception as e:
            self.flab.display(f"Error disconnecting from the {self.device_name}: {e}")

    # #Initialize the pump by reading its name
    # def initialize(self):
    #     ini_err = ''
    #     if self.con_status:
    #         if not self.ini_status:
    #             try:
    #                 ver = self.read_ver()
    #                 if ver == '':
    #                     self.ini_status = False
    #                     self.display_status("Harvard initialization failure: check device")
    #                 else:
    #                     self.ini_status = True
    #                     self.display_status("Harvard initialized successfully")
    #                     self.display_status(ver)
    #             except Exception as e:
    #                 ini_err = "Harvard initialization failure: check serial connection."
    #                 self.display_status(str(e))
    #                 self.ini_status = False
    #     else:
    #         ini_err = 'Harvard initialization failure: not connected.'
    #         self.display_status(ini_err)
    #         self.ini_status = False
    #
    #     return self.ini_status

    def display_status(self, s):
        if self.print_status:
            self.flab.display(s)

    def read_ver(self):
        s = 'version'
        r = self.write_read(s,150)
        return r

    def set_infusion_flowrate(self, flowrate, axis):
        s = f'irate {axis} {flowrate} ul/min {axis}'
        r = self.write_read(s,100)
        return r

    def set_withdraw_flowrate(self, flowrate, axis):
        s = f'wrate {axis} {flowrate} ul/min'
        r = self.write_read(s,100)
        return r

    def set_target_volume(self, volume, axis):
        s = f'tvolume {axis} {volume} ul/min'
        r = self.write_read(s,100)
        return r

    def set_syringe_volume(self, volume, axis):
        s = f'svolume {axis} {volume} ul'
        r = self.write_read(s,100)
        return r

    def set_syringe_diameter(self, diameter, axis):
        s = f'diameter {axis} {diameter}'
        r = self.write_read(s,100)
        return r

    def start_infuse(self, axis):
        s = f'irun {axis}'
        r = self.write_read(s,100)
        return r

    def start_infuse_all(self):
        s = 'irun ab'
        r = self.write_read(s,100)
        return r

    def start_withdraw(self, axis):
        s = f'wrun {axis}'
        r = self.write_read(s,100)
        return r

    def start_withdraw_all(self):
        s = f'wrun ab'
        r = self.write_read(s,100)
        return r

    def stop_pump(self, axis):
        s = f'stop {axis}'
        r = self.write_read(s,100)
        return r

    def stop_pumps(self):
        s = 'stop ab'
        r = self.write_read(s,100)
        return r

    def get_infused_volume(self, axis):
        if axis == 'a' or axis == 'b' or axis == 'A' or axis == 'B':
            s = f'ivolume {axis}'
            r = self.write_readline(s)
            if 'ul' in r:
                r = r.replace('ul','')
                r = r.strip()
                r = float(r) / 1000.0
            elif 'ml' in r:
                r = r.replace('ml','')
                r = r.strip()
                r = float(r)
            else:
                r = None
            return r
        else:
            self.flab.display(f'Error in {self.device_name} get_withdrawn_volume: axis unknown')
            return None

    def get_withdrawn_volume(self, axis):
        if axis == 'a' or axis == 'A':
            s = 'wvolume a'
            r = self.write_readline(s)
            r = r.replace('A: ', '')

            if 'ul' in r:
                r = r.replace('ul', '')
                r = r.strip()
                r = float(r) / 1000.0
            elif 'ml' in r:
                r = r.replace('ml', '')
                r = r.strip()
                r = float(r)
            else:
                pass
            return r

        elif axis == 'b' or axis == 'B':
            s = 'wvolume b'
            r = self.write_readline(s)
            r = r.replace('B: ', '')

            if 'ul' in r:
                r = r.replace('ul', '')
                r = r.strip()
                r = float(r) / 1000.0
            elif 'ml' in r:
                r = r.replace('ml', '')
                r = r.strip()
                r = float(r)
            else:
                pass
            return r

        else:
            self.flab.display(f'Error in {self.device_name} get_withdrawn_volume: axis unknown')
            return None


    # def set_valve_state(self, state):
    #     s = 'valve ' + state
    #     r = self.write_read(s,100)
    #     return r