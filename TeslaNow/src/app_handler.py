from src.router import Router
import logging
import traceback
logger = logging.getLogger(__name__)
import re
class AppHandler:
    DISALLOWED_CHARS_REGEX = r'[^a-zA-Z ;,+0-9/_-]+'

    def __init__(self):
        pass

    # Converts from semicolon-delimited lists to arrays, back and forth
    def __call__(self, byte_data):
        encoded_result = b''
        try:
            raw_data = byte_data.decode('UTF-8', 'strict')
            if re.search(AppHandler.DISALLOWED_CHARS_REGEX,raw_data):
                logger.info('Server only allows characters typically found in timezones,commas,semicolons and space')
                return encoded_result

            api, params_str = raw_data.split(' ', 1)
            params = params_str.split(';')
            results = Router()(api, params)
            result = (';').join([str(r) for r in results]) + "\n"
            encoded_result = result.encode()
            return encoded_result
        except UnicodeDecodeError:
            logger.info('Server does not accept any non utf-8 characters')
        except Exception as e:
            #TODO: This should not exist in production. Just added for easier debugging for more insights.
            traceback.print_exc()
            logger.info('Had trouble parsing the following input:{} with error {}'.format(raw_data, e))
        return encoded_result
