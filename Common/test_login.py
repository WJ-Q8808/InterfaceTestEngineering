import requests
from pprint import pprint

requests_sessions = requests.session()


def get_pubilc_url(product):
    pubilc_url = "https://devapi.myones.net/{}/master".format(product)
    return pubilc_url

def test_login(requests_sessions):
    login_url = '/auth/login'
    url_login = "{}{}".format(get_pubilc_url("project"), login_url)
    payload = {
        'password': 'wujian8808',
        'email': 'wujian@ones.ai'
    }

    response = requests_sessions.post(url=url_login,json=payload).json()
    token = response["user"].get("token")
    user_uuid = response["user"].get("uuid")
    def get_team(team_name):
        team_uuid = ""
        teams = response["teams"]
        for team in teams:
            if team_name in team["name"]:
                team_uuid += team["uuid"]
        return team_uuid
    team_uuid = get_team("Demo测试团队")
    header = {
        'referer': 'https://dev.myones.net/project/master/',
        'Content-Type': 'application/json',
        'Ones-Auth-Token':token,
        'Ones-User-Id':user_uuid
    }
    # global s = requests_sessions.headers.update(header)
    requests_sessions.headers.update(header)
    requests_dict = {"team_uuid":team_uuid,"requests_sessions":requests_sessions}
    return requests_dict

def get_projects(requests):
    url_projects = "https://devapi.myones.net/project/master/team/{}/projects/my_project".format(requests.get("team_uuid"))
    response = requests.get("requests_sessions").get(url=url_projects).json()
    print(response)
    return response



if __name__ == '__main__':
    requests_dict=test_login(requests_sessions)
    pprint(requests_sessions.headers)
    get_projects(requests_dict)


