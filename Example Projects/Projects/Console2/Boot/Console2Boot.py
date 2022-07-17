#Console2Boot
#A boot script for an interactive Flab development application - Flab 2
#Compatible with Python 3.9+
#Requires installation of PyQt5 v.5.15+ and flab v.1.1.2
#Distributed under GNU GPL v3
#Nicholas A. Jose
#Feb 2022

import os
import sys

cwd = os.getcwd()

par1 = os.path.abspath(os.path.join(cwd, '..'))
par2 = os.path.abspath(os.path.join(par1, '..'))
sys.path.append(par2)
sys.path.append(par1)

from flab import BootManager
from Tasks import Console2UIProcess, ConsoleFlabProcess

if __name__ == '__main__':
    try:
        boot_manager = BootManager.BootManager()

        ui_queue = boot_manager.create_queue()
        flab_queue = boot_manager.create_queue()

        f = boot_manager.create_flab_proxy(ui_queue = ui_queue, flab_queue = flab_queue, print_status = False)

        f.tasks.update({'Console2UIProcess':Console2UIProcess.Task(f)})
        f.tasks.update({'ConsoleFlabProcess':ConsoleFlabProcess.Task(f)})

        p1 = boot_manager.start_process(f, 'Console2UIProcess', f, ui_queue, flab_queue, blocking = False)
        p2 = boot_manager.start_process(f, 'ConsoleFlabProcess', f, flab_queue, ui_queue, blocking = False)
        p1.join()
        p2.join()

        boot_manager.shutdown()
        sys.exit()

    except Exception as e:
        print('Boot error:')
        print(e)


