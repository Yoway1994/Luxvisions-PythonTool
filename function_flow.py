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
    gm = GoldenLimitSelect(section)
    print(gm.nums)
    #for i, d in enumerate(gm.data_list):
    #    print(i, d["r_lsc"])

run_action = {
    "TEST":         run_test,
    "GOLDEN_LIMIT": run_golden_limit,}