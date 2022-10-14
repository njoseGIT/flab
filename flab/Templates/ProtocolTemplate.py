# ProtocolTemplate
# A template class for device protocols
# Version 2.0.3
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
ProtocolTemplate contains default methods for accessing Protocol properties

Version 2.0.3
"""

class Protocol():

    version = '2.0.3'

    def __init__(self):
        """
        constructor

        """
        self.protocol_name = 'ProtocolTemplate'

    def get(self, attribute_name):
        """
        Returns the value of an attribute by its name

        :param attribute_name: name of the attribute
        :type attribute_name: string

        :returns: object
        """
        return self.__getattribute__(attribute_name)

    def set(self, attribute_name, value):
        """
        Sets the value of a Device attribute

        :param attribute_name: name of the attribute
        :type attribute_name: string

        :param value: new value of the attribute

        :returns: None
        """
        self.__setattr__(attribute_name, value)

    def get_protocol_name(self):
        """
        Returns the name of a Protocol

        :returns: name of the protocol (string)
        """
        return self.driver_name

    def set_protocol_name(self, protocol_name):
        """
        Sets the name of a Protocol

        :param protocol_name: the protocol name
        :type protocol_name: string

        :returns: None
        """
        self.protocol_name = protocol_name

