#Flab
#DeviceTemplate.py
#A template class for devices
#Version 1.1.2
#Published 1-January-2021
#Distributed under GNU GPL v3
#Author: Nicholas Jose

from flab.Templates import DriverTemplate
from flab.Templates import ProtocolTemplate
import inspect

class Device(DriverTemplate.Driver, ProtocolTemplate.Protocol):

    device_name = 'DeviceTemplate'
    protocol_name = 'ProtocolTemplate'
    driver_name = 'DriverTemplate'
    version = '2.0.1'

    def __init__(self):
        self.device_name = 'DeviceTemplate'
        self.protocol_name = 'ProtocolTemplate'
        self.driver_name = 'DriverTemplate'

    #returns the value of a Device attribute
    def get(self, attribute_name):
        return self.__getattribute__(attribute_name)

    #sets the value of a Device attribute
    def set(self, attribute_name, value):
        self.__setattr__(attribute_name, value)

    #returns the name of a Device
    def get_device_name(self):
        return self.device_name

    #sets the name of a Device
    def set_device_name(self, device_name):
        self.device_name = device_name

    #returns the flab object of a Device
    def get_flab(self):
        return self.flab

    #sets the flab object of a Device
    def set_flab(self, flab):
        self.flab = flab

    #returns the attributes of a Device in a list
    def list_attributes(self):
        variables = []
        for i in inspect.getmembers(self):
            if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    #returns the methods of a Device in a list
    def list_methods(self):
        variables = []
        for i in inspect.getmembers(self):
            if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    #returns the arguments of a method of a Device in a list
    def list_method_args(self,method_name):
        fullargspec = inspect.getfullargspec(self.get(method_name))
        return fullargspec