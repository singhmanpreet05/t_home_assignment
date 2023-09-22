from src.apis.base_api import BaseApi
from src.repositories.timezone_repository import TimezoneRepository
from datetime import datetime
import pytz
import logging
logger = logging.getLogger(__name__)
from src.validators.timezone_validator import TimezoneValidator

class UpsertTimezone(BaseApi):
    def __init__(self):
        super().__init__()

    # Upserts Custom Timezones
    def __call__(self, name_offset_str_list):

        logger.info('UpsertTimezone called with name_offset_str_list={}'.format(name_offset_str_list))

        name_offset_list = []
        for name_offset in name_offset_str_list:
            name, offset_str = name_offset.split(',', 1)
            offset = int(offset_str)
            name_offset_list.append([name, offset])

        names = list(zip(*name_offset_list))[0]
        TimezoneValidator().validate_names(names)
        response = TimezoneRepository().upsert_records(name_offset_list)
        logger.info('UpsertTimezone about to return rows_updated={}'.format(response))
        return [response]