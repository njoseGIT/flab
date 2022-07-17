#Flab
#BootManager
#Version 2.0.1
#Published 17-Jul-2022
#Distributed under GNU GPL v3
#Author: Nicholas Jose

from flab import Flab
from multiprocessing import Process, Queue
from multiprocessing.managers import NamespaceProxy, SyncManager, Namespace
import types
import sys
import os

#A class for managing the booting of flab, specifically using the multiprocessing library
class BootManager():

    version = '2.0.1'
    processes = {}
    managers = {}

    #create the basic flab manager, queue manager and shared flab and queue
    #need to change server/client
    def __init__(self, server=False, client=False):
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

            self.flab_manager = FlabManager()
            self.queue_manager = SyncManager()
            self.flab_manager.start()
            self.queue_manager.start()
        except Exception as e:
            print('Error in creating boot manager')
            print(e)
        finally:
            pass

    #create a remote queue manager and machine/client queues
    def create_remote_manager(self,address, authkey, server=False):
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

    #set up boot directories
    def setup_boot_directories(self):

        if 'Boot' in os.getcwd():
            os.chdir('..')
            cwd = os.getcwd()
            par1 = os.path.abspath(os.path.join(cwd, '..'))
            par2 = os.path.abspath(os.path.join(par1, '..'))
            sys.path.append(par2)
        else:
            print('BootManager object must be created in a script in the boot directory')

    def create_queue(self):
        return self.queue_manager.Queue()

    def create_flab_proxy(self, ui_queue=None, flab_queue=None, print_status=True):
        flab_proxy = self.flab_manager.Flab(ui_queue=ui_queue, flab_queue=flab_queue,
                                            print_status=print_status)  # flab namespace
        flab_proxy.tasks = self.flab_manager.dict() # tasks dictionary
        flab_proxy.devices = self.flab_manager.dict()  # device dictionary
        flab_proxy.vars = self.flab_manager.dict()  # variable dictionary
        flab_proxy.uis = self.flab_manager.dict()  # GUI dictionary
        return flab_proxy

    def start_process(self, flab, task_name, *args, blocking=False):
        process_class = flab.tasks[task_name]
        process = Process(target=process_class.run, args=args)
        process.start()
        if blocking:
            process.join()
        return process

    # args is a multidimensional tuple, where each element consists of the process arguments
    def start_processes(self, flab, task_names, *args, blocking=False):
        procs = {}
        index = 0
        for t in task_names:
            process_class = flab.tasks[t]
            process = Process(target=process_class.run, args=args[index])
            process.start()
            procs.update({t: process})
            index = index + 1
        if blocking:
            for p in procs:
                procs[p].join()
        return procs

    #shuts down sync managers
    def shutdown(self):
        self.queue_manager.shutdown()
        self.flab_manager.shutdown()

#A proxy class for sharing flab
class FlabProxy(NamespaceProxy):
    _exposed_ = tuple(dir(Flab.Flab))

    def __getattr__(self, name):
        result = super().__getattr__(name)
        if isinstance(result, types.MethodType):
            def wrapper(*args, **kwargs):
                return self._callmethod(name, args)  # Note the return here
            return wrapper
        return result

#A synchmanager class for sharing flab across local processes
class FlabManager(SyncManager):
    pass

#A synchmanager class for sharing flab across networks
class RemoteManager(SyncManager):
    pass


