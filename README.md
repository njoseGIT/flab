# flab

Author: Nicholas A. Jose

For code documentation, go to https://flab.readthedocs.io/en/latest/.
This is currently under revision since the release of 3.0.

## Recent Updates
1.0.0: Device objects have publicly accessible attributes and methods.

1.0.7: Resolution of bug in booting. Boot script no longer requires changing of directories.

1.1.0: Resolved issues in closing flab and multiprocessing. Requires Python 3.10 or later

1.1.1: Resolved issue in listing tasks

2.0.0: BootManager contains functionality for network communication. Flab objects are now initialized with queues as 
optional arguments. TaskManager no longer implements QThread (as a "QTask") such that
flab is no longer dependent on PyQT. Templates are now included within flab.Templates. These are DeviceTemplate, DriverTemplate
and ProtocolTemplate, which may be inherited by Device classes.

2.0.1: 
- Resolved bug in distribution

2.0.2: 
- Docstrings created 

2.0.3: 
- Docstrings amended

2.0.4/2.0.5: 
- Setup file amended

2.0.6/7: 
- Resolved bug in Flab inheritance

3.0.0: 
 - Resolved issues in reloading of devices. 
 - Added ModelManager, DataManager and EnvironmentManager.
 - Added ModelTemplate and DataTemplate
 - Removal of Driver/Protocol inheritance in Devices for simplicity
 - Shared classes (Task, Device, etc.) init methods not required anymore

3.0.1: 
 - Bug fixes in object loading and console actions
 - Updated documentation
 - Added Devices:
   - AgilentLC
   - ArduinoMegaDevice
   - AvantesDevice
   - BronkhorstDevice   
   - HarvardPump33DDS
   - IkaRCTDigital
   - KnauerPump
   - SerialDevice
   - ShimadzuLC
   - UsbcamDevice
    
 - Added Tasks
   - IkaRCTDigital_Connect.py
   - IkaRCTDigital_Disconnect.py
   - IkaRCTDigital_Initialize.py
   - IkaRCTDigital_SetStirringSpeed.py
   - IkaRCTDigital_SetTemperature.py
   - IkaRCTDigital_StartStirring.py
   - IkaRCTDigital_StopStirring.py
   - KnauerPump_Connect.py
   - KnauerPump_Disconnect.py
   - KnauerPump_DoseVolume.py
   - KnauerPump_Initialize.py
   - KnauerPump_ReadFlowrateSetpoint.py
   - KnauerPump_SetFlowrate.py
   - KnauerPump_StartPumping.py
   - KnauerPump_StartTimedPump.py
   - KnauerPump_StopPumping.py
   - HarvardPump33DDS_Connect.py
   - HarvardPump33DDS_Disconnect.py
   - HarvardPump33DDS_Initialize.py
   - HarvardPump33DDS_StartInfusing.py
   - HarvardPump33DDS_StopPumping.py
    
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

## Flab Installation

To install flab, enter into the terminal:

    python3 -m pip install flab

## Flab Console

We recommend the use of Flab Console to manage the flab environment.
Flab Console provides a graphical user interface for sending flab commands and visualize all objects present. 
This is extremely useful for quickly prototyping code, as you do not need to restart python each time you need to modify a task.
Instead, you can simply change your code, save the file, "reload" the class in flab, and start it.

The Console Command Line takes only flab commands as inputs. For example

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

1. Clone the flab repository on Github
2. create a virtual environment and install the following dependencies, which are also given in flab_console_requirements.txt.
- setuptools==65.5.0
- pip==22.3.1
- PyQt5-sip==12.15.0
- PyQt5-Qt5==5.15.15
- PyQt5==5.15.11
- numpy==2.1.1
- wheel==0.43.0 
- pyqtgraph==0.12.3

## Directory structure
Before beginning any project with Flab, the working directory must be set up properly.
The working directory has the following structure. All projects are stored in the "Projects" folder. Any other code 
 or other files can also be kept in this working directory.

    Working_directory/
    
    │  ├ Projects/
    
    │  │  ├ example_project_1/ 
    
    │  │  └ example_project_2/
    
    │  └ Other_folders/


A project directory has the following structure: 

    example_project/
    
    ├ Tasks/

    ├ Devices/
    
    ├ UIs/

    ├ Models/

    └ Data/

A project directory may be automatically created using flab's create_project_directory() method

## Flab Objects

A Flab object acts as a space for the shared storage of:
1. devices (in the devices dictionary)
2. tasks (in the tasks dictionary)
3. variables (in the vars dictionary), 
4. modules (in the modules dictionary)
5. user interfaces (in the uis dictionary)
6. models (in the models dictionary)
7. data (in the data dictionary)

The Flab class inherits DeviceManager, TaskManager, UiManager, ModelManager and DataManager, such that methods in those classes may be easily 
customized. These managers contain methods for manipulating devices, tasks, ui's, models and data.

## Tasks

Tasks are essentially routines or programs, which can be run in a variety of fashions depending on user input. Task files
are saved as python files with the Tasks folder of a project.

To run a Task in Flab Console, each Task should inherit the TaskTemplate. This is provided in the Templates module.

Each task requires two attributes:

1. task_name: a string that matches the filename
2. task_type: a string that determines how the task is run. Either "thread", "asyncio" or "process"

Each task requires two methods:

1. run: this is called when flab.start_task is called. This method can contain while loops, which
       can be externally closed with the flag task_stopped.
2. stop: this is called when flab.stop_task is called. This method can be used to modify the a flag to stop the task 
or to run a shut-down procedure.

Tasks must be first loaded into flab with the load_task(task_name) method. They may then be started or stopped using the 
start_task(task_name, *args, **kwargs) and stop_task(task_name, *args, **kwargs) methods.
Multiple tasks can be loaded simulataneously with the flab.load_tasks method. All the tasks in a given project can be loaded 
using flab.load_all_tasks(). Tasks can also be dynamically reloaded by using the reload_task and reload_tasks 
methods. All tasks may be stopped in one line with the command "flab.stop_all_tasks()". Task objects do not have publicly accessible
attributes.
Example usage:

    flab.load_task('HelloWorld')
    flab.start_task('HelloWorld')
    flab.stop_task('HeloWorld')
    flab.reload_task()

###Threaded Tasks

By default,
all tasks are "threads" -- meaning that they run on a single CPU and are essentially "queued." See python's threading library
for a more detailed description.

Threaded Task Example:

    #Import the required libraries
    import time

    #Import the task template from flab.Templates
    from flab.Templates import TaskTemplate

    #Create the Task class, inheriting TaskTemplate.Task
    class Task(TaskTemplate.Task):

    #Define the name of the task. This should match the filename
    task_name = 'HelloWorld'

    #Define the type of the task. This is either 'thread' , 'process' or 'asyncio'
    task_type = 'thread'


    #define the run method, with any necessary and optional arguments (i.e. args, kwargs)
    def run(self, mandatory_argument, optional_argument = 'optional argument'):
        try:

            #print out Hello World + the mandatory argument in the system command line/terminal
            print('1. Hello World: ' + str(mandatory_argument))

            #display Hello World + the mandatory argument in the console command line
            self.flab.display('2. Hello World: ' + str(mandatory_argument) + ' ' + str(optional_argument))

            #create a shared variable called 'World' with the value 'Hello'
            self.flab.add_var('Hello', 'World')

            #display the shared variable called 'World' in the console command line
            self.flab.vars['count'] = 0
            self.flab.display('3. ' + str(self.flab.vars['count']))

            #create a shared variable called 'HelloWorld_stopped' with the value False
            self.flab.vars['HelloWorld_stopped'] = False

            #while the variable 'HelloWorld_stopped' is False, loop over a section of code
            while not self.flab.vars['HelloWorld_stopped']:
                #display 'Hello World' + mandatory argument in the console
                self.flab.display('4. Hello World: ' + str(mandatory_argument))
                #sleep for a second
                time.sleep(1)
        except Exception as e:
            self.flab.display('Error in HelloWorld')
            self.flab.display(e)
        finally:
            pass

    #define the method to be called when the task is stopped
    def stop(self):
        #set the variable 'HelloWorld_stopped' to True
        self.flab.vars['HelloWorld_stopped'] = True #a flag to stop the script

###Asyncio Tasks

An asynchronous task can be used to make running some routines more efficient. This utilizes
python's asyncio library. Asyncio tasks run in an asyncio loop, which is started by running flab.start_asyncio_loop().
Flab Console automatically starts the asyncio loop upon startup, which is visible from the "task bar".

An asyncio task has several key differences to a threaded task:
1. the asyncio library must be imported
2. task_type = 'asyncio'
3. run and stop methods must be defined with an "async" prefix, shown below:
    
    
    async def run(self):...
    
    async def stop(self):...

4. instead of using python's time.sleep(seconds) method for blocking, use:

    await asyncio.sleep(seconds)

Asyncio Task Example:

    from flab.Templates import TaskTemplate
    import asyncio
    
    class Task(TaskTemplate.Task):
    
        task_name = 'HelloWorld_asyncio'
        task_type = 'asyncio'
        task_stopped = False
        argument_descriptions = {'optional_argument': 'an optional argument', 'mandatory_argument': 'a mandatory argument'}
    
        async def run(self):
            try:
                self.flab.vars['HelloWorld_asyncio_stopped'] = False # a flag to stop the script
                # loop the display of 'Hello World' until the user stops the task.
                while not self.flab.vars['HelloWorld_asyncio_stopped']:
                    self.flab.display('Hello World')
                    await asyncio.sleep(1)
            except Exception as e:
                self.flab.display('Error in ' + self.task_name)
                self.flab.display(e)
    
        async def stop(self):
            self.flab.vars['HelloWorld_asyncio_stopped'] = True #a flag to stop the script
            self.flab.display('HelloWorld_asyncio stopped')


###Process Tasks

Process tasks are executing using Python's multiprocessing library, meaning that they are distributed across different CPUs.
This distribution makes the sharing of data i.e. flab slightly more complicated. A process would be used if the task is CPU bound,
or if the task needs to run as the parent process, such as GUI applications.

A process task has several key differences to a threaded task:
1. task_type = 'process'

Process Example:

    from flab.Templates import TaskTemplate

    #This task prints 'Hello World' every second within a separate process
    #A flab variable self.flab.vars['HelloWorldProcess_stopped'] is used instead of a Boolean flag within the Task so that external 
    other processes can signal this process to stop

    class Task(TaskTemplate.Task):

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

To digitally represent the properties and actions of a device, this can include:

1. How a computer digitally communicates with the device, explicitly defined in the Driver class.
2. How a device is used within a given task, explicitly defined in the Protocol class.
3. The specific configuration of the device, explicitly defined in the Device class.

Device class files are saved in the Devices folder of a given project.

A Device class must be defined with the following attribute:
1. device_name: a string matching the filename 

The Device class should also inherit from flab.Templates, DeviceTemplate.Device, to run properly in Console.

Use the flab method "load_device" to load a given device into the flab devices dictionary.
This dictionary can then be used to call upon device properties and functions.

Example: loading and using device

    flab.load_device('ExampleDevice')
    flab.devices['ExampleDevice'].set_default_temperature(50)

If a change has been made to the ExampleDevice class, the device module may be dynamically reloaded
into flab.

Example: reloading and using device

    flab.reload_device('ExampleDevice')
    flab.devices['ExampleDevice'].set_temperature(50)

To get or change the attributes of a device (or any other shared flab object) outside of the object class itself,
one should use the 'get' and 'set' methods. Doing this ensures that the correct value is returned - otherwise, the default value 
may be returned.

Example:

    use:

    temperature = flab.devices['ExampleDevice'].get('setpoint_temperature')
    flab.devices['ExampleDevice'.set('setpoint_temperature',5)

    instead of:

    temperature = flab.devices['ExampleDevice'].setpoint_temperature
    flab.devices['ExampleDevice'].setpoint_temperature = 5)

Some equipment providers or third parties already provide drivers in python, which can be adapted. Below is a Device
used for collecting data from Arduino Mega controllers using the pyfirmata library. 

Example: ArduinoMegaDevice
    
    from pyfirmata import Arduino, util, ArduinoMega
    from flab.Templates import DeviceTemplate
    
    class Device(DeviceTemplate.Device):
        """
        A class for driving Arduino Mega using the pyfirmata library (https://pypi.org/project/pyFirmata/)
        """

    port = 'NA' #arduino serial port [str]
    is_arduino_connected = False #boolean indicating if the arduino is connected [str]
    print_status = True #boolean indicating if the status of the arduino should be printed [str]
    driver_name = 'ArduinoMega' #name of the driver [str]
    mega = {'digital': tuple(x for x in range(56)),
            'analog': tuple(x for x in range(16)),
            'pwm': tuple(x for x in range(2, 14)),
            'use_ports': True,
            'disabled': (0, 1, 14, 15)} #properties of the arduino

    def set_port(self,port):
        """
        Sets the serial port

        :param port: the serial port
        :type port: str
        :returns: None
        """
        self.port = port


    def get_port(self):
        """
        Returns the serial port

        :returns: str
        """
        return self.port

    def connect_arduino(self):
        """
        Initializes communication with the arduino. the serial port must be set.

        :returns: 0 if the arduino connects successfully, exception if it doesn't
        """
        if not self.is_arduino_connected and self.port != 'NA':
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

    def get_voltage(self, pin):
        """
        returns the voltage of an analog pin. If there is an error, the voltage returned is 0.

        :param pin: pin number (between 1 and 16)
        :type pin: int

        :returns: double
        """
        try:
            v = self.ard.analog[pin].read() * 5.0
        except Exception as e:
            v = -1
        finally:
            pass
        return v

    def get_arduino_connected(self):
        """
        Checks if the arduino is communicating

        :returns: boolean
        """
        return self.is_arduino_connected


Sometimes, it is necessary to completely define a device from scratch. For serial communication, python's serial 
library can be used to create methods for communication. Below is an example of a Device that defines serial communication
functions, and can be inherited by other devices.

Example: SerialDevice

    #A generic class for devices using serial communication.

    import serial
    import time
    from flab.Templates import DeviceTemplate

    class Device(DeviceTemplate.Device):
    
        device_name = 'SerialDevice'
    
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

Below is an example of a device for a hotplate that inherits the SerialDevice class to facilitate digital communications.
Serial commands for communication can often be found in the manuals of equipment.

Example: IkaDriver

    #A class for driving IKA RCT digital hotplate

    from Projects.Example.Devices import SerialDevice

    class Driver(SerialDevice.Device):
    
        device_name = 'IkaDevice'
    
        con_status = False  # is IKA connected (serial port)
        ini_status = False  # is IKA initialized
        port = 'NA'
        #ASCII character at the beginning of a transmission
        beg_char = '/'
        #ASCII character at ending of a transmission
        end_char = ' \r \n'
        #time to pause after sending a transmission
        pause_time = 0.1
        bd = 9600
        to = 1
    
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

Finally, designing a task which utilizes a device requires correct usage of the underlying Device
classes. See below the task "LoadStartIka", which automatically loads, initializes and starts a hotplate.

Example: LoadStartIka

    #A task for loading, initializing and starting a IKA RCT Digital hotplate with a default temperature
    
    class Task():
    
        task_name = 'LoadStartIka'
        task_type = 'thread'
    
        #method called when task is run
        def run(self):
            load_err = ''
            try:
                self.flab.vars['LoadStartIka_stopped'] = False
                #load the device into flab
                self.flab.load_device('IkaDevice')
                p = self.flab.devices['IkaDevice']
                #set the device port
                p.set_port('/dev/tty.usbmodem7_____SM96_s_Q1')
                #set the device temperature
                p.set_temperature(50)
                #start the heater
                p.start_heater() 
            except Exception as e:
                load_err = 'Error loading and starting IkaDevice'
                self.flab.ui.print(load_err)
                self.flab.ui.print(e)
            finally:
                pass
            if load_err == '':
                self.flab.ui.print('IkaDevice loaded and started successfully')
    
        def stop(self):
            self.set_temperature(25)
            self.flab.vars['LoadStartIka_stopped'] = True 

## UIs

UIs are classes that govern how users (humans or otherwise) interact with running programs. The most common UI is graphical
(a GUI). A UI can be thought of as a hybrid between a Device and a Task. UI classes are saved in the UIs folder of a project.
The Ui class should also inherit from flab.Templates, UiTemplate.Ui, to run properly in Console.

Each UI requires the following attributes and methods:

1. ui_name: an attribute that is a string that matches the filename
3. run: this method defines how a ui runs. This method can contain while loops, which
       can be externally closed with a user defined flag
4. stop: this method defines how a ui stops. This method can be used to modify a user defined flag
   
UIs contain functions and attributes that describe the layout of the UI and the corresponding
actions of the UI elements respectively.

In HelloWorldUI, the UI class uses Tkinter 

Example: HelloWorldTkinterUi.py
    
    import tkinter as tk
    from flab.Templates import UiTemplate
    
    class Ui(UiTemplate.Ui):
    
        ui_name = 'HelloWorldTkinterUi'
    
        def __init__(self):
            self.window = None
    
        def run(self):
            # Create a new tkinter window
            self.window = tk.Tk()
            # Set a variable name
            self.flab.vars.update({'Hello':'World'})
            # Set the window title to a variable value
            self.window.title(str(self.flab.vars['Hello']))
            # Create a label widget to display the text
            self.label = tk.Label(self.window, text="Hello, World!")
            # Pack the label widget into the window
            self.label.pack()
            # Start the tkinter event loop
            self.window.mainloop()
    
        def stop(self):
            pass


UIs may be loaded into flab with the flab method load_ui(ui_name).

The run and stop methods of the UIs may be accessed with 'start_ui' and 'stop_ui' methods from flab.
We recommend that UIs should normally be closed using the window itself rather than programmatically through the
'stop' method. Rather, this should be used as a flag to stop other running classes and run shutdown routines.

    flab.load_ui('HelloWorldUi')
    flab.start_ui('HelloWorldUi')
    flab.stop_ui('HelloWorldUi')

## Data

Data classes contain attributes and methods for accessing stored data. It is important to note that Data classes
do not store data themselves. Data is primarily stored by accessing flab variables, either writing to them or reading from them.

Each Data class requires the following attributes and methods:
1. data_name: an attribute that is a string that matches the filename
2. update_variable: a method that describes how variables are updated from stored data.
3. update_file: a method that describes how a files, databases, etc. are updated from a flab variable.

For example: JsonDataExample, a class which access data in a json formatted file, with a flab variable named 'json_data'

    from flab.Templates import DataTemplate
    import os
    import json
    
    class Data(DataTemplate.Data):
    
        data_name = 'JsonDataExample' #name of the data object
    
        file_path = os.getcwd() + '\\Files\\example.json' # path of the file
        variable_names = ['json_data']  # names of variables that are stored
    
        def update_variable(self):
            """
            reads the json from the file path and coverts to a dictionary, and updates the variables dictionary
    
            Example:
    
                json:
                {
                    "a": [
                        1,
                        2,
                        3
                    ]
                }
    
                variables:
                {'a': [1, 2, 3]}
    
            :returns: None
            """
            try:
                with open(self.file_path, 'r') as file:
                    data_dict = json.load(file)
                    self.flab.vars.update(data_dict)
    
            except Exception as e:
                self.flab.display('Error in updating variable of ' + self.data_name)
                self.flab.display(e)
    
            finally:
                pass
    
        def update_file(self):
            """
            Updates the json file with the values of the variables
    
            Example:
    
                variables:
                {'a': [1, 2, 3]}
    
                json:
                {
                    "a": [
                        1,
                        2,
                        3
                    ]
                }
    
            """
    
            try:
                # get the sub-dictionary of variables to write
                subset_dict = {key: self.flab.vars[key] for key in self.variable_names}
                with open(self.file_path, 'w') as file:
                    json.dump(subset_dict, file, indent=4)
    
            except Exception as e:
                self.flab.display('Error in updating file of ' + self.data_name)
                self.flab.display(e)
    
            finally:
                pass

To use a Data object's methods, use the flab methods 'update_data_variable' and 'update_data_file', for example:

    flab.update_data_variable('JsonDataExample')
    flab.update_data_file('JsonDataExample')

Data classes can be loaded nad reloaded like all other objects, for example:

    flab.load('JsonDataExample')
    flab.reload('JsonDataExample')

## Model

Model classes represent attributes and methods for creating, training, running and evaluating models.
These Model classes can be used for a wide range modelling activities, from digital twins to machine learning models.

Each Model class requires the following attributes and methods:
1. model_name: this attribute is a string that matches the filename
2. train_model: this method describes how the model is trained.
3. predict_model: this method describes how a model makes a prediction
4. evaluate_model: this method describes how a model is evaluated, for example, goodness of fit

For example: LinearModelExample, a class which applies a linear regression model to a dataset (x and y).

    from flab3.Templates import ModelTemplate
    from sklearn.metrics import mean_squared_error, r2_score
    from sklearn.model_selection import cross_val_predict
    from sklearn.linear_model import LinearRegression
    
    class Model(ModelTemplate.Model):
    
        model_name = 'LinearModelExample' #name of the data object
        x = [[1], [2], [3]] # x data
        y = [1.1,2.4,3.8] # y data (actual)
        cross_validation_folds = 3 # number of cross-validation folds for evaluation
    
        def initialize(self):
            """
            Create a LinearRegression model.
    
            :returns: None
            """
    
            self.model = LinearRegression()
    
        def train(self):
            """
            Fits the data to a line
    
            :returns: None
            """
            try:
                # Fit the model to the training data
                self.model.fit(self.x, self.y)
    
            except Exception as e:
                self.flab.display('Error in training of ' + self.model_name)
                self.flab.display(e)
    
            finally:
                pass
    
    
        def predict(self, x_values):
            """
            Makes a model prediction with given x values
    
            :returns: predicted y values
            :rtype: list
            """
            try:
                y_prediction = []
                x_values = [[value] for value in x_values]
                y_prediction = self.model.predict(x_values)
                self.flab.display(y_prediction)
    
            except Exception as e:
                self.flab.display('Error in prediction of ' + self.model_name)
                self.flab.display(e)
    
            finally:
                return y_prediction
    
        def evaluate(self):
            """
            Evaluates the model accuracy in terms of mean squared error and R^2.
    
            :returns: mean squared error, R^2 value
            :rtype: tuple
            """
            try:
                model_mean_squared_error = -1
                model_r2 = -1
    
                # Perform cross-validation
                y_predicted = cross_val_predict(self.model, self.x, self.y, cv=self.cross_validation_folds)
    
                # Calculate performance metrics
                model_mean_squared_error = mean_squared_error(self.y, y_predicted)
                model_r2 = r2_score(self.y, y_predicted)
    
            except Exception as e:
                self.flab.display('Error in training of ' + self.model_name)
                self.flab.display(e)
    
            finally:
                return model_mean_squared_error, model_r2

To use a Model's methods, use the flab methods 'train', 'predict' and 'evaluate' for example:

    flab.train_model('JsonDataExample')
    flab.update_data_file('JsonDataExample')

Data classes can be loaded nad reloaded like all other objects, for example:

    flab.load('JsonDataExample')
    flab.reload('JsonDataExample')

# MyFirstProject

Coming soon!