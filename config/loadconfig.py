# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import json
import os


class CustomConfig():

    def read_file(self, file_path):
        with open(file_path, "r", encoding="utf-8") as rf:
            custom_config = json.load(rf)
            return custom_config

    def write_file(self, file_path, args_data):
        with open(file_path, "w", encoding="utf-8") as wf:
            write_data = json.dump(args_data, wf)
            return write_data


CustomConfig = CustomConfig()