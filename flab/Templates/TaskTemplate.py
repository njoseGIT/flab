# Flab 3
# TaskTemplate.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
TaskTemplate contains a template Task class,
which should be inherited by user Task classes to function properly
"""

import inspect

class Task():
    """
    Task description needed
    """

    task_name = 'TaskTemplate' #Mandatory attribute. This must match the name of the .py file
    task_type = 'thread' #Mandatory attribute. This must be "thread", "asyncio" or "process"
    info = {}

    def __init__(self):
        self.task_stopped = False
        self.argument_descriptions = {}

    def set_flab(self, flab):
        """
        Sets the flab object to reference within a task.

        :param flab: a flab object
        :type flab: Flab
        """
        self.flab = flab

    def get(self, attribute_name):
        """
        Returns the attribute of a task object.

        :param attribute_name: the name of the attribute
        :type attribute_name: str
        """
        return self.__getattribute__(attribute_name)

    def set(self, attr_str, value):
        """
        Sets the attribute of a task object.

        :param attribute_name: the name of the attribute
        :type attribute_name: str
        """
        self.__setattr__(attr_str, value)

    def run(self):
        """
        The method for running a task.

        :return: None
        """
        pass

    def stop(self):
        """
        The method for stopping a task.

        :return: NoneE
        """
        pass

    def display(self, s):
        self.flab.display(s)

    def get_info(self):
        return self.info

    def get_run_arguments(self):
        return inspect.getfullargspec(self.run)

    def get_stop_arguments(self):
        return inspect.getfullargspec(self.stop)



