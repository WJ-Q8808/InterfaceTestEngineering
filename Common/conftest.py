# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
import pytest
import requests

from Common.test_login import SetupApi

@pytest.fixture(scope="module")
def login_fixture():
    """
    前置条件，先登陆
    :return:
    """
    SessionMechanism = requests.session()
    ones_api = SetupApi("wujian@ones.ai","wujian8808","Core")
    ones_api.
    return SessionMechanism
