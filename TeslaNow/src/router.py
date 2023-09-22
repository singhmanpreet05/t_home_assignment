import logging
from src.apis.read_timezone import ReadTimezone
from src.apis.upsert_timezone import UpsertTimezone
from src.apis.delete_timezone import DeleteTimezone

logger = logging.getLogger(__name__)

class Router:
    def __init__(self):
        self.apis = {
            "read": ReadTimezone,
            "upsert": UpsertTimezone,
            "delete": DeleteTimezone
        }

    def __call__(self, api_name, params):
        logger.info('Router invoked with api_name={} params={}'.format(api_name, params))
        if (api_name in self.apis.keys()) and (len(params) <= 1024):
            api_handler = self.apis[api_name]
            result_list = self.__call_api(api_handler, params)
            logger.info('Router about to return result_list={}'.format(result_list))
            return result_list
        elif api_name not in self.apis.keys():
            msg = "No api with name {} found".format(api_name)
            logger.info(msg)
            raise AssertionError(msg)
        else:
            raise AssertionError("params too long of length:{}".format(len(params)))


    # private

    def __call_api(self, api_handler, params):
        try:
            return api_handler()(params)
        except Exception as e:
            logger.info("The api handler errored out with: {}".format(e))
            raise e


