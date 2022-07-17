#Flab
#ProtocolTemplate.py
#A template class for device protocols
#Version 2.0.1
#Published 15-Jul-2022
#Distributed under GNU GPL v3
#Author: Nicholas Jose

class Protocol():

    protocol_name = 'ProtocolTemplate'
    version = '2.0.1'

    def __init__(self):
        pass

    #returns the value of a Protocol attribute
    def get(self, attribute_name):
        return self.__getattribute__(attribute_name)

    #sets the value of a Protocol attribute
    def set(self, attribute_name, value):
        self.__setattr(attribute_name, value)

    #returns the name of a Protcol
    def get_protocol_name(self):
        return self.protocol_name

    #sets the name of a Protocol
    def set_protocol_name(self, protocol_name):
        self.protocol_name = protocol_name


