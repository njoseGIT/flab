# JsonDataExample.py
# An example data class for writing and reading json files
# Distributed under GNU GPL v3
# Nicholas A. Jose

from flab3.Templates import DataTemplate
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
