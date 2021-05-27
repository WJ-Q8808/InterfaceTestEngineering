from regression.loadyaml import ReadYaml
# from util.auth import sprint, dev

from pprint import pprint


class ResoluData:

    def __init__(self):
        self.opt_file = ReadYaml

    def read_single_file(self, file_path):
        base_data = self.opt_file.read_yaml(file_path)
        return base_data

    def find_api_type(self, path_list):
        # for file_path in path_list:
        base_data = self.read_single_file("/project/sprint_field.yaml")
        api_type = base_data["api_type"]
        # pprint(api_type)
        for single_api in api_type:
            api_name = single_api["name"]
            api_method = single_api["method"]
            api_path = single_api["method"]
            main_product = single_api["url_product"]["main_product"]
            minor_product = single_api["url_product"]["minor_product"]
            api_info = {}
            pprint(single_api)
            if single_api["params"]:
                pass
            if api_method == "get":
                if single_api["params"]:
                    pass

            if single_api["url_params"]:
                for url_params in single_api["url_params"]:
                    if url_params["is_params"]:
                    # pprint(url_params["value_path"])
                        for value_path in url_params["value_path"]:
                            api_name = value_path["api_name"]
                            field_path = value_path["field_path"]
                            field_number = value_path["field_number"]
                            for field in field_number:
                                find_response_path = field["find_response_path"]
                                url_name = field["field_name"]
                                print(api_name, field_path, field_number, find_response_path, url_name)
            if api_method == "post":
                if single_api["json_params"]:
                    for json_params in single_api["json_params"]:
                        if json_params["is_params"]:
                            json = json_params["json"]
                            pprint(json)
                            for value_path in json_params["value_path"]:
                                api_name = value_path["api_name"]
                                field_path = value_path["field_path"]
                                field_number = value_path["field_number"]
                                for field in field_number:
                                    find_response_path = field["find_response_path"]
                                    url_name = field["field_name"]
                                    print(api_name, field_path, find_response_path, url_name)



        return api_type

    def join_path(self, path, **kwargs):
        new_path = path.format(**kwargs)
        return new_path



    def reaquest_data(self, request_data):
        method = request_data["method"]
        path = request_data["path"]
        product = request_data["product"]
        main_product = product["main_product"]
        minor_product = product["minor_product"]
        json = request_data["json"]
        params = request_data["params"]

        return method, path, main_product, minor_product, json, params


opt = ResoluData()
if __name__ == '__main__':
    path_list = 1
    opt.find_api_type(path_list)