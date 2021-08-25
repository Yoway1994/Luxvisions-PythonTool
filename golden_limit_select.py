import re
import os
import numpy as np
import pandas as pd
from debug import *
from datetime import datetime
from openpyxl import load_workbook

p_f        = re.compile(r"00K_([\w]+)")
p_rlsc     = re.compile(r"RED Channel\s+{([.\s\d]+)}")
p_grlsc    = re.compile(r"GR Channel\s+{([.\s\d]+)}")
p_gblsc    = re.compile(r"GB Channel\s+{([.\s\d]+)}")
p_blsc     = re.compile(r"[\n\s]+B Channel\s+{([.\s\d]+)}")
p_rg_ratio = re.compile(r"r/gr\s+([.\d]+)")
p_bg_ratio = re.compile(r"b/gr\s+([.\d]+)")

path = "./golden_limit_select"
fname = {
    "txt": "AWB_LSC_GOLDEN_LIMIT_SAMPLE.txt",
    "xls": "AWB_LSC_GOLDEN_LIMIT_SAMPLE.xlsx",
    "smp": "SAMPLE_LIST.txt",}

def f_name(key):
    return os.path.join(path, fname[key])

class GoldenLimitSelect:
    def __init__(self, section):
        self.sec = section
        self.yes = ["Yes", "True", "yes", "true", "1"]

    def get_folder_path(self):
        l_f = []
        for dir in re.split(r"[,\s]+", self.sec["txt_folder"]):
            l_f.append(os.path.join(path, dir))
        return l_f

    def get_sample_nums(self):
        count = 0
        for dir in self.get_folder_path():
            count += len(os.listdir(dir))
        return count

    def select_sample(self):
        if self.sec["truncate"] in self.yes:self.truncate_log() 
        df_GLS = self.get_diff_dataframe()
        if self.sec["write_excel"] in self.yes:self.excel_save(df_GLS)
        self.gen_golden_limit_txt(df_GLS[["FuseID","LSC_diff","AWB_diff"]])

    def mark_sample(self):
        dir = self.get_folder_path()[0]
        with open(f_name("smp")) as smp:
            print(re.split(f"Folder: {dir}\n", smp.read()))
        return None

    @timer
    def get_diff_dataframe(self):
        num = self.get_sample_nums()
        fdr = self.get_folder_path()
        arry_4_chan  = np.zeros((4, num, 221), dtype = np.float64)
        arry_2_ratio = np.zeros((2, num), dtype = np.float64)
        index = 0
        id_list = []
        smp_list = open(f_name("smp"), "a+")
        for dir in fdr:
            smp_list.write(f"Folder: {dir}\n")
            for txt in os.listdir(dir):
                id_name = p_f.search(os.path.splitext(txt)[0]).group(1)
                smp_list.write(f"{id_name}\n")
                id_list.append(id_name)
                with open(os.path.join(dir, txt)) as txt_file:
                    context = txt_file.read()
                    arry_4_chan[0][index][:] = p_rlsc.search(context).group(1).split()
                    arry_4_chan[1][index][:] = p_grlsc.search(context).group(1).split()
                    arry_4_chan[2][index][:] = p_gblsc.search(context).group(1).split()
                    arry_4_chan[3][index][:] = p_blsc.search(context).group(1).split()
                    arry_2_ratio[0][index]   = p_rg_ratio.search(context).group(1)
                    arry_2_ratio[1][index]   = p_bg_ratio.search(context).group(1)
                index += 1
        smp_list.close()
        r_chan_diff    = np.sqrt(np.square((arry_4_chan[0]-arry_4_chan[0].mean(axis=0))).sum(axis=1)) 
        gr_chan_diff   = np.sqrt(np.square((arry_4_chan[1]-arry_4_chan[1].mean(axis=0))).sum(axis=1))
        gb_chan_diff   = np.sqrt(np.square((arry_4_chan[2]-arry_4_chan[2].mean(axis=0))).sum(axis=1))
        b_chan_diff    = np.sqrt(np.square((arry_4_chan[3]-arry_4_chan[3].mean(axis=0))).sum(axis=1))
        rg_ratio_diff  = abs(arry_2_ratio[0]-arry_2_ratio[0].mean())
        bg_ratio_diff  = abs(arry_2_ratio[1]-arry_2_ratio[1].mean())
        lsc_total_diff = r_chan_diff + gr_chan_diff + gb_chan_diff + b_chan_diff
        awb_total_diff = rg_ratio_diff + bg_ratio_diff
        dict_GLS = {
            "FuseID"         :id_list, 
            "LSC_diff"       :lsc_total_diff, 
            "AWB_diff"       :awb_total_diff,
            "R_Channel_diff" :r_chan_diff,
            "Gr_Channel_diff":gr_chan_diff,
            "Gb_Channel_diff":gb_chan_diff,
            "B_Channel_diff" :b_chan_diff,
            "RG_Ratio_diff"  :rg_ratio_diff,
            "BG_Ration_diff" :bg_ratio_diff,}
        def add_detail(dict, channel, pre):
            for i, data in enumerate(channel.T, 1):
                c_name = f"{pre}{i}"
                dict[c_name] = data
        add_detail(dict_GLS, arry_4_chan[0], "R_")
        add_detail(dict_GLS, arry_4_chan[1], "Gr_")
        add_detail(dict_GLS, arry_4_chan[2], "Gb_")
        add_detail(dict_GLS, arry_4_chan[3], "B_")
        df_GLS = pd.DataFrame(dict_GLS)
        return df_GLS

    def gen_golden_limit_txt(self, df):
        num = int(self.sec["pick_nums"])
        folders = self.sec["txt_folder"]
        df_awb = df[["FuseID","AWB_diff"]].sort_values("AWB_diff")
        df_lsc = df[["FuseID","LSC_diff"]].sort_values("LSC_diff")
        log = [""]
        log[0] = f"TimeStamp: {datetime.now()}, from folder: {folders}\n\n"
        def line_data(lg, df, title):
            lg[0] += f"\n{title}\n"
            for i, line in enumerate(df, 1):
                id, data = line
                lg[0] += f"{i:02d}, {id}, {data}\n"
        with open(f_name("txt"), "a+") as file:
            line_data(log, df_awb.head(num).values , "AWB Golden Sample")
            line_data(log, df_awb.tail(num)[::-1].values, "AWB Limit Sample")
            line_data(log, df_lsc.head(num).values,"LSC Golden Sample")
            line_data(log, df_lsc.tail(num)[::-1].values, "LSC Limit Sample")
            file.write(log[0])

    def truncate_log(self):
        with open(f_name("txt"), "w+"):
            pass
        with open(f_name("smp"), "w+"):
            pass
    
    @timer
    def excel_save(self, df):
        if not os.path.isfile(f_name("xls")):
            pd.DataFrame().to_excel(f_name("xls"))
        book = load_workbook(f_name("xls"))
        writer = pd.ExcelWriter(f_name("xls"), engine="openpyxl")
        writer.book = book
        writer.sheets = dict((ws.title, ws) for ws in book.worksheets)
        df.to_excel(writer, self.sec["sheet_name"])
        writer.save()