from io_flow import IoFlow

class Interface:
    def __init__(self):
        self.io_flow = IoFlow()

    def execute_from_cmd(self):
        self.io_flow.msg_output.print_on_cmd()
        return None

    def execute_from_app(self):
        return None