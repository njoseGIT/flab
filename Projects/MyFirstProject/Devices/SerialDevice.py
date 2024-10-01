import serial
import time
from flab.Templates import DeviceTemplate

#A generic class for drivers using serial communication.
class Device(DeviceTemplate.Device):

    driver_name = 'SerialDevice'

    #default parameters

    port = 'NA'
    #ASCII character at the beginning of a transmission
    beg_char = '/'
    #ASCII character at ending of a transmission
    end_char = '\r'
    #time to pause after sending a transmission
    pause_time = 0.1
    bd = 9600
    to = 1

    def __init__(self):
        pass

    #set the current port
    def set_port(self, port):
        self.port = port

    #return the current port
    def get_port(self):
        return self.port

    # open serial communication
    def open_ser(self):
        try:
            self.ser = serial.Serial(port=self.port, baudrate=self.bd, timeout=self.to)
            return 0
        except Exception as e:
            print(e)
            return e

    # close serial communication
    def close_ser(self):
        self.ser.close()

    # check serial port
    def check_ser(self):
        check = self.ser.is_open
        return check

    #write a string message over the serial port
    def write(self,mess):
        try:
            write_str = self.beg_char + mess + self.end_char
            write_byt = write_str.encode()
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
            write_byt = write_str.encode()
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
            write_byt = write_str.encode()
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