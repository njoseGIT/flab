# Flab 3
# Distributed under GNU GPL v3
# Author: Nicholas Jose

"""
The EnvironmentManager module contains methods for handling version control and external packages
"""

import pkg_resources
import sys
import os
import subprocess

class EnvironmentManager():
    """
    The EnvironmentManager module contains attributes and methods for configuring the running environment of a flab project
    """

    installed_packages = {} # a dictionary of installed packages
    environment_name = ''
    environment_path = r''

    def __init__(self):
        """
        Constructs the manager
        """
        pass

    def get_environment_info(self) -> str:
        """
        gets the current environment, whether the base interpreter or virtual environment

        :return: environment_name, environment_path
        """
        environment_name = ''
        environment_path = ''
        try:
            virtual_env = os.environ.get("VIRTUAL_ENV")
            if virtual_env:
                environment_name = os.path.basename(virtual_env)
                environment_path = os.path.abspath(virtual_env)
            else:
                environment_name = os.path.basename(os.path.abspath(os.path.join(sys.prefix, "..")))
                environment_path = os.path.abspath(os.path.join(sys.prefix, ".."))
        except Exception as e:
            self.display('Error in getting environment information')
            self.display(e)
        finally:
            self.environment_name, self.environment_path = environment_name, environment_path
            return environment_name, environment_path

    def get_installed_packages(self) -> dict:
        """
        returns a dictionary of the installed packages

        :returns: dict
        """
        package_info = {}
        try:
            installed_packages = pkg_resources.working_set
            for package in installed_packages:
                package_name = package.project_name
                package_version = package.version
                try:
                    package_description = package.get_metadata('METADATA')
                    package_description_lines = package_description.split('\n')
                    brief_description = next(
                        (line.split(': ', 1)[1] for line in package_description_lines if line.startswith('Summary:')), '')
                except Exception:
                    brief_description = 'No description exists'
                finally:
                    pass
                package_info[package_name] = [package_version, brief_description]
        except Exception as e:
            self.display('Error in getting installed packages')
            self.display(e)
        finally:
            self.installed_packages = package_info
            return package_info

    def install_package(self,package_name) -> bool:
        """
        installs a given package using the pip method

        :param package_name: name of the package to be installed
        :type package_name: str
        :return:
        """
        result = False
        try:
            python_executable = os.path.join(self.environment_path, "bin",
                                             "python") if sys.platform != "win32" else os.path.join(self.environment_path,
                                                                                                    "Scripts",
                                                                                                    "python.exe")
            result = subprocess.run([python_executable, "-m", "pip", "install", package_name],
                                    capture_output=True, text=True, check=True)
            self.display(result.stdout)
            result = True
        except Exception as e:
            self.display('Error in installing ' + str(package_name))
            self.display(e.stdout)
            result = False
        finally:
            self.installed_packages = self.get_installed_packages()
            return result

    def uninstall_package(self,package_name) -> bool:
        """
        Uninstallas a package from the current environment.

        :param package_name: name of the package
        :type package_name: str

        :return: True if successful, False if unsuccessful
        """
        result = False
        try:
            python_executable = os.path.join(self.environment_path, "bin",
                                             "python") if sys.platform != "win32" else os.path.join(self.environment_path,
                                                                                                    "Scripts",
                                                                                                    "python.exe")
            result = subprocess.run([python_executable, "-m", "pip", "uninstall", package_name,"-y"],
                                    capture_output=True, text=True, check=True)
            self.display(result.stdout)
            result = True
        except Exception as e:
            self.display('Error in uninstalling ' + str(package_name))
            self.display(e.stdout)
            result = False
        finally:
            self.installed_packages = self.get_installed_packages()
            return result

    def create_virtual_environment(self, virtual_environment_name, target_directory, python_interpreter) -> None:
        """
        Creates a virtual environment

        :param virtual_environment_name: name of the virtual environment
        :tupe virtual_environment_name: str

        :param target_directory: path to the target virtual environment directory
        :type target_directory: str

        :param python_interpreter: path to the python interpreter
        :type python_interpreter: str

        :return: None
        """
        try:
            venv_path = os.path.join(target_directory, virtual_environment_name)
            subprocess.check_call([python_interpreter, "-m", "venv", venv_path, "--clear"])
            self.display("Virtual environment " + str(virtual_environment_name) + " created successfully in " +
                         str(target_directory) + "using Python interpreter: " + str(python_interpreter))
        except Exception as e:
            self.display("Error creating virtual environment" + str(virtual_environment_name))
            self.display(e)
        finally:
            pass