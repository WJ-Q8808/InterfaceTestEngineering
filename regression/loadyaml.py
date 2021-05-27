# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
import yaml
import os
from pprint import pprint

class ReadYaml:

    def __init__(self):
        self.root_path = os.path.dirname(os.path.abspath(__file__))

    def read_yaml(self, file):
        base_path = "../api_core/{}".format(file)
        file_path = os.path.join(self.root_path, base_path)
        with open(file_path, "r",encoding='utf-8') as rf:
            yaml_data = yaml.load(rf.read(), Loader=yaml.Loader)
        return yaml_data

    def read_all_yaml(self, file):
        all_data = []
        base_path = "../api_core/{}".format(file)
        file_path = os.path.join(self.root_path, base_path)
        with open(file_path, "r",encoding='utf-8') as rf:
            yaml_data = yaml.load_all(rf.read(), Loader=yaml.Loader)
            for _data in yaml_data:
                all_data.append(_data)
        return all_data


ReadYaml = ReadYaml()


# root_path = os.path.dirname(os.path.abspath(__file__))
# file_path = os.path.join(root_path, '../api_core')
# print(file_path)
