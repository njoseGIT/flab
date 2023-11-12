# Flab 3
# UiTemplate.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
UiTemplate contains a template Ui class,
which should be inherited by user Ui classes to function properly
"""

class Ui():

    """
    Ui description needed
    """

    ui_name = 'UiTemplate' #Mandatory attribute. This must match the name of the .py file

    def __init__(self):
        self.argument_descriptions = {}

    def set_flab(self, flab):
        self.flab = flab

    def get(self, attr_str):
        return self.__getattribute__(attr_str)

    def set(self, attr_str, value):
        self.__setattr__(attr_str, value)

    def run(self):
        pass

    def stop(self):
        pass