#Nicholas Jose 2022
#A class for Knauer Pumps

from Projects.AMLearn.Devices import SerialDevice
import time
from serial.tools import list_ports
import serial

class Device(SerialDevice.Device):

    device_name = 'KnauerPump'
    print_status = True
    is_connected = False
    # ini_status = False  # is IKA initialized

    port = 'NA'
    #ASCII character at the beginning of a transmission
    beg_char = ''
    #ASCII character at ending of a transmission
    end_char = '\r'
    #time to pause after sending a transmission
    pause_time = 0.1
    bd = 9600
    to = 1

    #set flowrate in uL/min
    def set_flowrate(self, flowrate = 0.0):
        s = 'FLOW:' + str(int(flowrate))
        self.write(s)

    #read flowrate in uL/min
    def read_flowrate(self):
        s = 'FLOW?'
        r = self.write_read(s, 80)
        flowrate_str = r.replace('FLOW:','')
        flowrate_num = float(flowrate_str)
        return flowrate_num

    #turn pump on
    def start_pumping(self):
        s = 'ON'
        self.write(s)

    #turn pump off
    def stop_pumping(self):
        s = 'OFF'
        self.write(s)

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
                response = self.read_flowrate()
                ser.close()
                if response:
                    self.flab.display(f"{self.device_name} device found on port {port.device}")
                    return port.device
            except Exception:
                continue
        self.flab.display(f"{self.device_name} device not found.")
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
                if self.open_ser() == 0:
                    self.is_connected = True
                    self.flab.display(f"Connected {self.device_name} device on port {com_port}")
                    return com_port
            self.flab.display(f"Failed to connect to {self.device_name}.")
            self.is_connected = False
            return None
        except Exception as e:
            self.flab.display(f"Error finding and opening COM port on {self.device_name}: {e}")
            self.is_connected = False
            return None

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

        # def connect(self):
    #     con_err = ""
    #     if self.get_port() == 'NA':
    #         con_err = con_err + "Knauer port not assigned."
    #     else:
    #         try:
    #             self.open_ser()
    #             self.check_ser()
    #         except Exception as e:
    #             con_err = con_err + "Knauer connection error. Check port assignment."
    #             self.display_status(con_err)
    #     if con_err == '':
    #         self.con_status = True
    #         self.display_status("Knauer connected successfully.")
    #     return self.con_status

    # #Initialize the pump by ...
    # def initialize(self):
    #     ini_err = ''
    #     if self.con_status:
    #         if not self.ini_status:
    #             try:
    #                 flowrate = self.read_flowrate()
    #                 if flowrate == '':
    #                     self.ini_status = False
    #                     self.display_status("Knauer initialization failure: check device")
    #                 else:
    #                     self.ini_status = True
    #                     self.display_status("Knauer initialized successfully")
    #                     self.display_status(flowrate)
    #             except Exception as e:
    #                 ini_err = "Knauer initialization failure: check serial connection."
    #                 self.display_status(str(e))
    #                 self.ini_status = False
    #     else:
    #         ini_err = 'Knauer initialization failure: not connected.'
    #         self.display_status(ini_err)
    #         self.ini_status = False

        #return self.ini_status

    def display_status(self, s):
        if self.print_status:
            self.flab.display(s)

    def write(self,mess):
        try:
            write_str = self.beg_char + mess + self.end_char
            write_byt = write_str.encode('UTF-8')
            self.ser.write(write_byt)
            time.sleep(self.pause_time)
            self.ser.flushInput()
            self.ser.flushOutput()
            return 0
        except Exception as e:
            print(e)
            return e

    def read(self,nbyt):
        try:
            read_byt = self.ser.read(nbyt)
            read_str = str(read_byt.decode())
            return read_str
        except Exception as e:
            print(e)
            return ''

    #write and read (without flushing buffer)
    def write_read(self,mess,nbyt):
        try:
            write_str = self.beg_char + mess + self.end_char
            write_byt = write_str.encode('UTF-8')
            self.ser.write(write_byt)
            time.sleep(self.pause_time)
            read_byt = self.ser.read(nbyt)
            read_str = str(read_byt.decode())
            self.ser.flushInput()
            self.ser.flushOutput()
            return read_str
        except Exception as e:
            print(e)
            return ''

    #write and read (without flushing buffer)
    def write_readline(self,mess):
        try:
            write_str = self.beg_char + mess + self.end_char
            write_byt = write_str.encode('UTF-8')
            self.ser.write(write_byt)
            time.sleep(self.pause_time)
            read_byt = self.ser.readline()
            read_str = str(read_byt.decode())
            self.ser.flushInput()
            self.ser.flushOutput()
            return read_str
        except Exception as e:
            print(e)
            return ''