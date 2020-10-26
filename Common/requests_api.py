import requests
import logging

logging.

class Publice_requests:

    def __init__(self):
        self.requests_sessions = requests.session()

    pass


logger = logging.getLogger(__name__)

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