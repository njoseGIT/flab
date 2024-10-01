# CsvDataExample.py
# An example data class for writing and reading csv files
# Distributed under GNU GPL v3
# Nicholas A. Jose

from flab.Templates import DataTemplate
import os
import pandas

class Data(DataTemplate.Data):

    data_name = 'CsvDataExample' #name of the data object

    file_path = os.getcwd() + '\\Files\\example.csv' # path of the file
    variable_names = ['csv_data']  # names of variables that are stored

    def update_variable(self):
        """
        reads the csv from the file path and coverts to a dictionary, where the header of the csv file
        represents the keys of the dictionary, and the columns are lists within the dictionary

        Example:

            csv:
            a, b, c
            1, 2, 3
            4, 5, 6

            variables:
            {a: [1, 4], b:[2, 5], c:[3, 6]}

        :returns: None
        """
        try:
            # create a dataframe from the csv file
            dataframe = pandas.read_csv(self.file_path)
            # convert the dataframe into a dictionary
            data_dict = dataframe.to_dict(orient='list')
            # update the vars dictionary
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
            {a: [1, 2], b:[3, 4]}

            csv:
            a, b
            1, 3
            2, 4

        """

        try:
            # get the sub-dictionary of variables to write
            subset_dict = {key: self.flab.vars[key] for key in self.variable_names}
            # fill in empty cells
            filled_subset_dict = {key: pandas.Series(value) for key, value in subset_dict.items()}
            # Convert the dictionary into a Pandas DataFrame
            dataframe = pandas.DataFrame.from_dict(filled_subset_dict)
            # Save the DataFrame to an Excel file
            dataframe.to_csv(self.file_path, index=False)

        except Exception as e:
            self.flab.display('Error in updating file of ' + self.data_name)
            self.flab.display(e)

        finally:
            pass
