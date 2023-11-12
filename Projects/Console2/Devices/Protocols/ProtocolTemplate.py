#ProtocolTemplate.py
#A template class for device protocols
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

class Protocol():

    protocol_name = 'ProtocolTemplate'

    def __init__(self):
        pass

    def doublehelloworld(self):
        self.helloworld()
        self.helloworld()

