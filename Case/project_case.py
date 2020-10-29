# -*- coding: utf-8 -*-# 
#-------------------------------------------------------------------------------
from Common.test_login import SetupApi
from Case.conftest import login_fix


def test_get_projects(login_fix):
    """
    获取所有项目
    :return:
    """
    SessionMechanism = login_fix
    url_projects = SetupApi.base_url("/projects/my_project")
    response = SessionMechanism.get(url=url_projects)
    status=response.status_code
    assert status == 200

def test_get_product(login_fix):
    SessionMechanism = login_fix
    query = '''{products(filter: $filter, orderBy: $orderBy)
                    { name
                      uuid
                      assign{
                          uuid
                          name
                        }}}'''
    query = {"query": query, "variables": {"orderBy": {"createTime": "DESC"}}}
    graphql_products_url = SetupApi.base_url("/items/graphql")
    response = SessionMechanism.post(url=graphql_products_url, json=query)
    status=response.status_code
    assert status == 200