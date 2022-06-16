import os
from debug import *
import pandas as pd
from configparser import ConfigParser as cfg

intel_path = "./intel_rgb_ratio"

Gr_3000K = 518
Gr_5000K = 520
R_3000K = 522
R_5000K = 524
B_3000K = 526
B_5000K = 528
Gb_3000K = 530
Gb_5000K = 532

class IntelRgbRatio:
	def __init__(self, section):
		self.sec = section

	def reverse_little_endian(self, first, last):
		combine = last+first
		return int(combine, 16)

	def get_bytelist_nvm(self, file, byte_list):
		with open(os.path.join(intel_path, file), "rb") as bytes:
			for index, bit in enumerate(bytes.read()):
				hex = format(bit, '02x')
				byte_list.append(hex)

	def get_bytelist_ini(self, file, byte_list):
		cali_info = cfg()
		cali_info.read(os.path.join(intel_path, file))
		for lsc in cali_info["LSC"].items():
			_, value = lsc
			if (len(value) < 2): value = '0' + value
			byte_list.append(value)

	@timer
	def cal_rgb_ratio(self):
		module = []
		RGr3000K = []
		BGb3000K = []
		RGr5000K = []
		BGb5000K = []
		for file in os.listdir(intel_path):
			filename, file_extension = os.path.splitext(file)
			byte_list = []
			if (file_extension == ".nvm"):
				self.get_bytelist_nvm(file, byte_list)
			elif (file_extension == ".ini"):
				self.get_bytelist_ini(file, byte_list)
			else:
				raise Exception(f"unexpected extension: {file}")
				
			Gr_3000K_value = self.reverse_little_endian(byte_list[Gr_3000K], byte_list[Gr_3000K+1])
			Gr_5000K_value = self.reverse_little_endian(byte_list[Gr_5000K], byte_list[Gr_5000K+1])
			R_3000K_value = self.reverse_little_endian(byte_list[R_3000K], byte_list[R_3000K+1])
			R_5000K_value = self.reverse_little_endian(byte_list[R_5000K], byte_list[R_5000K+1])
			B_3000K_value = self.reverse_little_endian(byte_list[B_3000K], byte_list[B_3000K+1])
			B_5000K_value = self.reverse_little_endian(byte_list[B_5000K], byte_list[B_5000K+1])
			Gb_3000K_value = self.reverse_little_endian(byte_list[Gb_3000K], byte_list[Gb_3000K+1])
			Gb_5000K_value = self.reverse_little_endian(byte_list[Gb_5000K], byte_list[Gb_5000K+1])

			module.append(filename)
			RGr3000K.append(R_3000K_value/Gr_3000K_value)
			BGb3000K.append(B_3000K_value/Gb_3000K_value)
			RGr5000K.append(R_5000K_value/Gr_5000K_value)
			BGb5000K.append(B_5000K_value/Gb_5000K_value)
			#
		dic_ratio = {
			"module": module,
			"R/Gr_3000K": RGr3000K,
			"B/Gb_3000K": BGb3000K,
			"R/Gr_5000K": RGr5000K,
			"B/Gb_5000K": BGb5000K
			}
		df_rgb_ratio = pd.DataFrame(dic_ratio)
		df_rgb_ratio.to_csv("intel_rgb_ratio.csv")

		pd.options.display.max_columns = None
		pd.options.display.max_rows = None
		print(df_rgb_ratio)
