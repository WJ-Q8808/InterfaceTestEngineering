import requests
from Config.loadconfig import config
requests_sessions = requests.session()


class SetupApi:

    def __init__(self):
        pass

    def base_url(self,work_url,product="project",off_team_url=None):
        #封装URL
        public_url = "https://devapi.myones.net/{}/master".format(product)
        if off_team_url != None:
            public_url += "/{}".format(work_url)
            return public_url
        else:
            public_url += "/team/{}{}".format(team_uuid,work_url) #"Sh1mfGBd"
            return public_url

    def setup_login(self,SessionMechanism,email,password,team_name=None):
        global team_uuid
        login_url = self.base_url("/auth/login", off_team_url="login")
        data = {
            "email": email,
            "password": password
        }
        response = SessionMechanism.post(url=login_url, json=data)
        response_json = response.json()
        token = response_json["user"]["token"]
        user_uuid = response_json["user"]["uuid"]
        headers_message = {
            'referer': 'https://dev.myones.net/project/master/',
            'Content-Type': 'application/json',
            "Ones-Auth-Token": token,
            "Ones-User-Id": user_uuid
        }
        team_uuid = ""
        SessionMechanism.headers.update(headers_message)
        if team_name == None:
            team_uuid = response_json["teams"][0]["uuid"]
        else:
            team_uuid = "".join([j["uuid"] for j in response_json["teams"] if j["name"] == team_name])

        return team_uuid


SetupApi = SetupApi()
# SessionMechanism = requests.session()
# SetupApi.setup_login(SessionMechanism,config["EMAIL"],config["PASSWORD"],config["PRODUCT"])
# url=SetupApi.base_url(work_url="/items/graphql")
# print(url)
# if __name__ == '__main__':
#     ones_api = SetupApi("wujian@ones.ai","wujian8808","Core")
#     ones_api.get_graphql_products()
#     ones_api.get_projects()


