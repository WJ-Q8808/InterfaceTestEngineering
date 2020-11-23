from Config.loadconfig import ReadConfig
import requests
import time

config = ReadConfig("config.json").read_file()


class SetupApi:

    def __init__(self):
        self.config = ReadConfig("config.json").read_file()

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
        # 登陆后，更新SessionMechanism，获取 team_uuid
        global team_uuid
        login_url = self.base_url("/auth/login", off_team_url="login")
        data = {"email": email, "password": password}
        response = SessionMechanism.post(url=login_url, json=data)
        response_json = response.json()
        headers_message = {
            'referer': self.config["REFERER"],
            'Content-Type': 'application/json',
            "Ones-Auth-Token": response_json["user"]["token"],
            "Ones-User-Id": response_json["user"]["uuid"]
        }
        #更新SessionMechanism头部
        SessionMechanism.headers.update(headers_message)
        team_uuid = ""
        if team_name == None:
            team_uuid = response_json["teams"][0]["uuid"]
        else:
            team_uuid = "".join([j["uuid"] for j in response_json["teams"] if j["name"] == team_name])

        return response


if __name__ == '__main__':
    SetupApi = SetupApi()
    SessionMechanism = requests.session()
    response = SetupApi.setup_login(SessionMechanism, config["EMAIL"], config["PASSWORD"], config["PRODUCT"])
    time.time()


