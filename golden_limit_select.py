import re
import os
import numpy as np
from typing import List, Set

p_f        = re.compile(r"00K_([\w]+)")
p_rlsc     = re.compile(r"RED Channel\s+{([.\s\d]+)}")
p_grlsc    = re.compile(r"GR Channel\s+{([.\s\d]+)}")
p_gblsc    = re.compile(r"GB Channel\s+{([.\s\d]+)}")
p_blsc     = re.compile(r"[\n\s]+B Channel\s+{([.\s\d]+)}")
p_rg_ratio = re.compile(r"r/gr\s+([.\d]+)")
p_bg_ratio = re.compile(r"b/gr\s+([.\d]+)")

class GoldenLimitSelect:
    def __init__(self, section):
        self.section = section
        self.txt_folders = self.get_folder_path()
        self.nums = self.get_nums()
        self.data_list = self.get_data()
    
    def get_folder_path(self) -> List:
        l_f = []
        for dir in self.section["txt_folder"].split(", "):
            l_f.append(os.path.join(r"./golden_limit_select/", dir))
        return l_f

    def get_nums(self):
        count = 0
        for dir in self.txt_folders:
            count += len(os.listdir(dir))
        return count

    def get_data(self) -> List:
        tmp_list = []
        for dir in self.txt_folders:
            for txt in os.listdir(dir):
                abs_txt_name = os.path.join(dir, txt)
                with open(abs_txt_name) as file:
                    context = file.read()
                    tmp_dict = {
                        "fuse_id" : p_f.search(os.path.splitext(txt)[0]).group(1),
                        "r_lsc"   : np.array(p_rlsc.search(context).group(1).split(), dtype = np.float64),
                        "gr_lsc"  : np.array(p_grlsc.search(context).group(1).split(), dtype = np.float64),
                        "gb_lsc"  : np.array(p_gblsc.search(context).group(1).split(), dtype = np.float64),
                        "b_lsc"   : np.array(p_blsc.search(context).group(1).split(), dtype = np.float64),
                        "rg_ratio": p_rg_ratio.search(context).group(1),
                        "bg_ratio": p_bg_ratio.search(context).group(1),}
                    tmp_list.append(tmp_dict)
        return tmp_list

    def calculate_diff(self):
        