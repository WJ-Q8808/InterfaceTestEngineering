# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------

import json_tools
from pprint import pprint
from config.loadconfig import CustomConfig
from regression.loadyaml import ReadYaml
from deepdiff import grep



def json_tool(test1,test2):
    result = json_tools.diff(test1, test2)
    print(result)


def find_json(data,find_str):
    reuslt = data | grep(find_str, use_regexp=True)
    print(reuslt)
    return reuslt


if __name__ == '__main__':
    test_data = ReadYaml.read_yaml("../demo/demo01.yaml")
    print(test_data)

    # json = test_data["issueTypeLayouts"]["json"][0]
    # pprint(test_data)
    # # pprint(test1)
    # find_str = "uuid_equal"
    # value_number = 3
    # matched_paths = find_json(test_data, find_str)["matched_paths"]
    # root = matched_paths[0]
    # path_value = "".join(root.replace("root", "").replace("[","").replace("]","")).split("'")
    # path_value = root.replace("root", "").replace("[","").replace("]","").split("'")
    # print(path_value)
    # update_json = ""
    # print(path_value)
    # for i in path_value:
    #     if i:
    #         if i.isdigit():
    #             t = int(i)
    #             update_json = test_data[t]
    #         else:
    #             update_json = test_data[i]
    #     test_data = update_json
    # update_json = value_number
    # print(json)


