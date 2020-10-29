# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import json
import os

class ReadConfig():

    def __init__(self):
        pass

    def read_file(self,file):
        config_file_path = os.path.join(os.path.dirname(__file__), file)
        with open(config_file_path,"r") as rf:
            custom_config = json.load(rf)
            return custom_config


config = ReadConfig().read_file("config.json")
# print(config["EMAIL"])