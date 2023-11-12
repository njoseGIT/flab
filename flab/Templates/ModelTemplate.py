# Flab 3
# ModelTemplate.py
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
ModelTemplate contains a template Model class,
which should be inherited by user Model classes to function properly
"""


import inspect

class Model():
    """
    Model description needed
    """

    model_name = 'ModelTemplate'

    def __init__(self):
        pass

    def get(self, attribute_name):
        """
        Returns the value of a model attribute

        :param attribute_name: str

        :returns: model attribute
        """
        return self.__getattribute__(attribute_name)

    def set(self, attribute_name, value):
        """
        Sets the value of a model attribute

        :param attribute_name: str

        :returns: None
        """
        self.__setattr__(attribute_name, value)

    def get_model_name(self):
        """
        Returns the name of a model

        :returns: model name
        :rtype: str
        """
        return self.model_name

    def set_model_name(self, model_name):
        """
        Sets the name of a model

        :param model_name: str
        :returns: None
        """
        self.model_name = model_name

    def get_flab(self):
        """
        Returns the flab object of a model

        :returns: flab
        :rtype: Flab
        """
        return self.flab

    def set_flab(self, flab):
        """
        Sets the flab object of a model

        :param flab: Flab
        :returns: None
        """
        self.flab = flab

    def list_attributes(self) -> list:
        """
        Returns the attributes of a model in a list.

        :returns: the list of model attributes
        :rtype: list
        """
        attributes = []
        try:
            for i in inspect.getmembers(self):
                if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                    attributes.append(i[0])

        except Exception as e:
            self.flab.display('Error in listing ' + self.model_name + ' attributes')
            self.flab.display(e)

        finally:
            return attributes

    def list_methods(self):
        """
        Returns the methods of a Model in a list.

        :returns: the list of model methods
        :rtype: list
        """

        variables = []
        for i in inspect.getmembers(self):
            if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                variables.append(i[0])
        return variables

    def list_method_args(self,method_name):
        """
        Returns the arguments of a method of a model in a list

        :param method_name: str

        :returns: method arguments
        :rtype: list
        """
        fullargspec = inspect.getfullargspec(self.get(method_name))
        return fullargspec

    def predict(self):
        pass

    def evaluate(self):
        pass

    def train(self):
        pass