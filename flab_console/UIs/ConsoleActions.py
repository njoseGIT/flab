from PyQt5 import QtGui, QtCore, QtWidgets
from PyQt5.QtCore import QThread, QEventLoop, QTimer, Qt
from PyQt5.QtWidgets import QFileDialog, QListWidget, QMessageBox
from flab_console.UIs.Widgets import MainWindowWithClose, ConsoleLineEdit, OptionDialog, DateTimeDialog
import gc
import pyqtgraph as pg
import os
import inspect
import sys
import time
import datetime

class Actions():

    project_path = 'NA'
    def __init__(self, flab, ui_queue, flab_queue, projects_path = ''):
        self.flab = flab
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue
        self.project_path = 'NA'
        self.projects_path = projects_path

    def create_window(self):
        self.MainWindow = MainWindowWithClose.MainWindow(self.flab)
        self.setupUi(self.MainWindow)
        self.running_task_list = {}
        self.loaded_device_list = {}
        self.loaded_variable_list = {}
        self.loaded_data_list = {}
        self.loaded_uis_list = {}
        self.running_ui_list = {}
        self.loaded_model_list = {}

        self.console_task_names = ['ConsoleUIProcess','ConsoleFlabProcess']
        self.plot_setup()
        self.task_history_list = {}
        self.task_bar_items = {}
        self.task_bar_color_scheme = [
            (90, 181,224),
            (72, 145, 180),
            (49, 97, 120)
        ]
        self.plot_x_variable = None # name of the x variable
        self.plot_y_variables = [] # list of names of the y variables
        self.plot_variables_on = False # if the variable plot widget is on
        self.plot_items = {}

    def configure_actions(self):
        # file menu actions
        self.actionOpen_Project.triggered.connect(self.click_open_project)
        self.actionRestart.triggered.connect(self.restart)
        self.actionRestart_Project.triggered.connect(self.restart_project)
        self.actionExit.triggered.connect(self.exit_clicked)

        # view menu actions
        # self.actionVariable_Manager.triggered.connect(self.view_variable_manager)
        self.actionManagers.triggered.connect(self.view_managers)
        self.actionConsole.triggered.connect(self.view_console)

        # help menu actions
        self.actionAbout.triggered.connect(self.about_message)
        self.actionDocumentation.triggered.connect(self.documentation_message)

        # command line actions
        self.textBrowser_flab_console.readOnly = True
        self.lineEdit = ConsoleLineEdit.LineEdit(self.MainWindow)
        self.lineEdit_layout.addWidget(self.lineEdit)
        self.lineEdit.returnPressed.connect(self.onReturn) # line edit restrictions for inputs

        # task manager actions
        self.pushButton_load_task.clicked.connect(self.click_load_task)
        self.pushButton_start_task.clicked.connect(self.click_start_task)
        self.pushButton_reload_task.clicked.connect(self.click_reload_task)
        self.pushButton_stop_task.clicked.connect(self.click_stop_task)
        self.pushButton_stop_all_tasks.clicked.connect(self.click_stop_all_tasks)
        self.pushButton_schedule_task.clicked.connect(self.click_schedule_task)
        self.pushButton_kill_task.clicked.connect(self.click_kill_task)
        self.pushButton_kill_all_tasks.clicked.connect(self.click_kill_all_tasks)
        self.listWidget_tasks.setSortingEnabled(True)

        # device manager actions
        self.pushButton_load_device.clicked.connect(self.click_load_device)
        self.pushButton_reload_device.clicked.connect(self.click_reload_device)
        self.listWidget_devices.itemClicked.connect(self.listWidget_devices_clicked)
        self.pushButton_display_device_attribute.clicked.connect(self.click_display_device_attribute)
        self.pushButton_set_device_attribute.clicked.connect(self.click_set_device_attribute)
        self.pushButton_device_test_method.clicked.connect(self.click_test_device_method)
        self.listWidget_devices.setSortingEnabled(True)
        self.pushButton_plot_clear_all_y_variables.clicked.connect(self.click_plot_clear_all_y_variables)
        self.pushButton_plot_remove_y_variable.clicked.connect(self.click_plot_remove_y_variable)

        # variable manager actions
        self.listWidget_variables.itemClicked.connect(self.listWidget_variable_clicked)
        self.pushButton_create_variable.clicked.connect(self.click_create_variable)
        self.pushButton_set_variable_value.clicked.connect(self.click_set_variable)
        self.pushButton_delete_variable.clicked.connect(self.click_delete_variable)
        self.listWidget_variables.setSortingEnabled(True)
        self.pushButton_plot_set_x_variable.clicked.connect(self.click_plot_set_x_variable)
        self.pushButton_plot_add_y_variable.clicked.connect(self.click_plot_add_y_variable)
        self.pushButton_live_plot.clicked.connect(self.click_live_plot)

        # data manager actions
        self.pushButton_load_data.clicked.connect(self.click_load_data)
        self.pushButton_reload_data.clicked.connect(self.click_reload_data)
        self.pushButton_set_data_attribute.clicked.connect(self.click_set_data_attribute)
        self.pushButton_test_method.clicked.connect(self.click_test_data_method)
        # self.pushButton_set_data_attribute.clicked.connect(self.click_set_data_attribute)
        self.pushButton_display_data_attribute.clicked.connect(self.click_display_data_attribute)
        self.listWidget_data.itemClicked.connect(self.listWidget_data_clicked)
        self.listWidget_data.setSortingEnabled(True)
        self.pushButton_update_file.clicked.connect(self.update_file)
        self.pushButton_update_variable.clicked.connect(self.update_variable)

        # ui manager actions
        self.pushButton_load_ui.clicked.connect(self.click_load_ui)
        self.pushButton_reload_ui.clicked.connect(self.click_reload_ui)
        self.pushButton_start_ui.clicked.connect(self.click_start_ui)
        self.pushButton_stop_ui.clicked.connect(self.click_stop_ui)

        # model manager actions
        self.pushButton_load_model.clicked.connect(self.click_load_model)
        self.pushButton_reload_model.clicked.connect(self.click_reload_model)
        self.pushButton_evaluate_model.clicked.connect(self.click_evaluate_model)
        self.pushButton_train_model.clicked.connect(self.click_train_model)
        self.pushButton_model_predict.clicked.connect(self.click_model_predict)
        self.pushButton_set_model_attribute.clicked.connect(self.click_set_model_attribute)
        self.pushButton_display_model_attribute.clicked.connect(self.click_display_model_attribute)
        self.listWidget_models.itemClicked.connect(self.listWidget_models_clicked)
        self.pushButton_model_test_method.clicked.connect(self.click_test_model_method)
        self.listWidget_models.setSortingEnabled(True)

        self.start_live_update()

    def view_variable_manager(self):
        if self.actionVariable_Manager.isChecked():
            self.dockWidget_variables.show()
        else:
            self.dockWidget_variables.hide()

    def view_managers(self):
        if self.actionManagers.isChecked():
            self.dockWidget_managers.show()
        else:
            self.dockWidget_managers.hide()

    def view_console(self):
        if self.actionConsole.isChecked():
            self.dockWidget_console.show()
        else:
            self.dockWidget_console.hide()

    def about_message(self):
        self.msg = QtWidgets.QDialog()
        self.msg.setWindowTitle("About Flab Console")
        self.layout = QtWidgets.QVBoxLayout(self.msg)
        about_message = "Flab Console \n"\
                        "Version 3.0.0 \n" \
                        "Nicholas A. Jose \n" \
                        "University of Cambridge, UK \n" \
                        "Flab Console is a graphical user interface dashboard for Flab applications"
        mess = QtWidgets.QLabel(about_message)
        self.layout.addWidget(mess)
        self.msg.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowCloseButtonHint))
        self.msg.show()

    def documentation_message(self):
        self.msg = QtWidgets.QDialog()
        self.msg.setWindowTitle("Documentation")
        self.layout = QtWidgets.QVBoxLayout(self.msg)
        mess = QtWidgets.QLabel("<a href='https://flab.readthedocs.io/en/latest'>View the latest on documentation on flab here</a>")
        mess.setOpenExternalLinks(True)
        self.layout.addWidget(mess)
        self.msg.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowCloseButtonHint))
        self.msg.show()

    def exit_clicked(self):
        self.MainWindow.close()

    def close(self):
        self.send_flab_command('close_flab()')
        self.MainWindow.close()

    def open_project(self, project_path, new = True):
        self.actionOpen_Project.setEnabled(False)
        self.project_path = project_path
        os.chdir(project_path)
        cwd = os.getcwd()
        par1 = os.path.abspath(os.path.join(cwd, '..'))
        par2 = os.path.abspath(os.path.join(par1, '..'))
        sys.path.append(par2)
        self.send_flab_command('set_working_directory("' + project_path + '")')
        if new:
            self.send_flab_command('register_proxy()')
            self.send_flab_command('start_object_manager()')
        self.MainWindow.setWindowTitle('Flab 3.0:' + os.path.basename(project_path))
        self.flab.load_all_tasks_completed = False
        self.flab.load_all_devices_completed = False
        self.send_flab_command('load_all_devices()')
        while not self.flab.load_all_devices_completed:
            self.console_sleep(1)
        self.flab.load_all_data_completed = False
        self.send_flab_command('load_all_data()')
        while not self.flab.load_all_data_completed:
            self.console_sleep(1)
        self.flab.load_all_uis_completed = False
        self.send_flab_command('load_all_uis()')
        while not self.flab.load_all_uis_completed:
            self.console_sleep(1)
        self.send_flab_command('load_all_models()')
        while not self.flab.load_all_models_completed:
            self.console_sleep(1)
        self.send_flab_command('load_all_tasks()')
        while not self.flab.load_all_tasks_completed:
            self.console_sleep(1)
        self.send_flab_command('start_asyncio_loop()')
        self.list_loaded_tasks()
        self.list_loaded_devices()
        self.list_loaded_data()
        self.list_loaded_uis()
        self.list_loaded_models()
        self.send_flab_command('set_project_path("' + str(project_path) + '")')



    def list_objects(self):
        self.list_loaded_tasks()
        self.list_loaded_devices()
        self.list_loaded_data()
        self.list_loaded_uis()
        self.list_loaded_models()

    def click_open_project(self):
        try:
            s = QFileDialog()
            s.setDirectory(self.projects_path)
            if sys.platform.startswith('darwin'):
                project_path = s.getExistingDirectory(self.MainWindow,
                                                      caption = 'Open Project - Select Project Folder',
                                                      options=QFileDialog.DontUseNativeDialog)
            else:
                project_path = s.getExistingDirectory(self.MainWindow,
                                                      caption = 'Open Project - Select Project Folder')
            if project_path != '':
                new = True
                # if sys.platform.startswith('darwin'):
                #     s.setDirectory(project_path + '/Environments')
                #     environment_path = s.getExistingDirectory(self.MainWindow,
                #                                                   caption='Open Project - Select Environment Folder',
                #                                                   options=QFileDialog.DontUseNativeDialog)
                # else:
                #     s.setDirectory(project_path + '\\Environments')
                #     environment_path = s.getExistingDirectory(self.MainWindow,
                #                                                   caption='Open Project - Select Environment Folder',
                #                                                   options=QFileDialog.DontUseNativeDialog)
                # self.flab_queue.put(environment_path)
                if self.project_path != 'NA':
                    new = False
                    self.display('Closing current project')
                    self.timer.stop()
                    self.send_flab_command('close_project()')
                    self.listWidget_tasks.clear()
                    self.listWidget_devices.clear()
                    self.listWidget_data.clear()
                    self.listWidget_variables.clear()
                    self.listWidget_uis.clear()
                    self.timer.start()
                    # self.flab.restart = True
                    # self.MainWindow.close()

                self.open_project(project_path, new)

        except Exception as e:
            self.flab.display('Error in opening project')
            self.flab.display(e)

    def console_sleep(self, seconds):
        loop = QEventLoop()
        QTimer.singleShot(seconds*1000, loop.quit)
        loop.exec_()

    def click_load_object(self, folder_string, object_type):
        try:
            if os.name == 'nt':
                folder_string.replace("/","\\")
                cwd = os.path.abspath(os.getcwd()) + folder_string
            else:
                folder_string.replace("\\","/")
                cwd = os.path.abspath(os.getcwd()) + folder_string
            object_dialog = OptionDialog.Ui_optionDialog()
            object_dialog.setupUi(object_dialog)
            dir_object_files = os.listdir(cwd)
            dir_object_list = []
            for file_name in dir_object_files:
                if file_name.__contains__('.py'):
                    object_name = file_name.replace('.py','')
                    dir_object_list.append(object_name)
            unloaded_object = eval("list(set(dir_object_list)-set(self.flab."+object_type+".keys()))")
            object_dialog.listWidget.addItems(unloaded_object)
            def get_selected_object():
                selected_items = object_dialog.listWidget.selectedItems()
                selected_object_names = []
                for item in selected_items:
                    selected_object_names.append(item.text())
                command = 'load_'+object_type+'('+str(selected_object_names)+')'
                self.send_flab_command(command)
                object_dialog.accept()
            object_dialog.buttonBox.accepted.connect(get_selected_object)
            object_dialog.exec()
            time.sleep(0.2)
        except Exception as e:
            self.flab.display('Error in file dialog')
            self.flab.display(e)
        finally:
            pass

    def click_reload_object(self,object_type, object_type_plural):
        try:
            object = eval("self.listWidget_"+object_type_plural+".selectedItems()")
            if object != '':
                for i in object:
                    command = 'reload_'+object_type+'("' + i.text() + '")'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading ' + object_type)
        finally:
            pass

    def list_loaded_devices(self):
        try:
            self.listWidget_devices.clear()
            for d in self.flab.devices.keys():
                if d not in self.loaded_device_list:
                    try:
                        self.listWidget_devices.addItem(self.flab.devices[d].get('device_name'))
                    except Exception as e:
                        self.flab.display('Error in listing device ' + str(d))
                        self.flab.display(e)
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
                        self.listWidget_tasks.addItem(self.flab.tasks[t].get('task_name'))
                    except Exception as e:
                        self.flab.display('Error in listing task ' + str(t))
                        self.flab.display(e)
        except Exception as e:
            self.flab.display('Error in listing tasks')
            self.flab.display(e)
        finally:
            pass

    def list_loaded_data(self):
        try:
            self.listWidget_data.clear()
            for d in self.flab.data.keys():
                if d not in self.loaded_data_list:
                    try:
                        self.listWidget_data.addItem(self.flab.data[d].get('data_name'))
                    except Exception as e:
                        self.flab.display('Error in listing data ' + str(d))
                        self.flab.display(e)
        except Exception as e:
            self.flab.display('Error in listing data')
            self.flab.display(e)
        finally:
            pass

    def list_loaded_uis(self):
        try:
            self.listWidget_uis.clear()

            for d in self.flab.uis.keys():
                if d not in self.loaded_uis_list:
                    try:
                        self.listWidget_uis.addItem(self.flab.uis[d].get('ui_name'))
                    except Exception as e:
                        self.flab.display('Error in listing ui ' + str(d))
                        self.flab.display(e)
        except Exception as e:
            self.flab.display('Error in listing ui')
            self.flab.display(e)
        finally:
            pass

    def list_loaded_models(self):
        try:
            self.listWidget_models.clear()
            for model_name in self.flab.models.keys():
                if model_name not in self.loaded_model_list:
                    try:
                        self.listWidget_models.addItem(self.flab.models[model_name].get('model_name'))
                    except Exception as e:
                        self.flab.display('Error in listing model ' + str(model_name))
                        self.flab.display(e)
        except Exception as e:
            self.flab.display('Error in listing models')
            self.flab.display(e)
        finally:
            pass

    def click_load_task(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + "\Tasks"
            else:
                cwd = os.path.abspath(os.getcwd()) + "/Tasks"
            tasks_dialog = OptionDialog.Ui_optionDialog()
            tasks_dialog.setupUi(tasks_dialog)
            dir_task_files = os.listdir(cwd)
            dir_task_list = []
            for file_name in dir_task_files:
                if file_name.__contains__('.py'):
                    task_name = file_name.replace('.py','')
                    dir_task_list.append(task_name)
            unloaded_tasks = list(set(dir_task_list)-set(self.flab.tasks.keys()))
            tasks_dialog.listWidget.addItems(unloaded_tasks)
            def get_selected_tasks():
                selected_items = tasks_dialog.listWidget.selectedItems()
                selected_task_names = []
                for item in selected_items:
                    selected_task_names.append(item.text())
                command = 'load_tasks('+str(selected_task_names)+')'
                self.send_flab_command(command)
                tasks_dialog.accept()
            tasks_dialog.buttonBox.accepted.connect(get_selected_tasks)
            tasks_dialog.exec()
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
                    full_args = self.flab.tasks[task_name].get_run_arguments()
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []
                        # this needs to be fixed - why is the code for opt_args missing?

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
            self.flab.display(f'Error in starting task: {e}')
        finally:
            pass

    def click_reload_task(self):
        try:
            tasks = self.listWidget_tasks.selectedItems()
            if tasks != '':
                for i in tasks:
                    command = 'reload_task("' + i.text() + '")'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading and starting task')
        finally:
            pass

    # def click_reload_start_task(self):
    #     try:
    #         self.click_reload_task()
    #         self.console_sleep(1)
    #         self.click_start_task()
    #     except Exception as e:
    #         self.flab.display(e)
    #         self.flab.display('Error in reloading and starting task')
    #     finally:
    #         pass

    def click_schedule_task(self):

        try:
            tasks = self.listWidget_tasks.selectedItems()
            if tasks != '':
                for i in tasks:
                    task_name = i.text()
                    full_args = self.flab.tasks[task_name].get_run_arguments()
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
                        time_dialog = DateTimeDialog.DateTimeDialog()
                        timestamp = time_dialog.get_timestamp()
                        command = 'schedule_task('+str(timestamp) + ',"' + i.text() + '",' + arg_combined_str + ')'
                    else:
                        time_dialog = DateTimeDialog.DateTimeDialog()
                        timestamp = time_dialog.get_timestamp()
                        command = 'schedule_task('+str(timestamp) + ',"' + i.text() + '")'
                    if timestamp > time.time()+3:
                        self.send_flab_command(command)
                    else:
                        self.display('Error in schedule task - time must be later than current time')
                        self.message('Error in schedule task - time must be later than current time')

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in starting task')
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

    def click_kill_task(self):
        task_to_kill = self.listWidget_running_tasks.selectedItems()
        if task_to_kill != []:
            command = 'kill_task("' + task_to_kill[0].text() + '")'
            self.send_flab_command(command)

    def click_kill_all_tasks(self):
        command = 'kill_all_tasks()'
        self.send_flab_command(command)

    def click_load_device(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + '\Devices'
            else:
                cwd = os.path.abspath(os.getcwd()) + '/Devices'

            devices_dialog = OptionDialog.Ui_optionDialog()
            devices_dialog.setupUi(devices_dialog)
            dir_device_files = os.listdir(cwd)
            dir_device_list = []
            for file_name in dir_device_files:
                if file_name.__contains__('.py'):
                    task_name = file_name.replace('.py', '')
                    dir_device_list.append(task_name)
            unloaded_devices = list(set(dir_device_list) - set(self.flab.devices.keys()))
            devices_dialog.listWidget.addItems(unloaded_devices)

            def get_selected_devices():
                selected_items = devices_dialog.listWidget.selectedItems()
                selected_device_names = []
                for item in selected_items:
                    selected_device_names.append(item.text())
                command = 'load_devices(' + str(selected_device_names) + ')'
                self.send_flab_command(command)
                devices_dialog.accept()

            devices_dialog.buttonBox.accepted.connect(get_selected_devices)
            devices_dialog.exec()
            time.sleep(0.1)
            self.list_loaded_devices()
        except Exception as e:
            self.flab.display('Error in device dialog')
            self.flab.display(e)

    def click_reload_device(self):
        try:
            device_name = self.listWidget_devices.selectedItems()

            if device_name != []:
                device_name = device_name[0].text()
                self.send_flab_command('reload_device("'+device_name+'")')
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading device: ' + device_name)
        finally:
            pass

    def listWidget_devices_clicked(self):
        try:
            device = self.listWidget_devices.selectedItems()
            self.listWidget_device_attributes.clear()
            self.listWidget_device_methods.clear()
            excluded_methods_list = [
                'get', 'get_flab', 'get_device_name', 'list_attributes', 'list_methods',
                'list_method_args', 'list_devices', 'set', 'set_flab', 'set_device_name'
            ]
            excluded_attributes_list = [
                'flab','device_name'
            ]
            if device != []:
                device_name = device[0].text()
                attribute_list = self.flab.devices[device_name].list_attributes()
                method_list = self.flab.devices[device_name].list_methods()
                for attribute_name in attribute_list:
                    if attribute_name not in excluded_attributes_list:
                        self.listWidget_device_attributes.addItem(attribute_name)
                for method_name in method_list:
                    if method_name not in excluded_methods_list:
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
            self.flab.display(e)

    def click_load_data(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + "\Data"
            else:
                cwd = os.path.abspath(os.getcwd()) + "/Data"
            data_dialog = OptionDialog.Ui_optionDialog()
            data_dialog.setupUi(data_dialog)
            dir_data_files = os.listdir(cwd)
            dir_data_list = []
            for file_name in dir_data_files:
                if file_name.__contains__('.py'):
                    data_name = file_name.replace('.py','')
                    dir_data_list.append(data_name)
            unloaded_data = list(set(dir_data_list)-set(self.flab.data.keys()))
            data_dialog.listWidget.addItems(unloaded_data)
            def get_selected_data():
                selected_items = data_dialog.listWidget.selectedItems()
                selected_data_names = []
                for item in selected_items:
                    selected_data_names.append(item.text())
                command = 'load_data_list('+str(selected_data_names)+')'
                self.send_flab_command(command)
                data_dialog.accept()
            data_dialog.buttonBox.accepted.connect(get_selected_data)
            data_dialog.exec()
            time.sleep(0.1)
            self.list_loaded_data()
        except Exception as e:
            self.flab.display('Error in file dialog')
            self.flab.display(e)

    def plot_message(self, message):
        self.label_plot_messages.setText(message)

    def click_plot_set_x_variable(self):
        try:
            self.plot_x_variable = self.comboBox_plot_x_variables.currentText()
            if self.plot_x_variable != None:
                self.plot_message('Set x variable: ' + self.plot_x_variable)
        except Exception as e:
            self.flab.display('Error in setting plot x variable')
            self.flab.display(e)
            self.plot_message('Error in setting plot x variable')
        finally:
            pass

    def click_plot_add_y_variable(self):
        try:
            new_y_variable = self.comboBox_plot_y_variables.currentText()
            if new_y_variable != None and not new_y_variable in self.plot_y_variables:
                self.plot_y_variables = self.plot_y_variables + [new_y_variable]
                self.plot_message('Set y variable: ' + new_y_variable)
                self.listWidget_plot_y_variables.addItem(new_y_variable)
        except Exception as e:
            self.flab.display('Error in setting plot y variable')
            self.flab.display(e)
            self.plot_message('Error in setting plot y variable')
        finally:
            pass

    def click_plot_remove_y_variable(self):
        try:
            y_variable = self.listWidget_plot_y_variables.selectedItems()
            if y_variable != []:
                variable_name = y_variable[0].text()
                self.plot_y_variables.remove(variable_name)
                row = self.listWidget_plot_y_variables.row(y_variable[0])
                self.listWidget_plot_y_variables.takeItem(row)
                self.plot_y_variables.remove(variable_name)
                self.plot_message('Removed y variable: ' + str(variable_name))
        except Exception as e:
            self.flab.display('Error in clearing y variables')
            self.flab.display(e)
            self.plot_message('Error in removing y variable')
        finally:
            pass

    def click_plot_clear_all_y_variables(self):
        try:
            self.listWidget_plot_y_variables.clear()
            self.plot_y_variables = []
            self.plot_message('Removed all y variables')
        except Exception as e:
            self.flab.display('Error in removing all y variables')
            self.flab.display(e)
            self.plot_message('Error in removing all y variables')
        finally:
            pass

    def click_live_plot(self):
        try:
            if self.plot_variables_on:
                self.pushButton_live_plot.setText('Start Live Plot')
                self.plot_variables_on = False
                self.plot_message('Plotting stopped')
            else:
                self.pushButton_live_plot.setText('Stop Live Plot')
                self.plot_variables_on = True
                self.plot_message('Plotting started')
        except Exception as e:
            self.flab.display('Error in plotting')
            self.flab.display(e)
            self.plot_message('Error in plotting')
        finally:
            pass

    def click_reload_data(self):
        try:
            data = self.listWidget_data.selectedItems()
            if data != '':
                for i in data:
                    command = 'reload_data("' + i.text() + '")'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading and starting task')
        finally:
            pass

    def listWidget_data_clicked(self):
        try:
            data = self.listWidget_data.selectedItems()
            self.listWidget_data_attributes.clear()
            self.listWidget_data_methods.clear()
            excluded_methods_list = [
                'get', 'get_flab', 'get_data_name', 'list_attributes',
                'list_method_args', 'list_methods', 'set', 'set_flab', 'set_data_name'
            ]
            excluded_attributes_list = [
                'flab','data_name'
            ]
            if data != []:
                data_name = data[0].text()
                attribute_list = self.flab.data[data_name].list_attributes()
                method_list = self.flab.data[data_name].list_methods()
                for attribute_name in attribute_list:
                    if attribute_name not in excluded_attributes_list:
                        self.listWidget_data_attributes.addItem(attribute_name)
                for method_name in method_list:
                    if method_name not in excluded_methods_list:
                        self.listWidget_data_methods.addItem(method_name)
        except Exception as e:
            self.flab.display('Error in displaying attributes of ' + data_name)
            self.flab.display(e)
        finally:
            pass


    def click_test_data_method(self):
        try:
            data_method = self.listWidget_data_methods.selectedItems()
            data_name = self.listWidget_data.selectedItems()

            if data_method != [] and data_name != []:
                data_name = data_name[0].text()
                data_method = data_method[0].text()
                full_args = self.flab.data[data_name].list_method_args(data_method)
                if len(full_args.args) > 1:
                    args_list = full_args.args[1:]
                    arg_list = []
                    opt_arg_list = []

                    for a in args_list:
                        if 'argument_descriptions' in dir(self.flab.devices[data_name]):
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for '
                                                                  + self.flab.devices[data_name].argument_descriptions[a])
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])
                        else:
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for ' + a )
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])

                    arg_combined_str = ','.join(arg_list)
                    command = 'display(self.flab.data["' + data_name + '"].' + data_method + '(' + arg_combined_str + '))'
                else:
                    command = 'display(self.flab.data["' + data_name + '"].' + data_method + '())'
                self.send_flab_command(command)
        except Exception as e:
            self.flab.display('Error in testing data method')
            self.flab.display(e)
        finally:
            pass

    def click_display_data_attribute(self):
        data_attribute = self.listWidget_data_attributes.selectedItems()
        data_name = self.listWidget_data.selectedItems()
        if data_attribute != [] and data_name != []:
            command = 'display(self.flab.data["' + data_name[0].text() + '"].get("' + data_attribute[0].text() + '"))'
            self.send_flab_command(command)

    def click_set_data_attribute(self):
        try:
            data_attribute = self.listWidget_data_attributes.selectedItems()
            data_name = self.listWidget_data.selectedItems()
            if data_attribute != [] and data_name != []:
                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set Data Attribute: ',
                                                                      'Enter value for  '
                                                                      + data_name[0].text() + ' : ' + data_attribute[0].text())
                if text[1] and text[0] != "":
                    command = 'data["' + data_name[0].text() + '"].set("' + data_attribute[0].text() + '",' + text[0] + ')'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display('Error in setting data attributes of ' + data_name)
            self.flab.display(e)

    def update_file(self):
        try:
            data_name = self.listWidget_data.selectedItems()
            if data_name != []:
                self.send_flab_command('update_data_file("'+data_name[0].text()+'")')
        except Exception as e:
            self.flab.display('Error in updating file:' + str(e))
        finally:
            pass

    def update_variable(self):
        try:
            data_name = self.listWidget_data.selectedItems()
            if data_name != []:
                self.send_flab_command('update_data_variable("' + data_name[0].text() + '")')

        except Exception as e:
            self.flab.display('Error in updating variable: ' + str(e))
        finally:
            pass

    def click_load_ui(self):
        self.click_load_object(r'/UIs','uis')
        self.list_loaded_uis()

    def click_reload_ui(self):
        self.click_reload_object('ui','uis')
        self.list_loaded_uis()

    def click_start_ui(self):
        try:
            uis = self.listWidget_uis.selectedItems()
            if uis != '':
                for i in uis:
                    ui_name = i.text()
                    full_args = inspect.getfullargspec(self.flab.uis[ui_name].get('run'))
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []

                        for a in args_list:
                            if 'argument_descriptions' in dir(self.flab.uis[ui_name]):
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for '
                                                                      + self.flab.uis[ui_name].argument_descriptions[a])
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])
                            else:
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a, 'Enter value for ' + a )
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])

                        arg_combined_str = ','.join(arg_list)
                        command = 'start_ui("' + i.text() + '",' + arg_combined_str + ')'
                    else:
                        command = 'start_ui("' + i.text() + '")'
                    self.send_flab_command(command)

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in starting ui')
        finally:
            pass

    def click_stop_ui(self):
        ui_to_stop = self.listWidget_uis.selectedItems()
        if ui_to_stop != []:
            command = 'stop_ui("' + ui_to_stop[0].text() + '")'
            self.send_flab_command(command)

    def click_load_model(self):
        try:
            if os.name == 'nt':
                cwd = os.path.abspath(os.getcwd()) + '\Models'
            else:
                cwd = os.path.abspath(os.getcwd()) + '/Models'

            models_dialog = OptionDialog.Ui_optionDialog()
            models_dialog.setupUi(models_dialog)
            dir_model_files = os.listdir(cwd)
            dir_model_list = []
            for file_name in dir_model_files:
                if file_name.__contains__('.py'):
                    task_name = file_name.replace('.py', '')
                    dir_model_list.append(task_name)
            unloaded_models = list(set(dir_model_list) - set(self.flab.models.keys()))
            models_dialog.listWidget.addItems(unloaded_models)

            def get_selected_models():
                selected_items = models_dialog.listWidget.selectedItems()
                selected_model_names = []
                for item in selected_items:
                    selected_model_names.append(item.text())
                command = 'load_models(' + str(selected_model_names) + ')'
                self.send_flab_command(command)
                models_dialog.accept()

            models_dialog.buttonBox.accepted.connect(get_selected_models)
            models_dialog.exec()
            time.sleep(0.1)
            self.list_loaded_models()
        except Exception as e:
            self.flab.display('Error in model dialog')
            self.flab.display(e)

    def click_reload_model(self):
        try:
            model_name = self.listWidget_models.selectedItems()

            if model_name != []:
                model_name = model_name[0].text()
                self.send_flab_command('reload_model("' + model_name + '")')
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in reloading model: ' + model_name)
        finally:
            pass

    def listWidget_models_clicked(self):
        try:
            model = self.listWidget_models.selectedItems()
            self.listWidget_model_attributes.clear()
            self.listWidget_model_methods.clear()
            excluded_methods_list = [
                'get', 'get_flab', 'get_model_name', 'list_attributes',
                'list_method_args', 'list_methods', 'set', 'set_flab', 'set_model_name'
            ]
            excluded_attributes_list = [
                'flab','model_name'
            ]
            if model != []:
                model_name = model[0].text()
                attribute_list = self.flab.models[model_name].list_attributes()
                method_list = self.flab.models[model_name].list_methods()
                for attribute_name in attribute_list:
                    if not attribute_name in excluded_attributes_list:
                        self.listWidget_model_attributes.addItem(attribute_name)
                for method_name in method_list:
                    if not method_name in excluded_methods_list:
                        self.listWidget_model_methods.addItem(method_name)
        except Exception as e:
            self.flab.display(e)

    def click_display_model_attribute(self):
        model_attribute = self.listWidget_model_attributes.selectedItems()
        model_name = self.listWidget_models.selectedItems()
        if model_attribute != [] and model_name != []:
            command = 'display(self.flab.models["' + model_name[0].text() + '"].get("' + model_attribute[
                0].text() + '"))'
            self.send_flab_command(command)

    def click_set_model_attribute(self):
        try:
            model_attribute = self.listWidget_model_attributes.selectedItems()
            model_name = self.listWidget_models.selectedItems()
            if model_attribute != [] and model_name != []:
                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Set model Attribute: ',
                                                      'Enter value for  '
                                                      + model_name[0].text() + ' : ' + model_attribute[0].text())
                if text[1] and text[0] != "":
                    command = 'models["' + model_name[0].text() + '"].set("' + model_attribute[0].text() + '",' + text[
                        0] + ')'
                    self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)

    def click_test_model_method(self):
        try:
            model_method = self.listWidget_model_methods.selectedItems()
            model_name = self.listWidget_models.selectedItems()

            if model_method != [] and model_name != []:
                model_name = model_name[0].text()
                model_method = model_method[0].text()
                full_args = self.flab.models[model_name].list_method_args(model_method)
                if len(full_args.args) > 1:
                    args_list = full_args.args[1:]
                    arg_list = []
                    opt_arg_list = []

                    for a in args_list:
                        if 'argument_descriptions' in dir(self.flab.models[model_name]):
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                  'Enter value for '
                                                                  + self.flab.models[model_name].argument_descriptions[
                                                                      a])
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])
                        else:
                            text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                  'Enter value for ' + a)
                            if text[1] and text[0] != "":
                                arg_list.append(text[0])

                    arg_combined_str = ','.join(arg_list)
                    command = 'display(self.flab.models["' + model_name + '"].' + model_method + '(' + arg_combined_str + '))'
                else:
                    command = 'display(self.flab.models["' + model_name + '"].' + model_method + '())'
                self.send_flab_command(command)
        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in starting task')
        finally:
            pass

    def click_get_model_attribute(self):
        model = self.listWidget_models.selectedItems()
        if model != []:
            model_name = model[0].text()
            attribute_list = self.flab.models[model_name].list_attributes()
            item = QtWidgets.QInputDialog.getItem(self.MainWindow, 'Attributes', 'Select an attribute', attribute_list,
                                                  0,
                                                  False)

    def click_evaluate_model(self):
        try:
            models = self.listWidget_models.selectedItems()
            if models != '':
                for model in models:
                    model_name = model.text()
                    full_args = inspect.getfullargspec(self.flab.models[model_name].get('evaluate'))
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []

                        for a in args_list:
                            if 'argument_descriptions' in dir(self.flab.models[model_name]):
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for '
                                                                      +
                                                                      self.flab.models[
                                                                          model_name].argument_descriptions[
                                                                          a])
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])
                            else:
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for ' + a)
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])

                        arg_combined_str = ','.join(arg_list)
                        command = 'evaluate_model("' + model.text() + '",' + arg_combined_str + ')'
                    else:
                        command = 'evaluate_model("' + model.text() + '")'
                    self.send_flab_command(command)

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in model evaluation')
        finally:
            pass

    def click_train_model(self):
        try:
            models = self.listWidget_models.selectedItems()
            if models != '':
                for model in models:
                    model_name = model.text()
                    full_args = inspect.getfullargspec(self.flab.models[model_name].get('train'))
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []

                        for a in args_list:
                            if 'argument_descriptions' in dir(self.flab.models[model_name]):
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for '
                                                                      +
                                                                      self.flab.models[model_name].argument_descriptions[
                                                                          a])
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])
                            else:
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for ' + a)
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])

                        arg_combined_str = ','.join(arg_list)
                        command = 'train_model("' + model.text() + '",' + arg_combined_str + ')'
                    else:
                        command = 'train_model("' + model.text() + '")'
                    self.send_flab_command(command)

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in model training')
        finally:
            pass

    def click_model_predict(self):
        try:
            models = self.listWidget_models.selectedItems()
            if models != '':
                for model in models:
                    model_name = model.text()
                    full_args = inspect.getfullargspec(self.flab.models[model_name].get('predict'))
                    if len(full_args.args) > 1:
                        args_list = full_args.args[1:]
                        arg_list = []
                        opt_arg_list = []

                        for a in args_list:
                            if 'argument_descriptions' in dir(self.flab.models[model_name]):
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for '
                                                                      +
                                                                      self.flab.models[model_name].argument_descriptions[
                                                                          a])
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])
                            else:
                                text = QtWidgets.QInputDialog.getText(self.MainWindow, 'Argument Input: ' + a,
                                                                      'Enter value for ' + a)
                                if text[1] and text[0] != "":
                                    arg_list.append(text[0])

                        arg_combined_str = ','.join(arg_list)
                        command = 'predict_model("' + model.text() + '",' + arg_combined_str + ')'
                    else:
                        command = 'predict_model("' + model.text() + '")'
                    self.send_flab_command(command)

        except Exception as e:
            self.flab.display(e)
            self.flab.display('Error in model prediction')
        finally:
            pass

    def onReturn(self):
        try:
            command = self.lineEdit.text()
            self.send_flab_command(command)
        except Exception as e:
            self.flab.display('Error in flab command' + str(command))
            self.flab.display(e)

    def restart(self):
        self.flab.restart = True
        self.flab.project_path = 'NA'
        self.MainWindow.close()
        #self.close()

    def restart_project(self):
        self.flab.restart = True
        self.flab.project_path = self.project_path
        self.MainWindow.close()
        #self.close()

    def send_flab_command(self, command):
        try:
            timestamp = str(datetime.datetime.now().strftime('%D %H:%M:%S'))
            self.textBrowser_flab_console.append(timestamp + '  >  ' + command)
            self.lineEdit.setText('')
            if not command == '':
                self.lineEdit.commandHistory.insert(1,command)
                self.lineEdit.commandHistoryPosition = 0
                if command == 'exit' or command == 'close':
                    self.close()
                if command == 'restart':
                    self.restart()
                elif command == 'restart project':
                    self.restart_project()
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
                        self.textBrowser_flab_console.append('error in flab command: ' + str(command))
                        self.textBrowser_flab_console.append(str(e))
        except Exception as e:
            self.flab.display('error in flab command: ' + str(command))
            self.flab.display(e)
        finally:
            pass

    def start_queue_thread(self):
        self.qthread = QueueThread(self)
        #self.qthread.finished.connect(self.app.exit)
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
            current_time = time.time()

            #task tracking
            running_tasks = self.flab.get_running_task_names()
            task_history = self.flab.get_task_history()

            #remove dead tasks
            tasks_to_pop = []

            for running_task_name in self.running_task_list:
                if running_task_name not in running_tasks:
                    item_row = self.listWidget_running_tasks.row(self.running_task_list[running_task_name])
                    self.listWidget_running_tasks.takeItem(item_row)
                    tasks_to_pop.append(running_task_name)
            for p in tasks_to_pop:
                self.running_task_list.pop(p)
                self.send_flab_command('update_task_end_time("'+str(p)+'",'+str(current_time)+')')

            #add new tasks
            for running_task_name in task_history:
                match = running_task_name in self.task_bar_items
                if not match:
                    self.listWidget_running_tasks.addItem(running_task_name)
                    widget_item = self.listWidget_running_tasks.findItems(running_task_name,QtCore.Qt.MatchFlag.MatchExactly)
                    self.running_task_list.update({running_task_name:widget_item[0]})

                    #create the task bar item
                    self.task_bar_items[running_task_name] = pg.BarGraphItem(x0=[task_history[running_task_name][0]],
                                                                             y0 = [len(self.task_bar_items)], #y0=[len(self.running_task_list)-1],
                                                                             width=0,
                                                                             height=0.9,
                                                                             brush=self.task_bar_color_scheme[len(task_history)%3])
                    self.graphicsView_tasks_bar.addItem(self.task_bar_items[running_task_name])

                    #create the label for the task
                    task_text = pg.TextItem(running_task_name)
                    task_text.setPos(current_time, len(self.task_bar_items))
                    #task_text.setPos(current_time, len(self.running_task_list))
                    self.graphicsView_tasks_bar.addItem(task_text)

            #update task bar
            for task_name in running_tasks:
                if task_name in self.task_bar_items:
                    self.task_bar_items[task_name].setOpts(width=current_time - self.flab.task_history[task_name][0])
                    #self.flab.display(current_time - self.task_history[task_name][0])

            #update task bar time line
            self.tasks_time_line.setData([current_time,current_time], [0,len(self.running_task_list)])
            self.flab.vars['history'] = self.flab.get_task_history()

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
                        self.loaded_device_list.pop(p)

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

                        #variable plot widget
                        variable_index = self.comboBox_plot_x_variables.findText(variable_name)
                        self.comboBox_plot_x_variables.removeItem(variable_index)
                        self.comboBox_plot_y_variables.removeItem(variable_index)

                        match = self.listWidget_plot_y_variables.findItems(str(variable_name), QtCore.Qt.MatchFlag.MatchExactly)
                        if match != []:
                            item_row = self.listWidget_plot_y_variables.row(match[0])
                            self.listWidget_plot_y_variables.takeItem(item_row)

                    for p in variables_to_pop:
                        self.loaded_variable_list.pop(p)

                # add new variables
                for variable_name in loaded_variables:
                    match = self.listWidget_variables.findItems(str(variable_name), QtCore.Qt.MatchFlag.MatchExactly)
                    if match == []:
                        self.listWidget_variables.addItem(variable_name)
                        widget_item = self.listWidget_variables.findItems(str(variable_name), QtCore.Qt.MatchFlag.MatchExactly)
                        self.loaded_variable_list.update({variable_name: widget_item[0]})
                        self.comboBox_plot_x_variables.addItem(variable_name)
                        self.comboBox_plot_y_variables.addItem(variable_name)

                # update variable values
                self.listWidget_variable_values.clear()
                variable = self.listWidget_variables.selectedItems()
                if variable != []:
                    variable_name = variable[0].text()
                    variable_value = str(self.flab.vars[variable_name])
                    self.listWidget_variable_values.addItem(variable_value)

            #variable plotting
            if self.plot_variables_on:
                try:
                    for y_variable in self.plot_y_variables:
                        #create new plot items for newly added variables
                        match = y_variable in self.plot_items
                        if not match:
                            # create the plot item
                            color = self.plot_variable_colors[len(self.plot_y_variables) % len(self.plot_variable_colors)]
                            self.plot_items[y_variable] = self.graphicsView_plot_2d_plot.plot(
                                self.flab.vars[self.plot_x_variable],
                                self.flab.vars[y_variable],
                                name = y_variable,
                                symbol = 'o',
                                pen = color,
                                brush = 0.2,
                                symbolPen = color,
                                symbolBrush = 0.2,
                                symbolSize = 14)
                        else:
                             # update plot
                             self.plot_items[y_variable].setData(
                                 self.flab.vars[self.plot_x_variable],
                                 self.flab.vars[y_variable])
                except Exception as e:
                    self.plot_message('Error in plotting ' + str(e))
                finally:
                    pass


            #data tracking
            data_to_pop = []
            loaded_data = self.flab.data.keys()

            if self.flab.data is not {}:
                for data_name in self.loaded_data_list:
                    if data_name not in loaded_data:
                        item_row = self.listWidget_data.row(self.loaded_data_list[data_name])
                        self.listWidget_data.takeItem(item_row)
                        data_to_pop.append(data_name)
                    for p in data_to_pop:
                        self.loaded_data_list.pop(p)

                #add new data
                for data_name in loaded_data:
                    match = self.listWidget_data.findItems(data_name, QtCore.Qt.MatchFlag.MatchExactly)
                    if match == []:
                        self.listWidget_data.addItem(data_name)
                        widget_item = self.listWidget_data.findItems(data_name, QtCore.Qt.MatchFlag.MatchExactly)
                        self.loaded_data_list.update({data_name: widget_item[0]})

            #ui tracking
            running_uis = self.flab.get_running_ui_names()

            #remove dead uis
            uis_to_pop = []
            for ui_name in self.running_ui_list:
                if ui_name not in running_uis:
                    item_row = self.listWidget_running_uis.row(self.running_ui_list[ui_name])
                    self.listWidget_running_uis.takeItem(item_row)
                    uis_to_pop.append(ui_name)
            for p in uis_to_pop:
                self.running_ui_list.pop(p)

            #add new uis
            for ui_name in running_uis:
                match = self.listWidget_running_uis.findItems(ui_name,QtCore.Qt.MatchFlag.MatchExactly)
                if match == []:
                    self.listWidget_running_uis.addItem(ui_name)
                    widget_item = self.listWidget_running_uis.findItems(ui_name,QtCore.Qt.MatchFlag.MatchExactly)
                    self.running_ui_list.update({ui_name:widget_item[0]})

        except Exception as e:
            if str(e) != 'dictionary changed size during iteration':
                self.flab.display('Error in console live update')
                self.flab.display(e)
            else:
                pass

        finally:
            pass

    def clean_cache(self):
        gc.collect(generation=2)

    def display(self, s):
        try:
            timestamp = str(datetime.datetime.now().strftime('%D %H:%M:%S'))
            self.textBrowser_flab_console.append(timestamp + '  |  ' + str(s))
            self.textBrowser_flab_console.moveCursor(QtGui.QTextCursor.End)
            self.textBrowser_flab_console.ensureCursorVisible()
        except Exception as e:
            self.flab.display(e)


    def message(self, m):
        if m:
            self.msg = QtWidgets.QDialog()
            self.msg.setStyleSheet("background-color: rgba(0, 0, 0, 0);")  # Semi-transparent black background
            self.msg.setWindowTitle("Flab Message")
            self.layout = QtWidgets.QVBoxLayout(self.msg)
            mess = QtWidgets.QLabel(str(m))
            self.layout.addWidget(mess)
            self.msg.setWindowFlags(QtCore.Qt.WindowFlags(QtCore.Qt.WindowCloseButtonHint))
            self.msg.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.NoDropShadowWindowHint)
            self.msg.setAttribute(Qt.WA_TranslucentBackground)

            self.msg.show()

    def flab_console_command(self):
        command = self.lineEdit_flab_console.text()
        timestamp = str(datetime.datetime.now().strftime('%D %H:%M:%S'))
        self.textBrowser_flab_console.append(timestamp + '  >  '+command)
        self.lineEdit_flab_console.setText('')
        self.flab_queue.put(command)


    # moving bar plot for task scheduler and variable plotter
    def plot_setup(self):
        try:
            #initialize run time variable
            self.start_time = time.time()

            #color assignemnts
            pen_time = pg.mkPen(color=(250, 171, 42), width=10)

            #time axis
            time_axis = pg.DateAxisItem()

            self.graphicsView_tasks_bar.setBackground((74, 81, 87))
            self.graphicsView_tasks_bar.setAxisItems({'bottom': time_axis})
            self.tasks_time_line = self.graphicsView_tasks_bar.plot([self.start_time,self.start_time],[0,1],pen=pen_time)

            self.graphicsView_plot_2d_plot.setBackground((74, 81, 87))
            self.graphicsView_plot_2d_plot.addLegend()
            self.graphicsView_plot_2d_plot.enableAutoRange()
            self.graphicsView_plot_2d_plot.setAutoVisible()
            self.plot_variable_colors = ['r', 'g', 'b', 'c', 'm', 'y', 'w']



            #self.plot_variable_legend = pg.LegendItem(offset=(70, 30))
            #self.plot_variable_legend.setParentItem(self.graphicsView_plot_2d_plot.getViewBox())

        except Exception as e:
            print('Erorr in plot setup')
            print(e)
        finally:
            pass


    def buildData(self, data):
        stamps = sorted(data.keys())
        zero = min(stamps)
        x0 = []
        y0 = []
        width = []
        brushes = []
        for i, stamp in enumerate(stamps):
            try:
                nextStamp = stamps[i + 1]
            except:
                nextStamp = stamp + 1
            x0.append(stamp - zero)
            y0.append(data[stamp])
            width.append(nextStamp - stamp)
            brushes.append(QtGui.QColor(QtCore.Qt.GlobalColor(data[stamp])))


class QueueThread(QThread):

    print_str = QtCore.pyqtSignal(str)

    def __init__(self, ui):
        self.ui = ui
        super().__init__()

    def run(self):

        while self.ui.MainWindow.is_running:
            try:
                s = self.ui.ui_queue.get(block=True, timeout = 30)
                if s != "close" and s != "restart" and s != 'exit':
                    self.print_str.emit(str(s))
                else:
                    self.ui.close()
                    self.ui.MainWindow.is_running = False
                del s
            except Exception as e:
                if str(e) == '':
                    pass
                else:
                    self.print_str.emit(str(repr(e)))
            finally:
                pass





