from flab import BootManager
b = BootManager.BootManager()
f = b.create_flab_proxy('','')

f.load_task('HelloWorldTask')