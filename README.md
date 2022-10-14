# flab

Author: Nicholas A. Jose
Version: 2.0.2

## Recent Updates
1.0.0: Device objects have publicly accessible attributes and methods.

1.0.7: Resolution of bug in booting. Boot script no longer requires changing of directories.

1.1.0: Resolved issues in closing flab and multiprocessing. Requires Python 3.9 or later

1.1.1: Resolved issue in listing tasks

2.0.0: BootManager contains functionality for network communication. Flab objects are now initialized with queues as 
optional arguments. TaskManager no longer implements QThread (as a "QTask") such that
flab is no longer dependent on PyQT. Templates are now included within flab.Templates. These are DeviceTemplate, DriverTemplate
and ProtocolTemplate, which may be inherited by Device classes.

2.0.1: Resolved bug in distribution

2.0.2: Docstrings created 

2.0.3: Docstrings amended

## Summary

Flab was created to be a fast, flexible and fun framework for creating automated chemical laboratories. As a coding
framework, rather than defining specific sequence of automated actions, FLab aims to make the task of creating automated 
systems significantly simpler. 

Flab achieves its flexibility via the following principles:

1. Modularity via inheritance
2. Parallelization via threaded, asynchronous and multiprocess computing
3. Synchronization via a universal object space
4. Intuitive via minimalist and physically relevant ontologies
5. Accessible via open-source distribution (currently under GNU GPL v3)

Flab abstracts an experimental project into its main components: 
1. physical devices (the Device class)
2. actions (the Task class)
3. user interfaces (the UI class)

This package provides methods for the management of a shared object space (the Flab class), parallel/synchronised tasks 
(the TaskManager class), configuring shared devices (the DeviceManager class), and interfaces (the UiManager class).
This package also includes methods for running a given project (BootManager)

## Installation

To install flab, enter into the terminal

    python3 -m pip install flab

The dependency PyQt5 must also be installed, using

    python3 -m pip install PyQt5

## Directory structure
Before beginning any project with Flab, the working directory must be set up properly.
The working directory has the following structure. All projects are stored in the "Projects" folder. Any other code 
(such as a custom flab distribution) or data can also be kept in this working directory.

    Working_directory/
    
    │  ├ Projects/
    
    │  │  ├ example_project_1/ 
    
    │  │  └ example_project_2/
    
    │  └ Other_folders/


A project directory has the following structure: 

    example_project/
    
    ├ Boot/
    
    ├ Tasks/

    ├ Devices/
    
    │  ├ Drivers/ 
    
    │  └ Protocols/
    
    ├ UIs/
    
    │  ├ Actions/ 
    
    │  └ Designs/

    │  └ Windows/


A project directory may be automatically created using flab's create_project_directory() method

## Flab Objects

A Flab object acts as a space for the shared storage of:
1. devices (in the devices dictionary)
2. tasks (in the tasks dictionary)
3. variables (in the vars dictionary), 
4. modules (in the modules dictionary)

The Flab class inherits DeviceManager, TaskManager and UiManager, such that methods in those classes may be easily 
customized. These managers contain methods for manipulating devices, tasks and ui's.

A Flab object can also be created with optional queues to enable communication with a user interface (the "ui_queue") and a 
machine ("flab_queue"), which are None by default. Messages from flab can also be output to the terminal/command line with the 
boolean "print_status"

Example usage: Creating flab without queues and not printing to the command line/terminal

    from flab import Flab
    flab = Flab.Flab(print_status = False)

## Tasks

Tasks are essentially routines or programs, which can be run in a variety of fashions depending on user input. Task files
are saved as python files with the Tasks folder of a project.

Tasks must be first loaded into flab with the load_task(task_name) method. They may then be started or stopped using the 
start_task(task_name, *args, **kwargs) and stop_task(task_name, *args, **kwargs) methods.

Example usage:

    flab.load_task('HelloWorld')
    flab.start_task('HelloWorld')
    flab.stop_task('HeloWorld')

Multiple tasks can be loaded simulataneously with the flab.load_tasks method. All the tasks in a given project can be loaded 
using flab.load_all_tasks(). Tasks can also be dynamically reloaded by using the reload_task and reload_tasks 
methods. All tasks may be stopped in one line with the command "flab.stop_all_tasks()". Task objects do not have publicly accessible
attributes.

Each task requires three attributes:
1. task_name: a string that matches the filename
2. task_type: a string that determines how the task is run. Either "thread", "asyncio" or "process"
3. task_stopped: a Boolean flag indicating if the task has been stopped.

Each task requires three methods:

1. __ init __(self, flab): initializes the Task object with the shared flab space
2. run(self, *args, **kwargs): this is called when flab.start_task is called. This method can contain while loops, which
       can be externally closed with the flag task_stopped.
3. stop(self, *args, **kwargs): this is called when flab.stop_task is called. This method can be used to modify the task_stopped
   flag

###Threaded Tasks

By default,
all tasks are "threads" -- meaning that they run on a single CPU and are essentially "queued." See python's threading library
for a more detailed description.

Threaded Task Example:

    #HelloWorld continuously prints 'HelloWorld' every second until stopped

    import time
    class Task():
    
        task_name = 'HelloWorld'
        task_type = 'thread'
        task_stopped = False
    
        def __init__(self,flab):
            self.flab = flab
    
        def run(self):
            self.task_stopped = False
            while not self.task_stopped:
                print('Hello World')
                time.sleep(1)
    
        def stop(self):
            self.flab.tasks['HelloWorld'].task_stopped = True


###Asyncio Tasks

An asynchronous task can be used to make running some routines more efficient. This utilizes
python's asyncio library.

An asyncio task has several key differences to a threaded task:
1. the asyncio library must be imported
2. task_type = 'asyncio'
3. run and stop methods must be defined with an "async" prefix, shown below:
    
    
    async def run(self):...
    
    async def stop(self):...

4. instead of using python's time.sleep(seconds) method for blocking, use:

    await asyncio.sleep(seconds)

Asyncio Task Example 1:

    #This task prints Hello World continuously, every second, until stopped.

    import asyncio
    class Task():
    
        task_name = 'HelloWorldAsyncio'
        task_type = 'asyncio'
        task_stopped = False
    
        def __init__(self,flab):
            self.flab = flab
    
        async def run(self):
            self.task_stopped = False
            while not self.task_stopped:
                print('Hello World')
                await asyncio.sleep(1)
    
        async def stop(self):
            self.flab.tasks['HelloWorldAsyncio'].task_stopped = True #a flag to stop the script

There are two ways to run multiple asyncio tasks simultaneously. The first requires the definition of multiple asyncio
functions within one task. If this is done, the functions must be gathered at the end of the run method, as seen in the example
below.

    #This task runs two counting tasks asynchronously. 
    #A flab variable "count" is used for counting.
    #count() adds one to the count
    #count2() adds two to the count
    #when run correctly, the Python console should print multiples of three

    import asyncio
    class Task():
    
        task_name = 'CountAsyncio'
        task_type = 'asyncio'
        task_stopped = False
    
        def __init__(self,flab):
            self.flab = flab
    
        async def run(self):
            self.task_stopped = False
            self.flab.add_var(0, 'count')
            async def count():
                while not self.task_stopped:
                    self.flab.vars['count'] = self.flab.vars['count'] + 1
                    await asyncio.sleep(1)
                    print(self.flab.vars['count'])
            async def count2():
                while not self.task_stopped:
                    self.flab.vars['count'] = self.flab.vars['count'] + 2
                    await asyncio.sleep(1)
            await asyncio.gather(count(),count2())
    
        async def stop(self):
            self.flab.tasks['scratch'].task_stopped = True #a flag to stop the script

In the second manner, two separate asyncio tasks may be defined separately. However, both tasks must be called simultaneously
using flab.start_asyncio_tasks(task_names), where task_names is a list of the task names
   
Example: AsyncCount
 
    #This task runs one counting task asynchronously. 
    #A flab variable "count" is used for counting.
    #This task increases the count by one and prints the current count value

    import asyncio

    class Task():

        task_name = 'AsyncCount'
        task_type = 'asyncio'
        task_stopped = False
    
        def __init__(self,flab):
            self.flab = flab
    
        async def run(self):
            self.task_stopped = False
            self.flab.add_var(0, 'count')
            while not self.task_stopped:
                self.flab.vars['count'] = self.flab.vars['count'] + 1
                await asyncio.sleep(1)
                print(self.flab.vars['count'])
    
        async def stop(self):
            self.flab.tasks['AsyncCount'].task_stopped = True #a flag to stop the script

Example: AsyncCount2

    #This task runs one counting task asynchronously. 
    #A flab variable "count" is used for counting.
    #This task increases the count by two

    import asyncio

    class Task():
    
        task_name = 'AsyncCount2'
        task_type = 'asyncio'
        task_stopped = False
    
        def __init__(self,flab):
            self.flab = flab
    
        async def run(self):
            self.task_stopped = False
            while not self.task_stopped:
                self.flab.vars['count'] = self.flab.vars['count'] + 2
                await asyncio.sleep(1)
    
        async def stop(self):
            self.flab.tasks['AsyncCount2'].task_stopped = True #a flag to stop the script

Example: Running and stopping AsyncCount and AsyncCount2

    flab.load_tasks(['AsyncCount','AsyncCount2'])
    flab.start_asyncio_tasks(['AsyncCount','AsyncCount2'])
    flab.stop_asyncio_tasks(['AsyncCount','AsyncCount2'])

###Process Tasks

Process tasks are executing using Python's multiprocessing library, meaning that they are distributed across different CPUs.
This distribution makes the sharing of data i.e. flab slightly more complicated.

A process task has several key differences to a threaded task:
1. task_type = 'process'
2. The flag boolean used to stop a loop should be defined as a flab variable instead of a task variable

Process Example:


    #This task prints 'Hello World' every second within a separate process
    #A flab variable self.flab.vars['HelloWorldProcess_stopped'] is used instead of a Boolean flag within the Task so that external 
    other processes can signal this process to stop

    class Task():

        task_name = 'HelloWorldProcess'
        task_type = 'process'
    
        def __init__(self,flab):
            self.flab = flab
    
        def run(self):
            self.flab.add_var(False,'HelloWorldProcess_stopped')
            while not self.flab.vars['HelloWorldProcess_stopped']:
                print('Hello World')
                time.sleep(1)
    
        def stop(self):
            self.flab.vars['HelloWorldProcess_stopped'] = True

Loading, starting and stopping a process is exactly the same as starting a thread. There are a few differences when a process
is started within a boot script, which is discussed in the Boot section.

Example: Loading, starting and stopping process tasks

    flab.load_task('HelloWorldProcess')
    flab.start_task('HelloWorldProcess')
    flab.stop_task('HeloWorldProcess')

## Devices

Device classes are representations of physical laboratory devices. For example - a balance would become BalanceDevice,
or a hot plate would become HotPlateDevice.

To digitally represent the properties and actions of a device we provide the following abstraction:

1. How a computer digitally communicates with the device, explicitly defined in the Driver class.
2. How a device is used within a given task, explicitly defined in the Protocol class.
3. The specific configuration of the device, explicitly defined in the Device class.

The Device class inherits Driver and Protocol classes. Methods for drivers and/or protocols may already be provided by
the device manufacturer or third parties. If these are provided in python, they may be used in place of a user-defined
driver or protocol class by using python's import function.

Device class files are saved in the Devices folder of a given project.

A Device class has two key requirements:
1. device_name: a string matching the filename
2. an __ init __ method that does not take any input arguments
3. the method set_flab() which passes a flab object/reference to a device

Example: DeviceTemplate

    from flab.Templates import DriverTemplate
    from flab.Templates import ProtocolTemplate
    import inspect
    
    class Device(DriverTemplate.Driver, ProtocolTemplate.Protocol):
    
        device_name = 'DeviceTemplate'
        protocol_name = 'ProtocolTemplate'
        driver_name = 'DriverTemplate'
        version = '2.0.1'
    
        def __init__(self):
            self.device_name = 'DeviceTemplate'
            self.protocol_name = 'ProtocolTemplate'
            self.driver_name = 'DriverTemplate'
    
        #returns the value of a Device attribute
        def get(self, attribute_name):
            return self.__getattribute__(attribute_name)
    
        #sets the value of a Device attribute
        def set(self, attribute_name, value):
            self.__setattr__(attribute_name, value)
    
        #returns the name of a Device
        def get_device_name(self):
            return self.device_name
    
        #sets the name of a Device
        def set_device_name(self, device_name):
            self.device_name = device_name
    
        #returns the flab object of a Device
        def get_flab(self):
            return self.flab
    
        #sets the flab object of a Device
        def set_flab(self, flab):
            self.flab = flab
    
        #returns the attributes of a Device in a list
        def list_attributes(self):
            variables = []
            for i in inspect.getmembers(self):
                if not inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                    variables.append(i[0])
            return variables
    
        #returns the methods of a Device in a list
        def list_methods(self):
            variables = []
            for i in inspect.getmembers(self):
                if inspect.ismethod(i[1]) and not inspect.ismethoddescriptor(i[1]) and not inspect.isbuiltin(i[1]) and not '__' in i[0]:
                    variables.append(i[0])
            return variables
    
        #returns the arguments of a method of a Device in a list
        def list_method_args(self,method_name):
            fullargspec = inspect.getfullargspec(self.get(method_name))
            return fullargspec

The Device class is primarily used for defining any configuration parameters that are specific to given use-case.
For example, the below Device class for controlling hotplates is used to specify default temperatures

Example: IkaDefaultsDevice

    #A Device class for IKA RCT Digital hotplates
    
    from Projects.Working.Devices.Drivers import IkaDriver
    from Projects.Working.Devices.Protocols import IkaProtocol
    
    class Device(IkaDriver.Driver, IkaProtocol.Protocol):
    
        device_name = 'IkaDefaultsDevice'
    
        #Default parameters
        default_temperature = 100
    
        def __init__(self):
            pass
    
        def set_default_temperature(self, new_default):
            self.default_temperature = new_default
    
        def get_default_temperature(self):
            return self.default_temperature

Use the flab method "load_device" to load a given device into the flab devices dictionary.
This dictionary can then be used to call upon device properties and functions.

Example: loading and using device

    flab.load_device('DeviceTemplate')
    flab.devices['DeviceTemplate'].hello_world()

    flab.load_device('IkaDefaultsDevice')
    flab.devices['IkaDefaultsDevice'].set_default_temperature(50)

If a change has been made to the ExampleDevice class, the device module may be dynamically reloaded
into flab.

Example: reloading and using device

    flab.reload_device('ExampleDevice')
    flab.devices['ExampleDevice'].example_function()

###Drivers

Unlike a Task, a Driver has relatively fewer requirements. A Driver must define:

1. driver_name: a string matching the filename
2. an __ init __ method that does not accept any arguments

Any other methods and variables are given by the programmer. A certain degree of expertise in digital communication is 
required to program drivers, which is not covered in this guide.

Example: DriverTemplate
    
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


Some equipment providers or third parties already provide drivers in python, which can be adapted. Below is a Driver
used for collecting data from Arduino Mega controllers using the pyfirmata library. 

Example: ArduinoMegaDriver
    
    #A class for driving Arduino Mega using the pyfirmata library (https://pypi.org/project/pyFirmata/)

    from pyfirmata import Arduino, util, ArduinoMega

    class Driver(ArduinoMega):
    
        port = 'NA'
        is_arduino_connected = False
        print_status = True
        driver_name = 'ArduinoMegaDriver'
        mega = {'digital': tuple(x for x in range(56)),'analog': tuple(x for x in range(16)),'pwm': tuple(x for x in range(2, 14)),'use_ports': True,'disabled': (0, 1, 14, 15)}
    
        def __init__(self):
            pass
    
        #set the communication port
        def set_port(self,port):
            self.port = port

        #get the communication port
        def get_port(self):
            return self.port
    
        #connect the arduino
        #the port must be defined before connecting the arduino
        def connect_arduino(self):
            if (not self.is_arduino_connected) and (self.port != 'NA'):
                try:
                    self.ard = Arduino(self.port)
                    self.ard.setup_layout(self.mega)
                    self.it = util.Iterator(self.ard)
                    self.it.start()
                    self.is_arduino_connected = True
                    if self.print_status:
                        self.flab.display('Arduino connected successfully')
                    return 0
                except Exception as e:
                    if self.print_status:
                        self.flab.display(str(e))
                        self.flab.display('Error connecting Arduino Mega. Check connection')
                    return e
                finally:
                    pass
            else:
                return 0

        #get if arduino is connected
        def get_arduino_connected(self):
            return self.is_arduino_connected

        #I define this here because pyfirmata does not actually return a voltage when a pin is read - it is a number between
        #0 to 1
        def get_voltage(self, pin):
            try:
                v = self.ard.analog[pin].read() * 5.0
            except Exception as e:
                v = -1
            finally:
                pass
            return v

Sometimes, it is necessary to completely define a driver from scratch. For serial communication, python's serial 
library can be used to create methods for communication. Below is an example of a Driver that defines serial communication
functions, and can be inherited by other drivers.

Example: SerialDriver

    #A generic class for drivers using serial communication.

    import serial
    import time

    class Driver():
    
        driver_name = 'SerialDriver'
    
        #default parameters
    
        port = 'NA'
        #ASCII character at the beginning of a transmission
        beg_char = '/'
        #ASCII character at ending of a transmission
        end_char = '\r'
        #time to pause after sending a transmission
        pause_time = 0.1
        bd = 9600
        to = 1
    
        def __init__(self):
            pass
    
        #set the current port
        def set_port(self, port):
            self.port = port
    
        #return the current port
        def get_port(self):
            return self.port
    
        # open serial communication
        def open_ser(self):
            try:
                self.ser = serial.Serial(port=self.port, baudrate=self.bd, timeout=self.to)
                return 0
            except Exception as e:
                print(e)
                return e
    
        # close serial communication
        def close_ser(self):
            self.ser.close()
    
        # check serial port
        def check_ser(self):
            check = self.ser.is_open
            return check
    
        #write a string message over the serial port
        def write(self,mess):
            try:
                write_str = self.beg_char + mess + self.end_char
                write_byt = write_str.encode()
                self.ser.write(write_byt)
                time.sleep(self.pause_time)
                self.ser.flushInput()
                self.ser.flushOutput()
                return 0
            except Exception as e:
                print(e)
                return e
    
        def read(self,nbyt):
            try:
                read_byt = self.ser.read(nbyt)
                read_str = str(read_byt.decode())
                return read_str
            except Exception as e:
                print(e)
                return ''
    
        #write and read (without flushing buffer)
        def write_read(self,mess,nbyt):
            try:
                write_str = self.beg_char + mess + self.end_char
                write_byt = write_str.encode()
                self.ser.write(write_byt)
                time.sleep(self.pause_time)
                read_byt = self.ser.read(nbyt)
                read_str = str(read_byt.decode())
                self.ser.flushInput()
                self.ser.flushOutput()
                return read_str
            except Exception as e:
                print(e)
                return ''
    
        #write and read (without flushing buffer)
        def write_readline(self,mess):
            try:
                write_str = self.beg_char + mess + self.end_char
                write_byt = write_str.encode()
                self.ser.write(write_byt)
                time.sleep(self.pause_time)
                read_byt = self.ser.readline()
                read_str = str(read_byt.decode())
                self.ser.flushInput()
                self.ser.flushOutput()
                return read_str
            except Exception as e:
                print(e)
                return ''

Below is an example of a driver for a hotplate that inherits the SerialDriver class to facilitate digital communications.
Serial commands for communication can often be found in the manuals of equipment.

Example: IkaDriver

    #A class for driving IKA RCT digital hotplate

    from Projects.Example.Devices.Drivers import SerialDriver

    class Driver(SerialDriver.Driver):
    
        driver_name = 'IkaDriver'
    
        port = 'NA'
        #ASCII character at the beginning of a transmission
        beg_char = '/'
        #ASCII character at ending of a transmission
        end_char = ' \r \n'
        #time to pause after sending a transmission
        pause_time = 0.1
        bd = 9600
        to = 1
    
        def __init__(self):
            super().__init__()
    
        def read_name(self):
            s = 'IN_NAME'
            r = self.write_read(s, 80)
            return r
    
        def read_external_sensor(self):
            s = 'IN_PV_1'
            r = self.write_read(s, 80)
            return r[:len(r)-4]
    
        def read_hotplate_sensor(self):
            s = 'IN_PV_2'
            r = self.write_read(s, 80)
            return r[:len(r)-4]
    
        def read_stirring_speed(self):
            s = 'IN_PV_4'
            r = self.write_read(s, 80)
            return r
    
        def read_temperature_setpoint(self):
            s = 'IN_SP_1'
            r = self.write_read(s, 80)
            return r[:len(r)-4]
    
        def read_safety_temperature_setpoint(self):
            s = 'IN_SP_3'
            r = self.write_read(s, 80)
            return r
    
        def read_stirring_speed_setpoint(self):
            s = 'IN_SP_4'
            r = self.write_read(s, 80)
            return r[:len(r)-4]
    
        def set_temperature(self, t):
            s = 'OUT_SP_1 ' + str(t)
            r = self.write(s)
    
        def set_stirring_speed(self, rpm):
            s = 'OUT_SP_4 ' + str(rpm)
            r = self.write(s)
    
        def start_heater(self):
            s = 'START_1'
            r = self.write(s)
    
        def stop_heater(self):
            s = 'STOP_1'
            r = self.write(s)
    
        def start_stirring(self):
            s = 'START_4'
            r = self.write(s)
    
        def stop_stirring(self):
            s = 'STOP_4'
            r = self.write(s)
    
        def reset(self):
            s = 'RESET'
            r = self.write(s)
    
        def set_operating_mode(self, mode):
            if mode == 'A' or mode == 'B' or mode == 'D':
                s = 'SET_MODE_' + mode
                r = self.write(s)
                return mode
            else:
                return -1
    
        def set_echo_safety_temperature(self,t):
            s = 'OUT_SP_12@' + str(t)
            r = self.write_read(s, 80)
            return r
    
        def set_echo_safety_stirring_speed(self,rpm):
            s = 'OUT_SP_42@' + str(rpm)
            r = self.write_read(s, 80)
            return r
    
        def watchdog_one(self, m):
            s = 'OUT_WD1@' + str(m)
            r = self.write(s)
    
        def watchdog_two(self, m):
            s = 'OUT_WD2@m' + str(m)
            r = self.write(s)

###Protocols

A Protocol class provides higher level functions that define the actions a device will take in a project. Protocols
will often utilize the functions defined in a given Driver class. It is good practice to note which Driver class a 
Protocol is compatible with.

A protocol requires:
1. protocol_name: a string matching the filename
2. an __ init __ method that does not accept any arguments

Example: ProtocolTemplate

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

Protocols can also define how a given device is initialized, and how the user may interact with the device. For example
in the below protocol for hotplates, additional code is given to ensure a robust connection and startup of the device.

Example: IkaProtocol

    #A class for IKA RCT Digital hotpolate protocols

    class Protocol():
    
        protocol_name = 'IkaProtocol'
        print_status = True
    
        con_status = False  # is IKA connected (serial port)
        ini_status = False  # is IKA initialized
    
        def __init__(self):
            pass
    
        def connect(self):
            con_err = ""
            if self.get_port() == 'NA':
                con_err = con_err + "Ika port not assigned."
            else:
                try:
                    self.open_ser()
                    self.check_ser()
                except Exception as e:
                    con_err = con_err + "Ika connection error. Check port assignment."
                    self.display_status(con_err)
            if con_err == '':
                self.con_status = True
                self.display_status("Ika connected successfully.")
            return self.con_status
    
        #Initialize the hotplate by reading its name
        def initialize(self):
            ini_err = ''
            if self.con_status:
                if not self.ini_status:
                    try:
                        name = self.read_name()
                        if name == '':
                            self.ini_status = False
                            self.display_status("Ika initialization faiulre: check device")
                        else:
                            self.ini_status = True
                            self.display_status("Ika initialized successfully")
                            self.display_status(name)
                    except:
                        ini_err = "Ika initialization failure: check serial connection."
                        self.display_status(ini_err)
                        self.ini_status = False
            else:
                ini_err = 'Ika initialization failure: not connected.'
                self.display_status(ini_err)
                self.ini_status = False
    
            return self.ini_status
    
        def display_status(self, s):
            if self.printstatus:
                self.flab.display(s)

Finally, designing a task which utilizes a device requires correct usage of the underlying Device, Driver and Protocol
classes. See below the task "LoadStartIka", which automatically loads, initializes and starts a hotplate.

Example: LoadStartIka

    #A task for loading, initializing and starting a IKA RCT Digital hotplate with a default temperature
    
    class Task():
    
        task_name = 'LoadStartIka'
        task_type = 'thread'
        task_stopped = False
    
        #initialize all tasks with a flab object.
        def __init__(self, flab):
            self.flab = flab
    
        #method called when task is run
        def run(self):
            self.task_stopped = False
            load_err = ''
            try:
                #load the device into flab
                self.flab.load_device('IkaDefaultsDevice')
                p = self.flab.devices['IkaDefaultsDevice']
                #set the device port
                p.set_port('/dev/tty.usbmodem7_____SM96_s_Q1')
                #set the device temperature
                p.set_temperature(p.default_temperature)
                #start the heater
                p.start_heater() 
            except Exception as e:
                load_err = 'Error loading and starting IkaDefaultsDevice'
                self.flab.ui.print(load_err)
                self.flab.ui.print(e)
            finally:
                pass
            if load_err == '':
                self.flab.ui.print('IkaDefaultsDevice loaded and started successfully')
    
        def stop(self):
            self.task_stopped = True
            self.flab.devices['IkaDefaultsDevice'].start_heater() 

## UIs

UIs are classes that govern how users (humans or otherwise) interact with running programs. The most common UI is graphical
(a GUI). A UI can be thought of as a hybrid between a Device and a Task. UI classes are saved in the UIs folder of a project.

Each UI requires the following:

1. ui_name: a string that matches the filename
2. __ init __(self, flab): initializes the UI object with the shared flab object
3. run(self, *args, **kwargs): this defines how a ui runs. This method can contain while loops, which
       can be externally closed with the flag task_stopped.
4. stop(self, *args, **kwargs): this defines how a ui stops. This method can be used to modify a ui_stopped
   flag
   
UIs inherit classes stored in the Designs and Actions folders, which describe the layout of the UI and the corresponding
actions of the UI elements respectively.

In HelloWorldUI, the UI class inherits the Ui_MainWindow class of HelloWorldDesign and the Actions class of HelloWorldActions.
The HelloWorldUI run method uses PyQt5 to create a window (QtWidgets.QMainWindow) to run in.
Note: GUI libraries typically run within the main method. If you wish to start multiple UIs or to run a UI in a separate task,
it is best to create a separate process task for running the UI.

Example: HelloWorldUI
    
    #A GUI for HelloWorld

    from Projects.Example.UIs.Designs import HelloWorldDesign
    from Projects.Example.UIs.Actions import HelloWorldActions
    from PyQt5 import QtWidgets

    import sys

    class UI(HelloWorldDesign.Ui_MainWindow, HelloWorldActions.Actions):
    
        ui_name = 'HelloWorldUI'
    
        def __init__(self, flab):
            self.flab = flab
    
        #The method responsible for starting the UI
        def run(self):
            app = QtWidgets.QApplication(sys.argv)
            self.MainWindow = QtWidgets.QMainWindow()
            self.setupUi(self.MainWindow)
            self.configure_actions()
            self.MainWindow.show()
            app.exec_()
    
    
        #The method responsible for stopping the UI
        def stop(self):
            pass

UIs may be loaded into flab with the flab method load_ui(ui_name)

    flab = Flab.Flab()
    flab.load_ui('HelloWorldUi')
    flab.uis['HelloWorldUi'].run()

###Designs

Design classes may be created by a range of methods - by directly coding, using libraries such as Tkinter, or through applications
like QtDesigner. Design class files are stored in the Designs folder. 
*.ui files can be converted to *.py files automatically using the function convert_ui(ui_name), which is defined in UiManager.

Example: .ui to .py conversion.    

    flab = Flab.Flab()
    flab.convert_ui(''HelloWorldUi')

Example: HelloWorldDesign

    # -*- coding: utf-8 -*-

    # Form implementation generated from reading ui file '/Users/nicholasjose/Dropbox (Cambridge CARES)/Python/pyflab/Projects/Working/UIs/Designs/HelloWorldDesign.ui'
    #
    # Created by: PyQt5 UI code generator 5.15.4
    #
    # WARNING: Any manual changes made to this file will be lost when pyuic5 is
    # run again.  Do not edit this file unless you know what you are doing.

    from PyQt5 import QtCore, QtGui, QtWidgets
     
    class Ui_MainWindow(object):
        def setupUi(self, MainWindow):
            MainWindow.setObjectName("MainWindow")
            MainWindow.resize(1068, 716)
            self.centralwidget = QtWidgets.QWidget(MainWindow)
            self.centralwidget.setObjectName("centralwidget")
            self.label = QtWidgets.QLabel(self.centralwidget)
            self.label.setGeometry(QtCore.QRect(390, 330, 91, 16))
            self.label.setObjectName("label")
            self.pushButton = QtWidgets.QPushButton(self.centralwidget)
            self.pushButton.setGeometry(QtCore.QRect(370, 360, 113, 32))
            self.pushButton.setObjectName("pushButton")
            MainWindow.setCentralWidget(self.centralwidget)
            self.statusbar = QtWidgets.QStatusBar(MainWindow)
            self.statusbar.setObjectName("statusbar")
            MainWindow.setStatusBar(self.statusbar)
    
            self.retranslateUi(MainWindow)
            QtCore.QMetaObject.connectSlotsByName(MainWindow)
    
        def retranslateUi(self, MainWindow):
            _translate = QtCore.QCoreApplication.translate
            MainWindow.setWindowTitle(_translate("MainWindow", "Hello World"))
            self.label.setText(_translate("MainWindow", "Hello What?"))
            self.pushButton.setText(_translate("MainWindow", "Click me"))


###Actions

Action classes are used to define the actions that a UI undertakes after events. For example, in HelloWorldDesign,
to define what happens after pushButton is clicked.
Actions are defined in separate classes to enable programmers to easily change actions without affecting the UI's design,
and vice versa.

Each Actions class is defined with:
1. actions_name: a string matching the class filename
2. an __ init __ function that accepts a flab object as an input.

In the below example, upon clicking pushButton, defined within HelloWorldDesign, the test of label, also defined with 
HelloWorldDesign, displays "Hello World"

Actions Example:

    #Hello World UI Actions

    class Actions():
    
        actions_name = 'HelloWorldActions'
    
        def __init__(self, flab):
            self.flab = flab
    
        def configure_actions(self):
            self.pushButton.clicked.connect(self.hello_world)
    
        def hello_world(self):
            self.label.setText('Hello World')

## Boot

Boot scripts are used to start programs. The BootManager class implements Python's multiprocessing SyncManager class to
create the shared flab object, using namespaces and queues.

Every flab object must be initialized with queues, which are used to exchange information between separate "flab" process and "ui"
processes. These queues may or may not further used by the programmer, depending on the complexity of the program.

The flab queue stores commands for processes that execute actions within the flab environment (e.g. controlling devices).
The UI queue stores commands or strings for UI processes to execute or display

Before starting any specific code for your project, use the following steps to create a shared flab object

1. Create a BootManager object
2. Create a UI queue and a flab queue
3. Create a shared flab object using boot_manager.create_flab_proxy(ui_queue, flab_queue)

These steps are illustrated in the below example, which starts HelloWorldUI

Note: in V1.0.7+ the working directory does not need to be changed within the bootscript

Example: HelloWorldBoot

    from flab import BootManager
    import os
    
    if __name__ == '__main__':

        #1. create a boot_manager
        boot_manager = BootManager.BootManager()
    
        #2. create the queues
        ui_queue = boot_manager.create_queue()
        flab_queue = boot_manager.create_queue()
    
        #3. create a flab object proxy
        f = boot_manager.create_flab_proxy(ui_queue = ui_queue, flab_queue = flab_queue)
    
        #convert and run HelloWorldUI
        f.convert_ui('HelloWorldDesign')
        f.load_ui('HelloWorldUi')
        f.uis['HelloWorldUi'].run()

BootManager also contains separate functions for starting processes (start_process and start_processes), which can be used
to start multiple running processes from the boot script. This is illustrated in the Console Project, below.

## The Console Project

The Console Project is essentially a user input console that allows you to access the flab object and run tasks in real time.
This is extremely useful for quickly prototyping code, as you do not need to restart python each time you need to modify a task.
Instead, you can simply change a task, save the file, "reload" the task in flab, and start it.

The Console takes only flab commands as inputs. For example

    flab.start_task('HelloWorld')

becomes
    
    >start_task('Hello World')

the display method can be used to print out data in the console. For example

    >display('Hello World')

displays

    'Hello World'

If you wish to print out attributes, for example, the items in a flab dictionary or a flab variable, you need to use

    >display(flab.attribute)

for example

    >display(flab)

outputs

    <flab.Flab.Flab object at 0x7fafde453fa0>

and

    >display(flab.tasks)

outputs

    {'ConsoleUiProcess': <Projects.Console.Tasks.ConsoleUiProcess.Task object at 0x7f88dbd68ac0>,
    'ConsoleFlabProcess': <Projects.Console.Tasks.ConsoleFlabProcess.Task object at 0x7f88dbd68c10>, 
    'HelloWorld': <Projects.Console.Tasks.HelloWorld.Task object at 0x7f88dbd5f850>}

## Quick Start

To quickly get started with flab using Console:

1. Install the FLab package
2. Create a Projects directory
3. Download the Console Project from github, and copy it into your Projects folder.
4. Run ConsoleBoot.py from the Boot folder
5. Type in start_task('HelloWorld'). You should see repeated lines of 'Hello World' printed
6. Type in stop_task('HelloWorld'). The printing should stop.

#The Console2 Project
Console2 is an expansion of Console, and contains buttons for easy access to flab methods, and text browsers that display
the properties of devices, variables and running tasks.

More documentation on the use of Console2 will be uploaded soon.