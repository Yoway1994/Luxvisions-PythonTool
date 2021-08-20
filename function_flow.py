from error import *
from golden_limit_select import GoldenLimitSelect

def execute_function_flow(cfg, msg):
    command = display_section_on_cmd(cfg)
    if (command not in [c for c in cfg]): raise NoCommandError(command)
    run_action[command](cfg[command], msg)

def display_section_on_cmd(cfg):
    for index, action in enumerate(cfg, 0):
        if (index > 0): print(f"{index}. {action}") 
    return input("input >>> ")

def required_key_check(section, msg):
    missing_key = set(required_key[section.name]) - set(section)
    if (missing_key != set()): raise MissingRequiredKeyError(missing_key)

def run_test(section, msg):
    required_key_check(section, msg)
    msg.s_text = section["msg"]
    return None

def run_golden_limit(section, msg):
    required_key_check(section, msg)
    GoldenLimitSelect(section, msg)
    return None

required_key = {
    "TEST":         ("msg",),
    "GOLDEN_LIMIT": ("folder", "nums"),
}

run_action = {
    "TEST":         run_test,
    "GOLDEN_LIMIT": run_golden_limit,
}