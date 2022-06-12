#DriverTemplate.py
#A template class for device drivers
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

class Driver():

    driver_name = 'DriverTemplate'

    def __init__(self):
        pass

    def get(self, attr_str):
        return self.__getattribute__(attr_str)

    def set(self, attr_str, value):
        self.__setattr(attr_str, value)

    def helloworld(self):
        self.flab.display(self.driver_name + " : Hello World 2")

    def set_driver_name(self, s):
        self.driver_name = s

    def get_driver_name(self):
        return self.driver_name