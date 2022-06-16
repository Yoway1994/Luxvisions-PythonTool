from golden_limit_select import GoldenLimitSelect
from intel_rgb_ratio import IntelRgbRatio

### parser command
def execute_function_flow(cfg):
    command = display_section_on_cmd(cfg)
    run_action[command](cfg[command])

def display_section_on_cmd(cfg):
    for index, action in enumerate(cfg, 0):
        if (index > 0): print(f"{index}. {action}") 
    return input("input >>> ")

### function flow
def run_test(section):
    print(section["msg"])

def run_golden_limit(section):
    gls = GoldenLimitSelect(section)
    gls.select_sample()

def run_golden_limit_marker(section):
    gls = GoldenLimitSelect(section) 
    gls.mark_sample()
	
def run_intel_rgb_ratio(section):
	itel = IntelRgbRatio(section)
	itel.cal_rgb_ratio()

run_action = {
    "TEST" : run_test,
    "GOLDEN_LIMIT" : run_golden_limit,
    "MARKER" : run_golden_limit_marker,
	"INTEL_RGB_RATIO" : run_intel_rgb_ratio
    }