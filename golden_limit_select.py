import re
import os
import pandas as pd

class GoldenLimitSelect:
    def __init__(self, section, msg):
        self.folder = section["folder"]
        self.nums = section["nums"]