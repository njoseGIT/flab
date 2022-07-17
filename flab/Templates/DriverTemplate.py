#Flab
#DriverTemplate.py
#A template class for device drivers
#Version 2.0.1
#Published 15-Jul-2022
#Distributed under GNU GPL v3
#Author: Nicholas Jose

class Driver():

    driver_name = 'DriverTemplate'
    version = '2.0.1'

    def __init__(self):
        pass

    #returns the value of a Driver attribute
    def get(self, attribute_name):
        return self.__getattribute__(attribute_name)

    #sets the value of a Driver attribute
    def set(self, attribute_name, value):
        self.__setattr(attribute_name, value)

    #returns the name of a Driver
    def get_driver_name(self):
        return self.driver_name

    #sets the name of a Driver
    def set_driver_name(self, driver_name):
        self.driver_name = driver_name
