# XlsxDataExample.py
# An example data class for writing and reading xlsx files
# Distributed under GNU GPL v3
# Nicholas A. Jose

from flab.Templates import DataTemplate
import os
import pandas

class Data(DataTemplate.Data):

    data_name = 'XlsxDataExample'  # name of the data object
    file_path = os.getcwd() + '\\Files\\example.xlsx'  # path of the excel file
    sheet_name = 'Sheet1'  # the name of the sheet within the excel file
    variable_names = ['xlsx_data']  # names of variables that are stored

    def update_variable(self):
        """
        Updates the variable as a list from an excel table, where the variable names are the headers of each column,
        and the cells of each row are an element of the variable list.
        Note - this overwrites the existing variable.

        Example:

            Excel:
            |  a  |  b  |
            -------------
            |  1  |  3  |
            -------------
            |  2  |  4  |

            variables:
            {'a': [1, 2], 'b':[3, 4]}

        :returns: None

        """
        try:

            # Read the Excel file into a DataFrame
            data_frame = pandas.read_excel(self.file_path, sheet_name = self.sheet_name)

            # Convert the DataFrame into a dictionary (list of dictionaries)
            data_dict = data_frame.to_dict(orient='list')

            # update the variables dictionary with the parsed data
            self.flab.vars.update(data_dict)

        except Exception as e:
            self.flab.display('Error in updating variable of ' + self.data_name)
            self.flab.display(e)

        finally:
            pass

    def update_file(self):
        """
        Updates the excel file with variable values, where the variable names are the headers of each column,
        and the cells of each row are an element of the variable list
        Note - this overwrites the existing file.

        Example:

            variables:
            {'a': [1, 2], 'b':[3, 4]}

            Excel:
            |  a  |  b  |
            -------------
            |  1  |  3  |
            -------------
            |  2  |  4  |

        """

        try:
            # get the sub-dictionary of variables to write
            subset_dict = {key: self.flab.vars[key] for key in self.variable_names}

            # fill in empty cells
            filled_subset_dict = {key: pandas.Series(value) for key, value in subset_dict.items()}

            # Convert the dictionary into a Pandas DataFrame
            df = pandas.DataFrame.from_dict(filled_subset_dict)

            # Save the DataFrame to an Excel file
            df.to_excel(self.file_path, index=False)
        except Exception as e:
            self.flab.display('Error in updating file of ' + self.data_name)
            self.flab.display(e)

        finally:
            pass