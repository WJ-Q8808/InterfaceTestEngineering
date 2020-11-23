# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import json
import os

class ReadConfig():

    def __init__(self, file):
        self.file = file
        self.config_file_path = os.path.join(os.path.dirname(__file__), self.file)

    def read_file(self):
        with open(self.config_file_path,"r") as rf:
            custom_config = json.load(rf)

            return custom_config


# config = ReadConfig("config.json").read_file()