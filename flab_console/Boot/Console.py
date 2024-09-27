# Console3
# A package of methods for booting Console3
# Nicholas A. Jose

def boot():
    """
    A method for booting Console3

    :returns: None
    """
    import sys
    import os

    # configure working path
    cwd = os.getcwd()
    par1 = os.path.abspath(os.path.join(cwd, '..'))
    par2 = os.path.abspath(os.path.join(par1, '..'))
    sys.path.append(par2)
    sys.path.append(par1)

    from flab import BootManager
    from Tasks import ConsoleUIProcess, ConsoleFlabProcess

    try:
        restart = True
        project_path = 'NA'
        while restart:
            boot_manager = BootManager.BootManager(print_status=False)

            ui_queue = boot_manager.create_queue()
            flab_queue = boot_manager.create_queue()

            f = boot_manager.create_flab_proxy(ui_queue = ui_queue, flab_queue = flab_queue, print_status = False)
            f.project_path = project_path
            cwd = os.getcwd()

            f.tasks.update({'ConsoleUIProcess': ConsoleUIProcess.Task(f)})
            f.tasks.update({'ConsoleFlabProcess': ConsoleFlabProcess.Task(f)})

            p1 = boot_manager.start_process(f, 'ConsoleUIProcess', f, ui_queue, flab_queue, blocking = False, project_path = 'NA')
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
