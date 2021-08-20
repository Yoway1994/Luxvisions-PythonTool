import configparser
from function_flow import execute_function_flow

class IoFlow:
    def __init__(self,):
        self.cfg_input = InputCommand("command.ini")
        self.msg_output = OutputMessage()
        execute_function_flow(self.cfg_input, self.msg_output)

class InputCommand(configparser.ConfigParser):
    def __init__(self, cmd_file):
        configparser.ConfigParser.__init__(self)
        self.read(cmd_file)

class OutputMessage:
    def __init__(self):
        self.s_text = ""

    def print_on_cmd(self):
        print(self.s_text)
        return None

    def to_log(self):
        return None

