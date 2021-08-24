import re
import os
import numpy as np
import pandas as pd

p_f        = re.compile(r"00K_([\w]+)")
p_rlsc     = re.compile(r"RED Channel\s+{([.\s\d]+)}")
p_grlsc    = re.compile(r"GR Channel\s+{([.\s\d]+)}")
p_gblsc    = re.compile(r"GB Channel\s+{([.\s\d]+)}")
p_blsc     = re.compile(r"[\n\s]+B Channel\s+{([.\s\d]+)}")
p_rg_ratio = re.compile(r"r/gr\s+([.\d]+)")
p_bg_ratio = re.compile(r"b/gr\s+([.\d]+)")

class GoldenLimitSelect:
    def __init__(self, section):
        self.sec = section
    
    def get_folder_path(self):
        l_f = []
        for dir in re.split(r"[,\s]+", self.sec["txt_folder"]):
            l_f.append(os.path.join(r"./golden_limit_select/", dir))
        return l_f

    def get_sample_nums(self):
        count = 0
        for dir in self.get_folder_path():
            count += len(os.listdir(dir))
        return count

    def get_diff_dataframe(self):
        id_list = []
        num = self.get_sample_nums()
        fdr = self.get_folder_path()
        arry_4_chan  = np.zeros((4, num, 221), dtype = np.float64)
        arry_2_ratio = np.zeros((2, num), dtype = np.float64)
        index = 0
        for dir in fdr:
            for txt in os.listdir(dir):
                id_list.append(p_f.search(os.path.splitext(txt)[0]).group(1))
                with open(os.path.join(dir, txt)) as txt_file:
                    context = txt_file.read()
                    arry_4_chan[0][index][:] = p_rlsc.search(context).group(1).split()
                    arry_4_chan[1][index][:] = p_grlsc.search(context).group(1).split()
                    arry_4_chan[2][index][:] = p_gblsc.search(context).group(1).split()
                    arry_4_chan[3][index][:] = p_blsc.search(context).group(1).split()
                    arry_2_ratio[0][index]   = p_rg_ratio.search(context).group(1)
                    arry_2_ratio[1][index]   = p_bg_ratio.search(context).group(1)
                index += 1
        r_chan_diff    = np.sqrt(np.square((arry_4_chan[0]-arry_4_chan[0].mean(axis=0))).sum(axis=1)) 
        gr_chan_diff   = np.sqrt(np.square((arry_4_chan[1]-arry_4_chan[1].mean(axis=0))).sum(axis=1))
        gb_chan_diff   = np.sqrt(np.square((arry_4_chan[2]-arry_4_chan[2].mean(axis=0))).sum(axis=1))
        b_chan_diff    = np.sqrt(np.square((arry_4_chan[3]-arry_4_chan[3].mean(axis=0))).sum(axis=1))
        rg_ratio_diff  = abs(arry_2_ratio[0]-arry_2_ratio[0].mean())
        bg_ratio_diff  = abs(arry_2_ratio[1]-arry_2_ratio[1].mean())
        lsc_total_diff = r_chan_diff + gr_chan_diff + gb_chan_diff + b_chan_diff
        awb_total_diff = rg_ratio_diff + bg_ratio_diff
        df_GLS = pd.DataFrame({"FuseID":id_list, "LSC_diff":lsc_total_diff, "AWB_diff":awb_total_diff})
        return df_GLS

    def gen_golden_limit_txt(self, df):
        num = int(self.sec["pick_nums"])
        with open("./golden_limit_select/AWB_LSC_GOLDEN_LIMIT.txt", "w+") as file:
            log = "from folder: {}".format(self.sec["txt_folder"])
            file.write(log)
            pass
        pass

    def store_detail_data():
        pass