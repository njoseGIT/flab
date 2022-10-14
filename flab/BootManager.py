# Flab
# BootManager
# Version 2.0.2
# Published XX-XXX-XXXX
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The BootManager module contains classes that are used to configure flab environments, in which devices,
variables and tasks may be synchronized between different processes and threads.
A few configurations are possible, depending on the desired application, which are specified
in the init method.
"""

from flab import Flab
from multiprocessing import Process, Queue
from multiprocessing.managers import NamespaceProxy, SyncManager, Namespace
import types
import sys
import os


class BootManager:
    """BootManager contains methods for configuring the main process by creating managers for synchronizing devices,
    tasks, variables, etc.
    across processes and threads, as well as remote/local server/client communication.
    Version 2.0.2
    """

    version = '2.0.2'

    def __init__(self, server=False, client=False, print_status=True):
        """
        constructs the manager for synchronizing flab (flab_manager) and queues (queue_manager)

        :param server: that indicates if the main process is a server
        :type server: boolean
        :param client: boolean that indicates if the main process is a client
        :type client: boolean
        :returns: None
        """

        self.processes = {}
        self.managers = {}
        self.remote_manager = None
        self.server = None

        try:
            self.setup_boot_directories()
            FlabManager.register('Flab', Flab.Flab, FlabProxy)
            if server:
                machine_queue = Queue()
                client_queue = Queue()
                remote_flab_queue = Queue()
                remote_flab_namespace = Namespace()
                remote_flab_namespace.devices = []
                RemoteManager.register('machine_queue', callable=lambda: machine_queue)
                RemoteManager.register('client_queue', callable=lambda: client_queue)
                RemoteManager.register('remote_flab_queue', callable=lambda: remote_flab_queue)
                RemoteManager.register('remote_flab_namespace', callable=lambda: remote_flab_namespace)

            elif client:
                RemoteManager.register('machine_queue')
                RemoteManager.register('client_queue')
                RemoteManager.register('remote_flab_queue')
                RemoteManager.register('remote_flab_namespace')

            self.print_status = print_status
            self.flab_manager = FlabManager()
            self.queue_manager = SyncManager()
            self.flab_manager.start()
            self.queue_manager.start()
        except Exception as e:
            if self.print_status:
                print('Error in creating boot manager')
                print(e)
        finally:
            pass

    def create_remote_manager(self, address, authkey, server=False):
        """Creates a remote queue manager and machine/client queue for communication

        :param address: IP address of the communicating server
        :type: address: boolean

        :param authkey: authentication key
        :type authkey: str

        :param server: indicates if the main process is a server
        :type server: boolean

        :returns: None
        """
        try:
            if server:
                self.remote_manager = RemoteManager(address=address, authkey=authkey)
                self.server = self.remote_manager.get_server()
                self.server.serve_forever()
            else:
                self.remote_manager = RemoteManager(address=address, authkey=authkey)
                self.remote_manager.connect()
        except Exception as e:
            print(e)
            print('Error in remote connection. Check connection and inputs')
        finally:
            pass

    def setup_boot_directories(self):
        """
        Adds project paths to the system path from the boot directory

        :returns: None
        """
        if 'Boot' in os.getcwd():
            os.chdir('..')
            cwd = os.getcwd()
            par1 = os.path.abspath(os.path.join(cwd, '..'))
            par2 = os.path.abspath(os.path.join(par1, '..'))
            sys.path.append(par2)
        else:
            if self.print_status:
                print('BootManager object must be created in a script in the boot directory')

    def create_queue(self):
        """
        creates a queue using the queue_manager

        :returns: Queue
        """
        return self.queue_manager.Queue()

    def create_flab_proxy(self, ui_queue=None, flab_queue=None, print_status=True):
        """
        creates a proxy Flab object to enable pickling i.e. synchronization of a Flab object across threads and
        processes

        :param ui_queue: The queue for sending commands to the UI process. None by default
        :type ui_queue: Queue

        :param flab_queue: The queue for sending commands to the Flab process. None by default
        :param flab_queue: The queue for sending commands to the Flab process. None by default
        :type flab_queue: Queue

        :param print_status: If outputs should be printed. True by default.
        :type print_status: boolean

        :returns: flab_proxy object
        """
        flab_proxy = self.flab_manager.Flab(ui_queue=ui_queue, flab_queue=flab_queue,
                                            print_status=print_status)  # flab namespace
        flab_proxy.tasks = self.flab_manager.dict()  # tasks dictionary
        flab_proxy.devices = self.flab_manager.dict()  # device dictionary
        flab_proxy.vars = self.flab_manager.dict()  # variable dictionary
        flab_proxy.uis = self.flab_manager.dict()  # GUI dictionary
        return flab_proxy

    def start_process(self, flab, task_name, *args, blocking=False):
        """
        Starts a task as a process

        :param flab: the flab object
        :type flab: Flab

        :param task_name: the task name
        :type task_name: str

        :param args: arguments to be passed to the given task

        :param blocking: if the task should block. False by default
        :type blocking: boolean

        :returns: None
        """

        process_class = flab.tasks[task_name]
        process = Process(target=process_class.run, args=args)
        process.start()
        if blocking:
            process.join()
        return process

    # args is a multidimensional tuple, where each element consists
    def start_processes(self, flab, task_names, *args, blocking=False):
        """
        Starts multiple tasks as processes simultaneously

        :param flab: the flab object
        :type flab: Flab

        :param task_names: the task name
        :type task_names: [str]

        :param args: a multidimensional tuple, where each element consists of the process arguments for each task
        :type args: tuple

        :param blocking: if the task should block. False by default
        :type blocking: boolean

        :returns: None
        """
        processes = {}
        index = 0
        for t in task_names:
            process_class = flab.tasks[t]
            process = Process(target=process_class.run, args=args[index])
            process.start()
            processes.update({t: process})
            index = index + 1
        if blocking:
            for p in processes:
                procs[p].join()
        return processes

    def shutdown(self):
        """
        Shuts down synchronization managers

        :returns: None
        """
        self.queue_manager.shutdown()
        self.flab_manager.shutdown()


class FlabProxy(NamespaceProxy):
    """
    A proxy class for sharing flab objects
    """
    _exposed_ = tuple(dir(Flab.Flab))

    def __getattr__(self, name):
        """
        gets an attribute from a Flab object
        :param name: name of the attribute to get
        :type name: str

        :returns: attribute
        """
        result = super().__getattr__(name)
        if isinstance(result, types.MethodType):
            def wrapper(*args, **kwargs):
                return self._callmethod(name, args)  # Note the return here

            return wrapper
        return result


class FlabManager(SyncManager):
    """a manager class for sharing flab objects across local processes. Inherits the multiprocessing class
    SyncManager"""
    pass


class RemoteManager(SyncManager):
    """A manager class for sharing flab objects across networks. Inherits the multiprocessing class SyncManager"""
    pass
