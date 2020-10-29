# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import pytest
import requests
from Config.loadconfig import config
from Common.test_login import SetupApi


@pytest.fixture(scope="module")
def login_fix():
    """
    前置条件，先登陆
    """
    SessionMechanism = requests.session()
    SetupApi.setup_login(SessionMechanism,config["EMAIL"],config["PASSWORD"],config["PRODUCT"])
    return SessionMechanism


