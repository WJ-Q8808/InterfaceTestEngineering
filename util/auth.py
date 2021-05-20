# -*- coding: utf-8 -*-#
# -------------------------------------------------------------------------------
# Name:         auth
# Description:
# Author:       wujian
# Date:         2021/5/13
# -------------------------------------------------------------------------------
import os, re
import requests
import threading
from pprint import pprint
from config.loadconfig import CustomConfig
from paramsdata.loadyaml import ReadYaml

from util.logger import Logger
logger = Logger(logger=(__name__)).getlog()



class Base:

    def __init__(self):
        self.Session = requests.session()
        self.config_path = os.path.join(os.path.dirname(__file__), '../config/config.json')
        self.config = CustomConfig.read_file(self.config_path)

    def base_session(self, method, url, json, params, headers):
        """
        API   基础session对象方法
        :method: 请求类型 "Post、Get"
        :url: url地址
        :json: 传入对post参数
        :params: 传入对params参数
        :headers : 传入对头部信息
        :return: 以json新式返回具体response
        """
        response = requests.request(str.upper(method), url, json=json, params=params, headers=headers)
        logger.info("Url:{}".format(url))
        logger.info("body Json: {} ".format(json))
        logger.info("body params: {} ".format(params))
        logger.info("status_code : {} ".format(response.status_code))
        if int(response.status_code) != 200 or "erro" in response.text:
            logger.info("Response:{}".format(response.json()))
        try:
            result = response.json()
        except ValueError:
            logger.info("result is not a valid json format!!!")
        else:
            return result

        return response

    def ones_request(self, method, authed_url, config_referer, main_product, minor_product, json=None, params=None, headers={}):
        '''
        ONES_API  基础信息拼装
        '''
        base_url = authed_url.format(main_product=main_product,minor_product=minor_product)
        referer = config_referer.format(main_product)
        headers.update({
            "content-type": "application/json",
            "referer": referer
        })

        return self.base_session(method, base_url, json=json, params=params, headers=headers)

    def ones_authed_request(self, method, url, path, config_referer,  main_product, minor_product,
                            json=None, params=None, team_uuid=None, token=None, user_uuid=None):
        if team_uuid:
            authed_url = url+path.format(team_uuid)
        else:
            authed_url = url+path
        headers= {
            "Ones-auth-Token" : token,
            "Ones-User-Id" : user_uuid,
            "Connection":  "close"
        }
        return self.ones_request(method, authed_url, config_referer,  main_product, minor_product, json, params, headers=headers)

    def analyse_data(self, data_api):
        method = data_api["method"]
        path = data_api["path"]
        product = data_api["product"]
        main_product = product["main_product"]
        minor_product = product["minor_product"]
        json = data_api["json"]
        params = data_api["params"]
        return method, path, main_product, minor_product, json, params


class AuthLogin:

    def __init__(self):
        self.Base = Base()
        self.cached_date = {}

    def auth_login(self, config_url, config_referer, email, password):
        if not email or not password:
            raise RuntimeError('User or password is empty!')
        res_data = data["api_type"][0]["login"]
        method, path, main_product, minor_product, json, params = self.Base.analyse_data(res_data)
        json = {'email': email, 'password': password}
        response = self.Base.ones_authed_request(method, config_url, path, config_referer, main_product, minor_product, json=json)
        self.cached_date['token'] = response['user']['token']
        self.cached_date['user_uuid'] = response['user']['uuid']
        self.cached_date["config_url"] = config_url
        return response

    def set_team_uuid(self, team_uuid):
        self.cached_date['team_uuid'] = team_uuid
        return team_uuid

    def login(self, config_url, config_referer):
        email = self.Base.config["EMAIL"]
        password = self.Base.config["PASSWORD"]
        response = self.auth_login(config_url, config_referer, email, password)
        self.set_team_uuid(response["teams"][0]["uuid"])
        return response


class TeamApi:

    def __init__(self):
        self.Auth = AuthLogin()

    def base_env(self, cached, method, config_url, path, config_referer, is_team, main_product, minor_product, json=None, params=None):
        if is_team:
            return self.Auth.Base.ones_authed_request(method, config_url, path, config_referer, main_product, minor_product, json=json, params=params,
                                                      team_uuid=cached["team_uuid"], token=cached["token"], user_uuid=cached["user_uuid"])
        else:
            return self.Auth.Base.ones_authed_request(method, config_url, path, config_referer, main_product, minor_product, json=json, params=params,
                                                      token=cached["token"], user_uuid=cached["user_uuid"])

    def is_methed(self, func_env, cached, method, config_url, path, config_referer, main_product, minor_product, is_team, json, params):
        if method == "post":
            return func_env(cached, method, config_url, path, config_referer, is_team, main_product, minor_product, json=json)
        elif method == "get":
            return func_env(cached, method, config_url, path, config_referer, is_team, main_product, minor_product, params=params)

    def is_team(self, config_url, config_referer, cached, data_api):
        method, path, main_product, minor_product, json, params = self.Auth.Base.analyse_data(data_api)
        if "team" in path:
            is_team = True
        else:
            is_team = False
        return self.is_methed(self.base_env, cached, method, config_url, path, config_referer, main_product, minor_product, is_team, json, params)


    def get_data(self, yaml_json):
            pass


class Sprint_Evn():

    def __init__(self):
        self.TeamApi = TeamApi()
        self.sprint_url = self.TeamApi.Auth.Base.config["SPRINT_API_URL"]
        self.sprint_referer = self.TeamApi.Auth.Base.config["SPRINT_REFERER"]
        self.sprint_cached = {}
        if not self.sprint_cached:
            login_sprint = threading.Thread(target = self.TeamApi.Auth.login, args=(self.sprint_url, self.sprint_referer))
            login_sprint.start()
            login_sprint.join()
            self.sprint_cached = self.TeamApi.Auth.cached_date

    def sprint_api(self, api_data):
        config_url = self.sprint_url
        config_referer = self.sprint_referer
        cached = self.sprint_cached
        return self.TeamApi.is_team(config_url, config_referer, cached, api_data)



class Dev_Evn():
    def __init__(self):
        self.TeamApi = TeamApi()
        self.dev_url = self.TeamApi.Auth.Base.config["DEV_API_URL"]
        self.dev_referer = self.TeamApi.Auth.Base.config["DEV_REFERER"]
        self.dev_cached = {}
        if not self.dev_cached:
            login_dev = threading.Thread(target = self.TeamApi.Auth.login, args=(self.dev_url, self.dev_referer))
            login_dev.start()
            login_dev.join()
            self.dev_cached = self.TeamApi.Auth.cached_date

    def dev_api(self, api_data):
        config_url = self.dev_url
        config_referer = self.dev_referer
        cached = self.dev_cached
        return self.TeamApi.is_team(config_url, config_referer, cached, api_data)


class TestCase():
    pass





if __name__ == '__main__':
    data = ReadYaml.readyaml_file("body.yaml")[0]
    res_data = data["api_type"][1]["token_info"]

    Sprint_Evn = Sprint_Evn()
    Dev_Evn = Dev_Evn()

    Sprint_Evn.sprint_api(res_data)
    Dev_Evn.dev_api(res_data)

    # ths = []
    # th_sprint = threading.Thread(target = TeamApi.sprint_api, args=(data))
    # th_sprint.start()
    # ths.append(th_sprint)
    # th_dev = threading.Thread(target = TeamApi.dev_api, args=(data))
    # th_dev.start()
    # ths.append(th_dev)
    # for th in ths:
    #     th.join()
