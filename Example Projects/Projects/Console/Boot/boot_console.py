from flab import BootManager
import os
import sys
import time

if __name__ == '__main__':
    cwd = os.getcwd()
    if 'Boot' in cwd:
        os.chdir('..')

    boot_manager = BootManager.BootManager()

    ui_queue = boot_manager.create_queue()
    flab_queue = boot_manager.create_queue()

    f = boot_manager.create_flab_proxy(ui_queue, flab_queue)

    f.load_task('ConsoleUiProcess')
    f.load_task('ConsoleFlabProcess')

    time.sleep(5)

    p1 = boot_manager.start_process(f, 'ConsoleUiProcess', f, ui_queue, flab_queue, blocking = False)
    p2 = boot_manager.start_process(f, 'ConsoleFlabProcess', f, flab_queue, ui_queue, blocking = False)
    p1.join()
    p2.join()

    boot_manager.shutdown()
    sys.exit()


