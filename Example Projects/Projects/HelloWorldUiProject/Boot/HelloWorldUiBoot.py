from flab import BootManager

import os

if __name__ == '__main__':
    cwd = os.getcwd()
    if 'Boot' in cwd or 'Scripts' in cwd:
        os.chdir('..')

    boot_manager = BootManager.BootManager()

    ui_queue = boot_manager.create_queue()
    flab_queue = boot_manager.create_queue()

    f = boot_manager.create_flab_proxy(ui_queue, flab_queue)

    f.convert_ui('HelloWorldDesign')
    f.load_ui('HelloWorldUi')
    f.uis['HelloWorldUi'].run()