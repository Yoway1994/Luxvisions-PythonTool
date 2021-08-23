from configparser import ConfigParser as cfg
from function_flow import execute_function_flow

def main():
    cfg_input = cfg()
    cfg_input.read("command.ini")
    execute_function_flow(cfg_input)
    return None

if __name__ == "__main__":
    main()