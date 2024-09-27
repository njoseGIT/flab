# Console3
# A package of methods for booting Console3
# Nicholas A. Jose
import sys
import os
from flab import BootManager
from flab_console.Tasks import ConsoleUIProcess, ConsoleFlabProcess

def boot():
    """
    A method for booting Console3

    :returns: None
    """

    try:
        restart = True
        project_path = 'NA'
        while restart:
            boot_manager = BootManager.BootManager(print_status=False)

            ui_queue = boot_manager.create_queue()
            flab_queue = boot_manager.create_queue()

            f = boot_manager.create_flab_proxy(ui_queue = ui_queue, flab_queue = flab_queue, print_status = False)
            cwd = os.getcwd()

            project_path = 'NA'

            f.project_path = project_path
            f.tasks.update({'ConsoleUIProcess': ConsoleUIProcess.Task(f)})
            f.tasks.update({'ConsoleFlabProcess': ConsoleFlabProcess.Task(f)})

            p1 = boot_manager.start_process(f, 'ConsoleUIProcess', f, ui_queue, flab_queue, blocking = False, project_path = project_path)
            p2 = boot_manager.start_process(f, 'ConsoleFlabProcess', f, flab_queue, ui_queue, blocking = False)

            p1.join()
            p2.join()

            restart = f.restart
            project_path = f.project_path
            boot_manager.shutdown()
        sys.exit()

    except Exception as e:
        if str(e) != 'server not yet started':
            print('Boot error:')
            print(e)

    finally:
        pass

if __name__ == '__main__':
    boot()
