from flab_console.UIs import ConsoleDesign, ConsoleActions

class GUI(ConsoleDesign.Ui_MainWindow, ConsoleActions.Actions):

    def __init__(self, flab, ui_queue, flab_queue, project_path = '', projects_path = ''):
        self.flab = flab
        self.ui_queue = ui_queue
        self.flab_queue = flab_queue
        self.project_path = project_path
        self.projects_path = projects_path

    def run(self):
        try:
            self.create_window()
            self.configure_actions()
            self.start_queue_thread()
            self.MainWindow.show()
            if self.flab.project_path != '' and self.flab.project_path != 'NA':
                self.open_project(self.flab.project_path)
            else:
                self.click_open_project()

        except Exception as e:
            print('Error in starting Console3UI')
            print(e)

        finally:
            pass

