# Flab 3
# TaskManager
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""The TaskManager module includes classes and methods for creating and running synchronous/simultaneous routines"""

import glob
import threading
import sys
import os
import asyncio
import multiprocessing
from multiprocessing import Process
from flab.Templates import TaskTemplate
import time

class TaskManager:
    """
    The TaskManager class contains methods for loading, running and terminating tasks implementing python\'s threading
    library, asyncio, and multiprocessing
    """

    tasks = {} # dictionary of loaded tasks
    running_tasks = {} # dictionary of running tasks (i.e. instances of threads)
    scheduled_tasks = {} #a dictionary of scheduled tasks, including their scheduled start and stop times in seconds
    task_history = {} #a dictionary of the previous tasks run in a given session, along with their start and end times.
    load_all_tasks_completed = False # true if load_all_tasks has been completed
    loop = asyncio.new_event_loop() # create asyncio event loop

    def __init__(self):
        pass

    def load_task(self, task_name) -> None:
        """
        Loads a single task object into flab. The task name is given by the filename, without the '.py' at the end

        :param task_name: the task's name
        :type: str

        :returns: None
        """
        try:
            self.load_object(task_name,'.Tasks.', 'task', 'tasks', 'Task')

        except Exception as e:
            self.display('Error in loading ' + task_name)
            self.display(str(e))

        finally:
            pass

    def load_tasks(self, task_names) -> None:
        """
        Loads a list of tasks into flab. task_names is list of the task names (string)

        :param task_names: list of the task names
        :type task_names: [str]

        :returns: None
        """
        try:
            for task_name in task_names:
                self.load_task(task_name)

        except Exception as e:
            self.display('Error in loading tasks')
            self.display(str(e))

        finally:
            pass

    def load_all_tasks(self) -> None:
        """
        Loads every task present in the current project's Tasks folder

        :returns: None
        """
        try:
            cwd = os.getcwd()
            tasks = glob.glob(cwd + '/Tasks/*.py')
            task_names = []
            for t in tasks:
                task_names.append(t[len(cwd + '/Tasks/'):].replace('.py', ''))
            self.load_tasks(sorted(task_names))

        except Exception as e:
            self.display('Error in loading tasks')
            self.display(str(e))

        finally:
            self.display('All tasks loaded successfully')
            self.load_all_tasks_completed = True

    def reload_task(self, task_name) -> None:
        """
        Reloads a single task into a flab object

        :param task_name: name of the task
        :type task_name: str

        :returns: None
        """
        try:
            self.reload_object(task_name,'tasks','task','Task')

        except Exception as e:
            self.display('Error reloading ' + task_name)
            self.display(str(e))

        finally:
            pass

    def reload_tasks(self, task_names) -> None:
        """
        Reloads multiple tasks

        :param task_names: names of tasks in a list
        :type task_names: [str]

        :returns: None
        """
        reload_error = ''
        try:
            for task_name in task_names:
                error = self.reload_task(task_name)
                reload_error = reload_error + str(error)

            if reload_error == '':
                self.display('All Tasks reloaded successfully')

        except Exception as e:
            self.display("Error in reloading tasks" + str(task_names))
            self.display(str(e))

        finally:
            return reload_error

    def start_task(self, task_name, *args, **kwargs) -> None:
        """
        Start a task using the "run" method, using the task attribute task_type to determine how to start it.

        :param task_name: name of the task
        :type task_name: str

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            task_type = task.get('task_type')
            if task_type == 'thread':
                self.start_thread(task_name, *args, **kwargs)
            elif task_type == 'asyncio':
                self.start_asyncio_task(task_name, *args, **kwargs)
            elif task_type == 'process':
                self.start_process(task_name, *args, **kwargs)
            else:
                self.display(task_name + ' task type ' + task.get('task_type') + ' not recognized')

        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def load_start_task(self, task_name, *args, **kwargs) -> None:
        """
        Load and start a task in one method

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            self.load_task(task_name)
            self.start_task(task_name, *args, **kwargs)

        except Exception as e:
            self.display('Error in loading and starting task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def reload_start_task(self, task_name, *args, **kwargs) -> None:
        """
        reload and start a task in one method

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            self.reload_task(task_name)
            self.start_task(task_name, *args, **kwargs)

        except Exception as e:
            self.display('Error in reloading and starting task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def stop_task(self, task_name, *args, **kwargs) -> None:
        """
        Stop a task using the task's "stop" method.

        :param task_name: name of the task
        :type task_name: str

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            task_type = task.get('task_type')
            if task_type == 'thread':
                self.stop_thread(task_name, *args, **kwargs)
            elif task_type == 'asyncio':
                self.stop_asyncio_task(task_name, *args, **kwargs)
            elif task_type == 'process':
                self.stop_process(task_name, *args, **kwargs)
            else:
                self.display(task_name + ' task type ' + task.get('task_type') + ' not recognized')

        except Exception as e:
            self.display('Error in stopping task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def stop_all_tasks(self):
        """
        This method stops all running tasks
        Asyncio event loops should be stopped upon closing

        :returns: None
        """
        try:
            current_tasks = self.running_tasks
            temp_tasks = []
            for running_task_name in current_tasks:
                if running_task_name.__contains__('RUN_') and not running_task_name.__contains__('AsyncioEventLoop'):
                    temp_tasks.append(running_task_name)
            for running_task_name in temp_tasks:
                task_name = running_task_name[running_task_name.index('_')+1:running_task_name.rindex('_')]
                self.stop_task(task_name)

        except Exception as e:
            self.display('Error in stopping all tasks')
            self.display(str(e))

        finally:
            pass

    def kill_task(self, running_task_name):
        """
        kill a task, using the task attribute task_type to determine how to kill it.

        :param running_task_name: name of the task
        :type running_task_name: str

        :returns: None
        """
        try:
            #parse running task name into task to obtain task type
            task_name = running_task_name[running_task_name.index('_')+1:running_task_name.rindex('_')]
            task = self.tasks[task_name]
            task_type = task.get('task_type')
            if task_name == 'AsyncioEventLoop':
                self.stop_asyncio_loop()
            elif task_type == 'thread':
                self.kill_thread(running_task_name)
            elif task_type == 'asyncio':
                self.kill_asyncio_thread(running_task_name)
            elif task_type == 'process':
                self.kill_process(running_task_name)
            else:
                self.display(running_task_name + ' task type ' + task.get('task_type') + ' not recognized')
        except Exception as e:
            self.display('Error in killing task ' + running_task_name)
            self.display(str(e))

        finally:
            pass

    def kill_all_tasks(self):
        """
        This method kills all running tasks. This does not kill the asyncio event loop.

        :returns: None
        """
        try:
            for running_task_name in self.get_running_task_names():
                if not running_task_name.__contains__('AsyncioEventLoop'):
                    self.kill_task(running_task_name)

        except Exception as e:
            self.display('Error in killing all tasks')
            self.display(str(e))
        finally:
            pass

    def start_thread(self, task_name, *args, **kwargs) -> None:
        """
        Start a thread with the run method, with input arguments args and kwargs

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            thr = ThreadTrace('run', task_name, self, target=task.get('run'), args=args, kwargs=kwargs, daemon=True)
            thr.start()
            thread_name = 'RUN_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({thread_name : thr})
            self.task_history.update({thread_name : [time.time(),None,str(len(self.task_history))]})

        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def stop_thread(self, task_name, *args, **kwargs) -> None:
        """
        Runs the stop method of a task, with input arguments args and kwargs.
        Since Flab 3.0, this method does not kill running tasks

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            task = self.tasks[task_name]
            thr = ThreadTrace('stop', task_name, self, target=task.get('stop'), args=args, kwargs=kwargs, daemon=True)
            thr.start()
            thread_name = 'STOP_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({thread_name: thr})
            self.task_history.update({thread_name : [time.time(),None,str(len(self.task_history))]})

        except Exception as e:
            self.display('Error in stopping task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def kill_thread(self, thread_name) -> None:
        """
        Directly kills a thread

        :param thread_name: name of the thread
        :type thread_name: str

        :returns: None
        """
        try:
            thr = self.running_tasks[thread_name]
            thr.kill()
            thr.join()

        except Exception as e:
            self.display('Error in killing task ' + str(thread_name))
            self.display(str(e))

        finally:
            pass

    def display_running_tasks(self) -> None:
        """
        Displays task instances

        :returns: None
        """
        self.display(self.running_tasks.keys())

    def display_alive_tasks(self) -> None:
        """
        displays all tasks that are still alive

        :returns: None
        """
        for t in self.running_tasks:
            try:
                if self.running_tasks[t].is_alive() is True:
                    self.display(t)
            except Exception as e:
                self.display('Error in displaying alive tasks')
                self.display(str(e))
            finally:
                pass

    def display_alive_threads(self) -> None:
        """
        This is deprecated in favour of "display_alive_tasks"
        displays all threads that are still alive

        :returns: None
        """
        for task in self.running_tasks:
            try:
                if self.running_tasks[task].is_alive() is True:
                    self.display(task)
            except Exception as e:
                self.display('Error in displaying alive tasks')
                self.display(str(e))
            finally:
                pass

    def get_running_task_names(self) -> [str]:
        """
        Returns names of running tasks

        :returns: list of str
        """
        running_task_names = []
        try:
            for i in self.running_tasks:
                if self.running_tasks[i].is_alive() is True:
                    running_task_names.append(i)

        except Exception as e:
            self.display('Error in getting running task names')
            self.display(str(e))

        finally:
            return sorted(running_task_names)

    def start_process(self, task_name, *args, blocking=False, **kwargs) -> None:
        """
        Start a process with the run method,  with input arguments args and kwargs

        :param task_name: name of the task
        :type task_name: str

        :param args: args for the task

        :param blocking: if the task is blocking (False by default)
        :type blocking: boolean

        :returns: None
        """
        try:
            process_class = self.tasks[task_name]
            process_task = ProcessTask(process_class)
            process = Process(target=process_task.run, args=args, kwargs=kwargs, daemon=True)
            process.start()
            process_name = 'RUN_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({process_name: process})
            self.task_history.update({process_name : [time.time(),None,str(len(self.task_history))]})
            if blocking:
                process.join()

        except Exception as e:
            self.display('Error in starting process ' + task_name)
            self.display(str(e))

        finally:
            pass

    def start_processes(self, task_names, *args, blocking=False) -> None:
        """
        Start multiple processes at once.

        :param task_names: name of the task
        :type task_names: [str]

        :param args: args is a multidimensional tuple, where each element consists of the process arguments

        :param blocking: if the task is blocking (False by default)
        :type blocking: boolean

        :returns: None
        """
        try:
            processes = {}
            index = 0
            for t in task_names:
                process_class = self.tasks[t]
                process = Process(target=process_class.get('run'), args=args[index])
                process.start()
                processes.update({'RUN_' + t: process})
                self.running_tasks.update({'RUN_' + t: process})
                index = index + 1
            for p in processes:
                processes[p].join()
            if blocking:
                for p in processes:
                    processes[p].join()

        except Exception as e:
            self.display('Error in starting processes ' + task_names)
            self.display(str(e))

        finally:
            pass

    def stop_process(self, task_name, *args, blocking=True) -> None:
        """
        stop a process by calling the stop method of the process as another process.
        Since Flab 3.0 this method does not kill a process

        :param task_name: the task name
        :type task_name: str

        :param args: args is a multidimensional tuple, where each element consists of the process arguments

        :param blocking: if the task is blocking (True by default)
        :type blocking: boolean

        :returns: None
        """
        try:
            process_class = self.tasks[task_name]
            process = Process(target=process_class.get('stop'), args=args, daemon=True)
            process.start()
            process_name = 'STOP_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({process_name: process})
            self.task_history.update({process_name : [time.time(),None,str(len(self.task_history))]})

            if blocking:
                process.join()
        except Exception as e:
            self.display('Error in stopping process ' + task_name)
            self.display(str(e))
        finally:
            pass

    def kill_process(self, running_task_name):
        """
        Kills a process by calling the terminate method.

        :param running_task_name: the running task name
        :type running_task_name: str

        :returns: None
        """
        try:
            if running_task_name in self.running_tasks:
                self.running_tasks[running_task_name].terminate()
        except Exception as e:
            self.display('Error in killing process ' + running_task_name)
            self.display(str(e))
        finally:
            pass

    def start_asyncio_loop(self) -> None:
        """
        Start an asyncio event loop, which will be used to run all asyncio tasks in a single thread

        :returns: None
        """
        try:
            loop_task = LoopTask()
            self.tasks.update({'AsyncioEventLoop':loop_task})
            self.start_task('AsyncioEventLoop', self.loop)

        except Exception as e:
            self.display('Error in starting asyncio loop')
            self.display(str(e))
        finally:
            pass

    def stop_asyncio_loop(self) -> None:
        """
        This function stops the asyncio loop running in the loop thread

        :returns: None
        """
        try:
            async def stop_loop():
                running_loop = asyncio.get_running_loop()
                running_loop.stop()
            asyncio.run_coroutine_threadsafe(stop_loop(), self.loop)
        except Exception as e:
            self.display('Error in stopping asyncio loop')
            self.display(str(e))
        finally:
            pass

    def is_asyncio_loop_running(self) -> bool:
        """
        Checks if the asyncio loop is running

        :returns: true if the asyncio loop is running, false if not
        :rtype: bool
        """
        is_running = False
        try:
            is_running = self.loop.is_running()
        except Exception as e:
            self.display('Error in checking asyncio loop')
            self.display(str(e))
        finally:
            return is_running


    def start_asyncio_task(self, task_name, *args, **kwargs) -> None:
        """
        Start an asyncio task by adding it to the asyncio loop as a coroutine

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments
        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            coroutine_trace = CoroutineTrace('run',task_name, self, self.loop)
            coroutine_trace.start(*args, **kwargs)
            coroutine_name = 'RUN_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({coroutine_name : coroutine_trace})
            self.task_history.update({coroutine_name : [time.time(),None,str(len(self.task_history))]})
        except Exception as e:
             self.display('Error in starting task ' + task_name)
             self.display(str(e))
        finally:
             pass

    def stop_asyncio_task(self, task_name, *args, **kwargs) -> None:
        """
        Stop an asyncio task by running the stop method.
        Since Flab 3.0 this does not kill a running asyncio thread.

        :param task_name: name of the task
        :type task_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            coroutine_trace = CoroutineTrace('stop',task_name, self, self.loop)
            coroutine_trace.start(*args, **kwargs)
            coroutine_name = 'STOP_' + task_name + '_' + str(len(self.task_history))
            self.running_tasks.update({coroutine_name : coroutine_trace})
            self.task_history.update({coroutine_name : [time.time(),None,str(len(self.task_history))]})

        except Exception as e:
            self.display('Error in starting task ' + task_name)
            self.display(str(e))

        finally:
            pass

    def kill_asyncio_thread(self, running_task_name):
        """
        Kills an asyncio task.

        :param running_task_name: name of the task
        :type running_task_name: str

        :returns: None
        """
        try:
            self.running_tasks[running_task_name].kill()

        except Exception as e:
            self.display('Error in killing task ' + running_task_name)
            self.display(str(e))

        finally:
            pass

    def send_command(self, queue, function_name, *args, **kwargs) -> None:
        """
        A function for passing commands between different processes in a queue

        :param queue: a queue for message passing
        :type queue: Queue

        :param function_name: name of the function
        :type function_name: str

        :param args: task arguments

        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            to_pass = function_name, args, kwargs
            queue.put(to_pass)

        except Exception as e:
            self.display('Error in send_command')
            self.display(str(e))

        finally:
            pass

    def execute_command(self, parsed_command) -> None:
        """
        A function for executing a structured function command

        :param parsed_command: a parsed command
        :type parsed_command: (function, (args), {kwargs})

        :returns: None
        """
        try:
            function = self.__getattribute__(parsed_command[0])
            function(*parsed_command[1], **parsed_command[2])
        except Exception as e:
            self.display('Error in execute_command')
            self.display(str(e))
        finally:
            pass

    def update_task_end_time(self,running_task_name,task_end_time) -> None:
        """
        A function for updating the end time of a given task in the task history

        :param running_task_name: Name of the running task
        :type running_task_name: str

        :param task_end_time: The task end time timestamp (returned from time.time())
        :type task_end_time: str

        :returns: None
        """
        try:
            self.task_history[running_task_name][1] = task_end_time
        except Exception as e:
            self.display('Error in updating task end time of ' + running_task_name)
            self.display(str(e))
        finally:
            pass

    def get_task_history(self):
        """
        Returns the task history

        :returns: task history
        :rtype: dict
        """
        return self.task_history

    def load_schedule_task(self):
        """
        Loads a ScheduleTask into the tasks

        :returns: None
        """
        task = ScheduleTask(self)
        self.tasks.update({'ScheduleTask':task})

    def schedule_task(self, start_time, task_name, *args, **kwargs):
        """
        Schedule a task by adding a ScheduleTask to the asyncio loop as a coroutine

        :param task_name: name of the task
        :type task_name: str

        :param start_time: starting timestamp
        :type task_name: flaot

        :param args: task arguments
        :param kwargs: task keyword arguments

        :returns: None
        """
        try:
            coroutine_trace = CoroutineTrace('run','ScheduleTask', self, self.loop)
            coroutine_trace.start(start_time, task_name, *args, **kwargs)
            coroutine_name = 'SCHEDULE_' + str(task_name) + '_' + str(len(self.task_history))
            self.running_tasks.update({coroutine_name : coroutine_trace})
            self.task_history.update({coroutine_name : [time.time(),None,str(len(self.task_history))]})
        except Exception as e:
             self.display('Error in scheduling task ' + task_name)
             self.display(str(e))
        finally:
             pass

class ProcessTask():
    """
    A class for Processes, which enables embedded activation of virtual environments
    """

    def __init__(self, process_class):
        """
        :param process_class: class of the process to be run
        """
        self.process_class = process_class

    def activate_environment(self, exec_path):
        """
        Activates the specified environment given by the path of the executable

        :param exec_path: path to the python executable in the new environment
        """
        try:
            import os, sys
            # set environment variable PATH
            old_os_path = os.environ.get('PATH', '')
            os.environ['PATH'] = os.path.dirname(os.path.abspath(exec_path)) + os.pathsep + old_os_path
            base = os.path.dirname(os.path.dirname(os.path.abspath(exec_path)))
            # site-packages path
            if sys.platform == 'win32':
                site_packages = os.path.join(base, 'Lib', 'site-packages')
            else:
                site_packages = os.path.join(base, 'lib', 'python%s' % sys.version[:3], 'site-packages')
            # modify sys.path
            prev_sys_path = list(sys.path)
            # remove previous environment
            for item in prev_sys_path:
                sys.path.remove(item)
            import site
            site.addsitedir(site_packages)
            sys.real_prefix = sys.prefix
            sys.prefix = base
            # Move the added items to the front of the path:
            new_sys_path = []
            for item in list(sys.path):
                if item not in prev_sys_path:
                    new_sys_path.append(item)
                    sys.path.remove(item)
            sys.path[:0] = new_sys_path
        except Exception as e:
            self.display('Error in activating environment')
            self.display(str(e))
        finally:
            pass

    def run(self, *args, **kwargs):
        """
        Runs the process's "run" method, preceded by a change in environment if necessary.

        :param args: process arguments
        :param kwargs: process arguments
        :returns: None
        """
        try:
            try:
                environment_path = self.process_class.get('environment_path')
                if sys.platform.startswith('win'):
                    exec_path = os.path.join(environment_path, 'Scripts', 'python.exe')
                else:
                    bin_dir = 'Scripts' if sys.platform.startswith('win') else 'bin'
                    exec_path = os.path.join(environment_path, bin_dir, 'python')

                multiprocessing.set_executable(exec_path)
            except Exception as e:
                exec_path = ''
            finally:
                pass

            run = self.process_class.get('run')
            if exec_path != '':
                self.activate_environment(exec_path)
            run(*args, **kwargs)
        except Exception as e:
            self.flab.display('Error in ProcessTask')
            self.flab.display(str(e))
        finally:
            pass

class ThreadTrace(threading.Thread):
    """
    A class for killable threads using traces. Inherits Thread from the threading library.
    """

    def __init__(self, task_method, task_name, flab, *args, **kwargs):
        """
        creates a ThreadTrace object, which can be killed via the kill command

        :param task_method: name of the method
        :type task_method: str

        :param task_name: name of the task
        :type task_name: str

        :param flab: a flab object
        :type flab: Flab

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """
        self.task_method = task_method
        self.task_name = task_name
        self.flab = flab
        threading.Thread.__init__(self, *args, **kwargs)
        self.killed = False

    def start(self):
        """
        starts the thread

        :returns: None
        """
        try:
            self.__run_backup = self.run
            self.run = self.__run
            threading.Thread.start(self)
        except Exception as e:
            self.flab.display(str(e))

    def __run(self):
        """
        creates a tracer for the thread

        :returns: None
        """
        try:
            sys.settrace(self.globaltrace)
            self.__run_backup()
            self.run = self.__run_backup
        except Exception as e:
            self.flab.display(str(e))

    def globaltrace(self, frame, event, arg):
        """
        Creates a global trace for the thread

        :param frame: frame

        :param event: event

        :param arg: argument

        :returns: localtrace
        """
        if event == 'call':
            return self.localtrace
        else:
            return None

    def localtrace(self, frame, event, arg):
        """
        Creates a local trace for the thread. If the thread is killed the thread will exit.

        :param frame: frame

        :param event: event

        :param arg: argument

        :returns: localtrace
        """
        if self.killed:
            if event == 'line':
                raise SystemExit()
        return self.localtrace

    def kill(self):
        """
        raises a flag to kill a thread

        :returns: None
        """
        self.killed = True

class LoopTask(TaskTemplate.Task):
    '''
    A Task class for an asyncio event loop thread
    '''

    task_type = 'thread'
    task_name = 'AsyncioEventLoop'
    task_stopped = False

    def __init__(self):
        self.loop = None

    def run(self, loop) -> None:
        """
        starts running the eventloop

        :param loop: the event loop
        :type loop: asyncio eventloop

        :returns: None
        """
        self.loop = loop
        asyncio.set_event_loop(self.loop)
        try:
            loop.run_forever()
        finally:
            loop.run_until_complete(loop.shutdown_asyncgens())
            loop.close()

class ScheduleTask(TaskTemplate.Task):
    '''
    A Task class for scheduling tasks
    '''

    task_type = 'asyncio'
    task_name = 'ScheduleTask'
    task_stopped = False

    def __init__(self, flab):
        self.flab = flab

    async def run(self, start_time, task_name, *args, **kwargs):
        await asyncio.sleep(start_time-time.time())
        self.flab.start_task(task_name, *args, **kwargs)

class CoroutineTrace():
    '''
    A class for "killable" coroutines
    '''

    def __init__(self, task_method, task_name, flab, loop):
        """
        creates a CoroutineTrace object, which can be killed via the kill command

        :param task_method: name of the method
        :type task_method: str

        :param task_name: name of the task
        :type task_name: str

        :param flab: a flab object
        :type flab: Flab

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        """

        self.task_method = task_method
        self.task_name = task_name
        self.flab = flab
        self.killed = False
        self.future = None
        self.loop = loop

    def start(self, *args, **kwargs) -> None:
        '''
        starts the coroutine

        :param args: arguments for the task

        :param kwargs: keyword arguments for the task

        :returns: None
        '''
        try:
            coroutine_run = self.flab.tasks[self.task_name].get(self.task_method)
            self.future = asyncio.run_coroutine_threadsafe(coroutine_run(*args,**kwargs),self.loop)
        except Exception as e:
            self.flab.display('Error in starting ' + str.upper(self.task_method) + '_' + self.task_name)
            self.flab.display(str(e))
        finally:
            pass

    def kill(self) -> None:
        '''
        kills the coroutine using the future object

        :returns: None
        '''
        try:
            if self.future != None:
                self.future.cancel()
                self.killed = True
        except Exception as e:
            self.flab.display('Error in killing ' + str.upper(self.task_method) + '_' + self.task_name)
            self.flab.display(str(e))
        finally:
            pass

    def is_alive(self) -> bool:
        '''
        checks if the coroutine is alive

        :returns: bool
        '''
        alive = None
        try:
            alive = not self.future.done()
        except Exception as e:
            alive = False
            #self.flab.display('Error in checking if coroutine ' + self.task_name + ' is alive')
            #self.flab.display(str(e))
        finally:
            return alive