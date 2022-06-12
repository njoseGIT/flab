#DeviceTemplate.py
#A template class for devices
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

from Devices.Drivers import DriverTemplate
from Devices.Protocols import ProtocolTemplate
import inspect

class Device(DriverTemplate.Driver, ProtocolTemplate.Protocol):

    device_name = 'DeviceTemplate'
    protocol_name = 'ProtocolTemplate'
    driver_name = 'DriverTemplate'

    def __init__(self):
        self.device_name = 'DeviceTemplate'
        self.protocol_name = 'ProtocolTemplate'
        self.driver_name = 'DriverTemplate'

    def get(self, attr_str):
        return self.__getattribute__(attr_str)

    def set(self, attr_str, value):
        self.__setattr__(attr_str, value)

    def get_device_name(self):
        return self.device_name

    def set_device_name(self, device_name):
        self.device_name = device_name

    def get_flab(self):
        return self.flab

    def set_flab(self, flab):
        self.flab = flab

    def list_attributes(self):
        variables = []
        for i in inspect.getmembers(self):
            if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_methods(self):
        variables = []
        for i in inspect.getmembers(self):
            if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_method_args(self,method_name):
        fullargspec = inspect.getfullargspec(self.get(method_name))
        return fullargspec