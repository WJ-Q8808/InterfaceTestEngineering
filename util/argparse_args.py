# -*- coding: UTF-8 -*-
import argparse
import json
import os
import re
from logger import Logger

logger = Logger(logger=(__name__)).getlog()



"""
根据回归测试目标：输入对应参数
模式：命令行参数 两个url地址、账号、密码、用例路径，来进行不同环境对api数据对比
命令行模式如下：
1、
python main.py --url_sprint 47.119.135.84 --url_dev 119.23.214.42 -a marsdev@ones.ai -w Test1234 -d {data_path}

"""


class ArgumentConfig:

    def __init__(self):
        self.file_path = os.path.join(os.path.dirname(__file__), '../config.json')

    def base_add_argument(self):
        '''
        默认参数：账号、密码、数量及其它信息
        Args:
            kwargs:传值给ArgumentParser显示prog和description，以及其它值
        Return:可以继续添加参数
            parse:添加参数
        '''
        # 实例化对象
        parser = argparse.ArgumentParser(description="Please enter a required parameter as the script running condition")
        # 添加定义对象属性；
        parser.add_argument("-s", "--sprint_url", help="Fill in the URL of the insert data environment", required=True)
        parser.add_argument("-v", "--dev_url", help="Fill in the URL of the insert data environment", required=True)
        parser.add_argument("-t", "--create_type", help="Insert data type", required=True)
        parser.add_argument("-n", "--number", help="Number to insert", type=int, required=True)
        parser.add_argument("-a", "--email", help="Fill in the login account number", required=False)
        parser.add_argument("-w", "--password", help="Fill in the login password", required=False)
        parser.add_argument("-p", "--project_uuid", help="Copy template UUID", required=False)
        parser.add_argument("-m", "--thread_number", help="How many thread groups do you need to execute", type=int, required=False)
        parser.add_argument("-i", "--switch", help="Specifies the mode of operation", type=str, required=False)
        parser.add_argument("-c", "--select", help="Total number of queries", type=str, required=False)
        return parser

    def base_parse_args(self, parse):
        '''
        默认赋值：账号、密码、配置文件到cached_data
        Args:
            cached_data:缓存参数
        Return:可以继续添加参数
            args:参数的值传递到外部

        url:插入数据的url
        create_type：插入数据的类型
        number：需要插入多少条数据（准确度：100以内）
        email：账号
        password：密码
        project_uuid：指定的project_uuid
        thread_number: 线程数
        switch：是否指定成员执行
        '''
        args_data = {}
        args = parse.parse_args()
        if args.sprint_url:
            args_data["SPRINT_API_URL"] = args.sprint_url
        if args.dev_url:
            args_data["DEV_API_URL"] = args.dev_url
        if args.create_type:
            args_data["CREATE_TYPE"] = args.create_type
        if args.number:
            args_data["NUMBER"] = args.number
        args_data["EMAIL"] = args.email
        if not args.password:
            args_data["PASSWORD"] = "Test1234"
        else:
            args_data["PASSWORD"] = args.password
        args_data["SWITCH"] = args.switch
        args_data["SELECT"] = args.select
        args_data["THREAD_NUMBER"] = args.thread_number
        args_data["PROJECT_UUID"] = args.project_uuid

        return args_data

    def get_url(slef, input_env):
        """
        输入原始url，转换成api的url
        :param input_url:
        :return:
        """
        new_str = str(input_env).upper()
        tail_url = "/{main_product}/api/{minor_product}"
        try:
            if "SAAS" in new_str:
                new_head = "https://ones.ai"
                return new_head+tail_url, new_head+"/{product}/"
            elif "MASTER" in new_str:
                new_head = "https://dev.myones.net"+"/{main_product}/master"
                return new_head+"/api/{minor_product}", new_head
            elif len(input_env) == 5 and ("master" not in new_str):
                new_head = "https://dev.myones.net"+"/{main_product}"+"/{}".format(input_env)
                return new_head+"/api/{minor_product}", new_head
            elif input_env.replace(".", "").isdigit():
                new_head = "http://{}".format(input_env)
                return new_head+tail_url, new_head+"/{product}/"
            else:
                logger.info("URL input error")
        except Exception as e:
            logger.info(e)

    def write_config_json(self, args_data):
        if args_data["SPRINT_API_URL"]:
            execute_url, referer_url = self.get_url(args_data["SPRINT_API_URL"])
            args_data["SPRINT_API_URL"] = execute_url
            args_data["SPRINT_REFERER"] = referer_url
        if args_data["DEV_API_URL"]:
            execute_url, referer_url = self.get_url(args_data["DEV_API_URL"])
            args_data["DEV_API_URL"] = execute_url
            args_data["DEV_API_URL"] = referer_url
        if not args_data["EMAIL"] or not args_data["PASSWORD"]:
            args_data["EMAIL"] = "marsdev@ones.ai"
            args_data["PASSWORD"] = "Test1234"
        with open(self.file_path, 'w', encoding='utf-8') as fp:
            fp.seek(0)
            fp.truncate()
            json.dump(args_data, fp)

        with open(self.file_path, "r", encoding="utf-8") as f:
            config = json.load(f)
            return config

    def clean_config_file(self):
        with open(self.file_path, 'a', encoding='utf-8') as fp:
            fp.seek(0)
            fp.truncate()


argument = ArgumentConfig()
