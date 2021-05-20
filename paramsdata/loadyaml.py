# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import yaml
import os
from pprint import pprint

class ReadYaml:

    def __init__(self):
        pass

    def readyaml_file(self,file):
        all_data = []
        self.params_file_path = os.path.join(os.path.dirname(__file__), file)
        with open(self.params_file_path,"r",encoding='utf-8') as rf:
            yamls_data = yaml.load_all(rf.read(), Loader=yaml.Loader)
            for yaml_data in yamls_data:
                all_data.append(yaml_data)
        return all_data


ReadYaml = ReadYaml()

from pprint import pprint
if __name__ == '__main__':
    body_yaml = ReadYaml.readyaml_file("arg.yaml")
    pprint(body_yaml)







