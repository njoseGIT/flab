#Hello World UI Actions

class Actions():

    actions_name = 'HelloWorldActions'

    def __init__(self, flab):
        self.flab = flab

    def configure_actions(self):
        self.pushButton.clicked.connect(self.hello_world)

    def hello_world(self):
        self.label.setText('Hello World')


