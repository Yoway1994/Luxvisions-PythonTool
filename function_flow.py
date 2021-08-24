import numpy as np
import pandas as pd
from golden_limit_select import GoldenLimitSelect


def execute_function_flow(cfg):
    command = display_section_on_cmd(cfg)
    run_action[command](cfg[command])

def display_section_on_cmd(cfg):
    for index, action in enumerate(cfg, 0):
        if (index > 0): print(f"{index}. {action}") 
    return input("input >>> ")

def run_test(section):
    print(section["msg"])

def run_golden_limit(section):
    gls = GoldenLimitSelect(section)
    df_res = gls.get_diff_dataframe()
    gls.gen_golden_limit_txt(df_res)

    return None

run_action = {
    "TEST":         run_test,
    "GOLDEN_LIMIT": run_golden_limit,}