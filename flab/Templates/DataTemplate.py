# Flab 3
# DataTemplate.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
DataTemplate contains a template Data class,
which should be inherited by user Data classes to function properly
"""

import inspect
from dataclasses import dataclass

@dataclass
class Data():
    """
    Data description needed

    """
    data_name = 'DataTemplate' #Mandatory attribute. This must match the name of the .py file

    def __init__(self):
        pass

    def get(self, attr_str):
        return self.__getattribute__(attr_str)

    def set(self, attr_str, value):
        self.__setattr__(attr_str, value)

    def get_data_name(self):
        return self.data_name

    def set_data_name(self, data_name):
        self.data_name = data_name

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