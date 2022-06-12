#Console2Actions.py
#A class containing UI actions for Console 2
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, QEventLoop, QTimer
import gc
from Console2.UIs.Widgets import MainWindowWithClose, ConsoleLineEdit
from PyQt5.QtWidgets import QFileDialog, QListWidget
import os
import inspect
import sys
import time

class Actions():

    def __init__(self, flab, ui_queue, flab_queue):
        self.flab = flab
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue

    def create_window(self):
        self.MainWindow = MainWindowWithClose.MainWindow(self.flab)
        self.setupUi(self.MainWindow)
        self.running_task_list = {}
        self.loaded_device_list = {}
        self.loaded_variable_list = {}
        self.console_task_names = ['Console2UIProcess','ConsoleFlabProcess']

    def configure_actions(self):
        self.textBrowser_flab_console.readOnly = True
        self.lineEdit = ConsoleLineEdit.LineEdit(self.MainWindow)
        self.lineEdit_layout.addWidget(self.lineEdit)
        self.lineEdit.returnPressed.connect(self.onReturn) # line edit restrictions for inputs
        self.pushButton_load_task.clicked.connect(self.click_load_task)
        self.pushButton_start_task.clicked.connect(self.click_start_task)
        self.pushButton_reload_task.clicked.connect(self.click_reload_task)
        self.pushButton_reload_start_task.clicked.connect(self.click_reload_start_task)
        self.pushButton_stop_task.clicked.connect(self.click_stop_task)
        self.pushButton_stop_all_tasks.clicked.connect(self.click_stop_all_tasks)

        self.pushButton_load_device.clicked.connect(self.click_load_device)
        self.listWidget_devices.itemClicked.connect(self.listWidget_devices_clicked)
        self.pushButton_display_device_attribute.clicked.connect(self.click_display_device_attribute)
        self.pushButton_set_device_attribute.clicked.connect(self.click_set_device_attribute)
        self.pushButton_device_test_method.clicked.connect(self.click_test_device_method)

        self.listWidget_variables.itemClicked.connect(self.listWidget_variable_clicked)
        self.pushButton_create_variable.clicked.connect(self.click_create_variable)
        self.pushButton_set_variable_value.clicked.connect(self.click_set_variable)
        self.pushButton_delete_variable.clicked.connect(self.click_delete_variable)

        self.actionOpen_Project.triggered.connect(self.click_open_project)
        self.actionExit.triggered.connect(self.close)

        self.start_live_update()

    def close(self):
        self.MainWindow.close()

    def click_open_project(self):
        try:
            os.chdir('..')
            s = QFileDialog()
            project_path = s.getExistingDirectory(self.MainWindow,caption='Open Project')
            if project_path != '':
                os.chdir(project_path)
                cwd = os.getcwd()
                par1 = os.path.abspath(os.path.join(cwd, '..'))
                par2 = os.path.abspath(os.path.join(par1, '..'))
                sys.path.append(par2)
                self.send_flab_command('set_working_directory("'+project_path+'")')
                self.send_flab_command('register_all_devices()')
                self.send_flab_command('start_device_manager()')
                self.MainWindow.setWindowTitle('FLab 2.0: '+os.path.basename(project_path))
                self.message('Loading tasks and devices')
                self.send_flab_command('load_all_tasks()')
                while not self.flab.load_all_tasks_completed:
                    self.console_sleep(1)
                self.send_flab_command('load_all_devices()')
                while not self.flab.load_all_devices_completed:
                    self.console_sleep(1)
                self.list_loaded_tasks()
                self.list_loaded_devices()
                self.msg.close()

        except Exception as e:
            self.flab.display('Error in opening project')
            self.flab.display(e)

    def console_sleep(self, seconds):
        loop = QEventLoop()
        QTimer.singleShot(seconds*1000, loop.quit)
        loop.exec_()

    def list_loaded_devices(self):
        try:
            self.listWidget_devices.clear()
            for d in self.flab.devices.keys():
                    self.listWidget_devices.addItem(self.flab.devices[d].get('device_name'))
        except Exception as e:
            self.flab.display('Error in listing devices')
            self.flab.display(e)
        finally:
            pass

    def list_loaded_tasks(self):
        try:
            self.listWidget_tasks.clear()
            for t in self.flab.tasks.keys():
                if t not in self.console_task_names:
                    try:
                        self.listWidget_tasks.addItem(self.flab.tasks[t].task_name)
                    except Exception as e:
                        self.flab.display('Error in listing task' + str(t))
                        self.flab.display(e)
        except Exception as e:
            self.flab.display('Error in listing tasks')
            self.flab.display(e)
        finally:
            pass

    def click_load_task(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + "\Tasks"
            else:
                cwd = os.path.abspath(os.getcwd()) + "/Tasks"
            s = QFileDialog()
            file_name = s.getOpenFileName(caption = 'Load Task', filter = 'Python files (*.py)',directory=cwd)
            if file_name[1]:
                file_name = os.path.basename(file_name[0])
                file_name = str.replace(file_name,'.py','')
                command = 'load_task("' + file_name + '")'
                self.send_flab_command(command)
                time.sleep(0.1)
                self.list_loaded_tasks()
        except Exception as e:
            self.flab.display('Error in file dialog')
            self.flab.display(e)

    def click_start_task(self):
        try:
            tasks = self.listWidget_tasks.selectedItems()
            if tasks != '':
                for i in tasks:
                    task_name = i.text()
                    full_args = inspect.getfullargspec(self.flab.tasks[task_name].run)
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []

                        for a in args_list:
                            if 'argument_descriptions' in dir(self.flab.tasks[task_name]):
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for '
                                                                      + self.flab.tasks[task_name].argument_descriptions[a])
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])
                            else:
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for ' + a )
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])

                        arg_combined_str = ','.join(arg_list)
                        command = 'start_task("' + i.text() + '",' + arg_combined_str + ')'
                    else:
                        command = 'start_task("' + i.text() + '")'
                    self.send_flab_command(command)

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in starting task')
        finally:
            pass

    def click_reload_task(self):
        try:
            tasks = self.listWidget_tasks.selectedItems()
            if tasks != '':
                for i in tasks:
                    command = 'reload_task("' + i.text() + '")'
                    self.textBrowser_flab_console.append('>' + command)
                    self.lineEdit.commandHistory.insert(1, command)
                    self.lineEdit.commandHistoryPosition = 0
                    self.flab_queue.put(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading and starting task')
        finally:
            pass

    def click_reload_start_task(self):
        try:
            tasks = self.listWidget_tasks.selectedItems()
            if tasks != '':
                for i in tasks:
                    command = 'reload_start_task("' + i.text() + '")'
                    self.textBrowser_flab_console.append('>' + command)
                    self.lineEdit.commandHistory.insert(1, command)
                    self.lineEdit.commandHistoryPosition = 0
                    self.flab_queue.put(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading and starting task')
        finally:
            pass

    def click_stop_task(self):
        task_to_stop = self.listWidget_tasks.selectedItems()
        if task_to_stop != []:
            command = 'stop_task("' + task_to_stop[0].text() + '")'
            self.send_flab_command(command)

    def click_stop_all_tasks(self):
        command = 'stop_all_tasks()'
        self.send_flab_command(command)
        self.flab.stop_all_tasks()

    def click_load_device(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + '\Devices'
            else:
                cwd = os.path.abspath(os.getcwd()) + '/Devices'
            s = QFileDialog()
            file_name = s.getOpenFileName(caption = 'Load Device', filter = 'Python files (*.py)',directory=cwd)
            if file_name[1]:
                file_name = os.path.basename(file_name[0])
                file_name = str.replace(file_name,'.py','')
                command = 'load_device("' + file_name + '")'
                self.textBrowser_flab_console.append('>' + command)
                self.lineEdit.commandHistory.insert(1, command)
                self.lineEdit.commandHistoryPosition = 0
                self.flab_queue.put(command)
        except Exception as e:
            self.flab.display('Error in file dialog')
            self.flab.display(e)

    def listWidget_devices_clicked(self):
        try:
            device = self.listWidget_devices.selectedItems()
            self.listWidget_device_attributes.clear()
            self.listWidget_device_methods.clear()
            if device != []:
                device_name = device[0].text()
                attribute_list = self.flab.devices[device_name].list_attributes()
                method_list = self.flab.devices[device_name].list_methods()
                for attribute_name in attribute_list:
                    self.listWidget_device_attributes.addItem(attribute_name)
                for method_name in method_list:
                    self.listWidget_device_methods.addItem(method_name)
        except Exception as e:
            self.flab.display(e)

    def click_display_device_attribute(self):
        device_attribute = self.listWidget_device_attributes.selectedItems()
        device_name = self.listWidget_devices.selectedItems()
        if device_attribute != [] and device_name != []:
            command = 'display(self.flab.devices["' + device_name[0].text() + '"].get("' + device_attribute[0].text() + '"))'
            self.send_flab_command(command)

    def click_set_device_attribute(self):
        try:
            device_attribute = self.listWidget_device_attributes.selectedItems()
            device_name = self.listWidget_devices.selectedItems()
            if device_attribute != [] and device_name != []:
                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set Device Attribute: ',
                                                                      'Enter value for  '
                                                                      + device_name[0].text() + ' : ' + device_attribute[0].text())
                if text[1] and text[0] != "":
                    command = 'devices["' + device_name[0].text() + '"].set("' + device_attribute[0].text() + '",' + text[0] + ')'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)

    def click_test_device_method(self):
        try:
            device_method = self.listWidget_device_methods.selectedItems()
            device_name = self.listWidget_devices.selectedItems()

            if device_method != [] and device_name != []:
                device_name = device_name[0].text()
                device_method = device_method[0].text()
                full_args = self.flab.devices[device_name].list_method_args(device_method)
                if len(full_args.args) > 1:
                    args_list = full_args.args[1:]
                    arg_list = []
                    opt_arg_list = []

                    for a in args_list:
                        if 'argument_descriptions' in dir(self.flab.devices[device_name]):
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for '
                                                                  + self.flab.devices[device_name].argument_descriptions[a])
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])
                        else:
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for ' + a )
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])

                    arg_combined_str = ','.join(arg_list)
                    command = 'display(self.flab.devices["' + device_name + '"].' + device_method + '(' + arg_combined_str + '))'
                else:
                    command = 'display(self.flab.devices["' + device_name + '"].' + device_method + '())'
                self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in starting task')
        finally:
            pass

    def click_get_device_attribute(self):
        device = self.listWidget_devices.selectedItems()
        if device != []:
            device_name = device[0].text()
            attribute_list = self.flab.devices[device_name].list_attributes()
            item = QtWidgets.QInputDialog.getItem(self.MainWindow, 'Attributes', 'Select an attribute', attribute_list,0,False)

    def listWidget_variable_clicked(self):
        try:
            self.listWidget_variable_values.clear()
            variable = self.listWidget_variables.selectedItems()
            if variable != []:
                variable_name = variable[0].text()
                variable_value = str(self.flab.vars[variable_name])
                self.listWidget_variable_values.addItem(variable_value)
        except Exception as e:
            self.flab.display(e)

    def click_set_variable(self):
        try:
            variable = self.listWidget_variables.selectedItems()
            if variable != []:
                variable_name = variable[0].text()
                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set Variable Value: ',
                                                      'Enter value for '
                                                      + variable_name + ': ')
                if text[1] and text[0] != "":
                    value = text[0]
                    command = 'vars.update(' + variable_name + '=' + value + ')'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)

    def click_create_variable(self):
        try:
            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'New variable name: ',
                                                  'Enter variable name:')
            if text[1] and text[0] != "":
                variable_name = text[0]
                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'New variable value: ',
                                                      'Enter variable value:')
                if text[1] and text[0] != "":
                    value = text[0]
                    command = 'add_var(' + value + ',"' + variable_name + '")'
                    self.send_flab_command(command)
                else:
                    command = 'add_var("","' + variable_name + '")'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)


    def click_delete_variable(self):
        try:
            variable = self.listWidget_variables.selectedItems()
            if variable != []:
                variable_name = variable[0].text()
                command = 'vars.pop("' + variable_name + '")'
                self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)

    def onReturn(self):
        try:
            command = self.lineEdit.text()
            self.send_flab_command(command)
        except Exception as e:
            self.flab.display('Error in flab command')
            self.flab.display(e)

    def send_flab_command(self, command):
        try:
            self.textBrowser_flab_console.append('>'+command)
            self.lineEdit.setText('')
            if not command == '':
                self.lineEdit.commandHistory.insert(1,command)
                self.lineEdit.commandHistoryPosition = 0
                if command == 'exit':
                    self.flab.close_flab()
                elif command[0:7] == 'python ':
                    try:
                        eval(command[7:])
                    except Exception as e:
                        self.textBrowser_flab_console.append('error in python command')
                        self.textBrowser_flab_console.append(str(e))
                elif 'clear' in command:
                    try:
                        self.textBrowser_flab_console.clear()
                    except Exception as e:
                        self.textBrowser_flab_console.append('error in clearing textBrowser')
                else:
                    try:
                        self.flab_queue.put(command)
                    except Exception as e:
                        self.textBrowser_flab_console.append('error in flab command')
                        self.textBrowser_flab_console.append(str(e))
        except Exception as e:
            self.flab.display('error in flab command')
            self.flab.display(e)
        finally:
            pass

    def start_queue_thread(self):
        self.qthread = QueueThread(self)
        self.qthread.print_str.connect(self.display)
        self.MainWindow.is_running = True
        self.qthread.start()

    def start_live_update(self):
        self.timer = QtCore.QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_liveview)
        self.timer.start()

        self.gc_timer = QtCore.QTimer()
        self.gc_timer.setInterval(1000*60)
        self.gc_timer.timeout.connect(self.clean_cache)
        self.gc_timer.start()

    def update_liveview(self):
        try:
            #task tracking
            running_tasks = self.flab.get_running_task_names()

            #remove dead tasks
            tasks_to_pop = []
            for task_name in self.running_task_list:
                if task_name not in running_tasks:
                    item_row = self.listWidget_running_tasks.row(self.running_task_list[task_name])
                    self.listWidget_running_tasks.takeItem(item_row)
                    tasks_to_pop.append(task_name)
            for p in tasks_to_pop:
                self.running_task_list.pop(p)

            #add new tasks
            for task_name in running_tasks:
                match = self.listWidget_running_tasks.findItems(task_name,QtCore.Qt.MatchFlag.MatchExactly)
                if match == []:
                    self.listWidget_running_tasks.addItem(task_name)
                    widget_item = self.listWidget_running_tasks.findItems(task_name,QtCore.Qt.MatchFlag.MatchExactly)
                    self.running_task_list.update({task_name:widget_item[0]})

            #device tracking
            devices_to_pop = []
            loaded_devices = self.flab.devices.keys()

            if self.flab.devices is not {}:
                for device_name in self.loaded_device_list:
                    if device_name not in loaded_devices:
                        item_row = self.listWidget_devices.row(self.loaded_device_list[device_name])
                        self.listWidget_devices.takeItem(item_row)
                        devices_to_pop.append(device_name)
                    for p in devices_to_pop:
                        self.running_task_list.pop(p)

                #add new devices
                for device_name in loaded_devices:
                    match = self.listWidget_devices.findItems(device_name, QtCore.Qt.MatchFlag.MatchExactly)
                    if match == []:
                        self.listWidget_devices.addItem(device_name)
                        widget_item = self.listWidget_devices.findItems(device_name, QtCore.Qt.MatchFlag.MatchExactly)
                        self.loaded_device_list.update({device_name: widget_item[0]})

            # variable tracking
            variables_to_pop = []
            loaded_variables = self.flab.vars.keys()

            if self.flab.vars is not {}:
                for variable_name in self.loaded_variable_list:
                    if variable_name not in loaded_variables:
                        item_row = self.listWidget_variables.row(self.loaded_variable_list[variable_name])
                        self.listWidget_variables.takeItem(item_row)
                        variables_to_pop.append(variable_name)
                    for p in variables_to_pop:
                        self.loaded_variable_list.pop(p)

                # add new variables
                for variable_name in loaded_variables:
                    match = self.listWidget_variables.findItems(variable_name, QtCore.Qt.MatchFlag.MatchExactly)
                    if match == []:
                        self.listWidget_variables.addItem(variable_name)
                        widget_item = self.listWidget_variables.findItems(variable_name, QtCore.Qt.MatchFlag.MatchExactly)
                        self.loaded_variable_list.update({variable_name: widget_item[0]})

                # update variable values
                self.listWidget_variable_values.clear()
                variable = self.listWidget_variables.selectedItems()
                if variable != []:
                    variable_name = variable[0].text()
                    variable_value = str(self.flab.vars[variable_name])
                    self.listWidget_variable_values.addItem(variable_value)

        except Exception as e:
            self.flab.display(e)

    def clean_cache(self):
        gc.collect(generation=2)

    def display(self, s):
        try:
            self.textBrowser_flab_console.append(str(s))
            self.textBrowser_flab_console.moveCursor(QtGui.QTextCursor.End)
            self.textBrowser_flab_console.ensureCursorVisible()
        except Exception as e:
            self.flab.display(e)

    def message(self, m):
        if m:
            self.msg = QtWidgets.QDialog()
            self.msg.setWindowTitle("FLab Message")
            self.layout = QtWidgets.QVBoxLayout(self.msg)
            mess = QtWidgets.QLabel(str(m))
            self.layout.addWidget(mess)
            self.msg.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowCloseButtonHint))
            self.msg.show()

    def flab_console_command(self):
        command = self.lineEdit_flab_console.text()
        self.textBrowser_flab_console.append('>'+command)
        self.lineEdit_flab_console.setText('')
        self.flab_queue.put(command)

class QueueThread(QThread):

    print_str = QtCore.pyqtSignal(str)

    def __init__(self, ui):
        self.ui = ui
        super().__init__()

    def run(self):

        while self.ui.MainWindow.is_running:
            try:
                s = self.ui.ui_queue.get(block=True, timeout = 30)
                if s != "close":
                    self.print_str.emit(str(s))
                else:
                    self.ui.MainWindow.is_running = False
                del s
            except Exception as e:
                if str(e) == '':
                    pass
                else:
                    self.print_str.emit(str(repr(e)))
            finally:
                pass