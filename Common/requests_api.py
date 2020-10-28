import requests
import logging

logger = logging.getLogger(__name__)


class Publice_requests:

    def __init__(self):
        self.requests_sessions = requests.session()
    def __init__(self,product):
        pubilc_url = "https://devapi.myones.net/{}/master".format(product)


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
    pass


class BaseService:

    def __init__(self, config):
        self.config = config

    def base_request(self, url, json=None, headers=None, **kwargs):
        result = None
        logger.info('request: {}'.format(url))
        try:
            if json:
                result = requests.post(
                    url=url, json=json, headers=headers,
                    timeout=self.config.REQUEST_TIMEOUT,
                    **kwargs
                ).json()
            else:
                result = requests.get(url=url, json=json, headers=headers).json()
        except RuntimeError as e:
            logger.error("request error: {}".format(traceback.format_exc()))
            raise e

        logger.debug('response: {}'.format(result))
        return result