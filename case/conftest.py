# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import pytest
import requests
from config.loadconfig import ReadConfig
from common.test_login import SetupApi

config = ReadConfig("config.json").read_file()

@pytest.fixture(scope="module")
def login_fix():
    """
    前置条件，先登陆
    """
    SessionMechanism = requests.session()
    SetupApi.setup_login(SessionMechanism,config["EMAIL"],config["PASSWORD"],config["PRODUCT"])
    return SessionMechanism


