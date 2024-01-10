from flab3.Templates import TaskTemplate

class Task(TaskTemplate.Task):

    task_name = 'DataTestTask'
    task_type = 'thread'

    def run(self):
        """
        An example task which shows the functionality of flab data classes.

        :returns: None
        """
        try:
            self.flab.display('Updating variables from files')

            self.flab.data['CsvDataExample'].update_variable()
            self.flab.data['JsonDataExample'].update_variable()
            self.flab.data['CsvDataExample'].update_variable()

            self.flab.display(
                'csv_data: ' + str(self.flab.vars['csv_data']) + '\n'
                'xlsx_data: ' + str(self.flab.vars['xlsx_data']) + '\n'
                'csv_data: ' + str(self.flab.vars['csv_data'])
            )

            self.flab.display('Changing variable values')

            # change the variables
            self.flab.vars['json_data'] = [4, 5, 6]
            self.flab.vars['csv_data'] = [4, 5, 6]
            self.flab.vars['xlsx_data'] = [4, 5, 6]

            self.flab.display(
                'csv_data: ' + str(self.flab.vars['csv_data']) + '\n'
                'xlsx_data: ' + str(self.flab.vars['xlsx_data']) + '\n'
                'csv_data: ' + str(self.flab.vars['csv_data'])
            )

            self.flab.display('Updating the files')

            self.flab.data['CsvDataExample'].update_file()
            self.flab.data['JsonDataExample'].update_file()
            self.flab.data['CsvDataExample'].update_file()

        except Exception as e:
            self.flab.display('Error in ' + self.task_name)
            self.flab.display(str(e))

        finally:
            pass

    def stop(self):
        self.flab.vars['DataTestTask_stopped'] = True #a flag to stop the script. This is unused in this example.