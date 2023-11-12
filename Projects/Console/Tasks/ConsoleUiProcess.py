from Projects.Console.UIs import ConsoleUI

class Task():
    task_name = 'ConsoleUiProcess'
    queues = ()
    proxies = ()
    pipes = ()

    def __init__(self, flab):
        self.flab = flab

    #method called when process is running
    def run(self, flab, in_queue, out_queue):
        self.flab = flab
        self.in_queue = in_queue
        self.out_queue = out_queue
        ui = ConsoleUI.Ui_MainWindow(flab, self.in_queue, self.out_queue)
        ui.run()




