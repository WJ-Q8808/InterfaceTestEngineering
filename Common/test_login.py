import requests
from pprint import pprint

requests_sessions = requests.session()


class SetupApi:

    def __init__(self,user_email,password,team_name=None):
        login_url = self.base_url("/auth/login",off_team_url="login")
        self.SessionMechanism = requests.session()

        data = {
            "email": user_email,  # wujian@ones.ai
            "password": password  # wujian8808
        }
        response = self.SessionMechanism.post(url=login_url, json=data)
        response_json = response.json()
        # response_status = response.status_code
        self.token = response_json["user"]["token"]
        self.user_uuid = response_json["user"]["uuid"]
        headers_message = {
            'referer': 'https://dev.myones.net/project/master/',
            'Content-Type': 'application/json',
            "Ones-Auth-Token": self.token,
            "Ones-User-Id": self.user_uuid
        }

        self.SessionMechanism.headers.update(headers_message)
        if team_name == None:
            self.team_uuid = response_json["teams"][0]["uuid"]
        else:
            self.team_uuid = "".join([j["uuid"] for j in response_json["teams"] if j["name"] == team_name])

    def setup_login(self,email,password,SessionMechanism,team_name=None):
        login_url = self.base_url("/auth/login", off_team_url="login")
        data = {
            "email": email,  # wujian@ones.ai
            "password": password  # wujian8808
        }
        response = SessionMechanism.post(url=login_url, json=data)
        response_json = response.json()
        # response_status = response.status_code
        token = response_json["user"]["token"]
        user_uuid = response_json["user"]["uuid"]
        headers_message = {
            'referer': 'https://dev.myones.net/project/master/',
            'Content-Type': 'application/json',
            "Ones-Auth-Token": token,
            "Ones-User-Id": user_uuid
        }

        SessionMechanism.headers.update(headers_message)
        team_uuid = ""
        if team_name == None:
            self.team_uuid = response_json["teams"][0]["uuid"]
        else:
            self.team_uuid = "".join([j["uuid"] for j in response_json["teams"] if j["name"] == team_name])

        return team_uuid,SessionMechanism


    def base_url(self,work_url="",product="project",off_team_url=None):
        #封装URL
        public_url = "https://devapi.myones.net/{}/master".format(product)
        if off_team_url != None:
            public_url += "/{}".format(work_url)
            return public_url
        else:
            public_url += "/team/{}{}".format(self.team_uuid,work_url)
            return public_url


    def get_projects(self):
        """
        获取所有项目
        :return:
        """
        url_projects = self.base_url("/projects/my_project")
        response = self.SessionMechanism.get(url=url_projects).json()
        print(response)
        return response

    def get_graphql_products(self,bady=""):
        '''
        获取所有
        :param bady:
        :return:
        '''
        query = '''{products(filter: $filter, orderBy: $orderBy)
                { name
                  uuid
                  assign{
                      uuid
                      name
                    }}}'''
        query = {"query":query,"variables":{"orderBy":{"createTime":"DESC"}}}
        graphql_products_url = self.base_url("/items/graphql")
        response_json = self.SessionMechanism.post(url=graphql_products_url,json=query).json()
        print(response_json)

        return response_json

# SetupApi = SetupApi("wujian@ones.ai","wujian8808","Core")

if __name__ == '__main__':
    ones_api = SetupApi("wujian@ones.ai","wujian8808","Core")
    ones_api.get_graphql_products()
    ones_api.get_projects()


