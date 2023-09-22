from src.apis.base_api import BaseApi
from src.repositories.timezone_repository import TimezoneRepository
from datetime import datetime, timedelta
import pytz
import logging
logger = logging.getLogger(__name__)
import re
from src.validators.timezone_validator import TimezoneValidator

class ReadTimezone(BaseApi):
    def __init__(self):
        super().__init__()

    # Fetches the given timezones from the repository
    def __call__(self, names):
        TimezoneValidator().validate_names(names)

        logger.info('ReadTimezone called with names={}'.format(names))
        timezone_objs = TimezoneRepository().read_by_names(names)
        timestamps = self._serialize(timezone_objs)
        logger.info('ReadTimezone about to return timestamps={}'.format(timestamps))
        return timestamps

    # private

    def _serialize(self, timezone_objs):
        timestamps = []
        for obj in timezone_objs:
            if obj is None:
                timestamps.append(BaseApi.EMPTY_ITEM) # Adds null for missing timezones
            else:
                time_now = self._compute_time(obj)
                timestamps.append(time_now)

        return timestamps

    def _compute_time(self, timezone):
        if timezone.is_custom:
            return self._compute_custom_timestamp(timezone)
        else:
            return self._compute_standard_timestamp(timezone)

    def _compute_standard_timestamp(self, timezone):
        try:
            local_time = datetime.now(pytz.timezone(timezone.name))
            timestamp = self._to_timestamp(local_time)
        except pytz.exceptions.UnknownTimeZoneError:
            timestamp = BaseApi.EMPTY_ITEM

        return timestamp

    def _compute_custom_timestamp(self, timezone):
        # get current time
        utc_now_dt = datetime.now(tz=pytz.UTC)
        # add offset
        local_time = utc_now_dt + timedelta(seconds=timezone.offset)
        timestamp = self._to_timestamp(local_time)
        return timestamp

    def _to_timestamp(self, a_datetime):
        return a_datetime.replace(microsecond=0).isoformat()
