from flab.Templates import DeviceTemplate

class Device(DeviceTemplate.Device):
    device_name = "HelloWorldDevice"  # Name of the HelloWorldDevice
    hello = 'world'

    def create_device_attribute(self):
        self.hello_world = 'hello world'

    def display_device_attribute(self):
        self.flab.display(self.hello_world)

    def display_hello_world(self):
        self.flab.display("Hello World")
