from src.apis.base_api import BaseApi
from src.repositories.timezone_repository import TimezoneRepository
from datetime import datetime
import pytz
import logging
logger = logging.getLogger(__name__)
from src.validators.timezone_validator import TimezoneValidator

class DeleteTimezone(BaseApi):
    def __init__(self):
        super().__init__()

    def __call__(self, names):
        logger.info('DeleteTimezone called with names={}'.format(names))
        TimezoneValidator().validate_names(names)
        response = TimezoneRepository().delete_records(names)
        logger.info('DeleteTimezone about to return rows updated={}'.format(response))
        return [response]