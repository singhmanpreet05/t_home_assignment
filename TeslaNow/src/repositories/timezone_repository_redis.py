from datetime import datetime
import pytz

from src.repositories.base_repository import BaseRepository
from src.entities.timezone import Timezone
import logging
logger = logging.getLogger(__name__)
from src.datasources.redis.connection_manager import connection_manager_instance
import itertools
import json

class TimezoneRepositoryRedis(BaseRepository):
    def __init__(self):
        super().__init__()

    # TODO: Make it use dependency injection to use specific datasource
    def read_by_names(self, names):
        logger.info('read_by_names called with names={}'.format(names))
        connection = connection_manager_instance.get_connection()
        timezone_jsons = connection.mget(*names)
        logger.info("connection.mget with names:{}".format(names))
        timezone_hashes = [json.loads(timezone_json) for timezone_json in timezone_jsons if timezone_json is not None]
        timezone_records = [list(timezone_hash.values()) for timezone_hash in timezone_hashes]
        logger.info('query result:{}'.format(timezone_records))

        timezone_map = dict([ [timezone_record[0], Timezone(*timezone_record)] for timezone_record in  timezone_records])
        timezone_objs = list(map(lambda name: timezone_map.get(name, None), names))
        logger.info('Timezone Repo about to return:{}'.format(timezone_objs))
        return timezone_objs

    def upsert_records(self, name_offset_list):
        logger.info('upser_records called with timezone_offset_list={}'.format(name_offset_list))
        connection = connection_manager_instance.get_connection()
        name_to_data = {}
        for name, offset in name_offset_list:
            data = {
                "name": name,
                "is_custom": True,
                "offset": offset,
                "created_at": datetime.now(tz=pytz.UTC).replace(microsecond=0).isoformat(),
                "updated_at": datetime.now(tz=pytz.UTC).replace(microsecond=0).isoformat()
            }
            name_to_data[name] = json.dumps(data)
        logger.info("connection.mset with input:{}".format(name_to_data))
        result = connection.mset(name_to_data)
        logger.info('query result:{}'.format(result))
        return bool(result)

    def delete_records(self, names):
        logger.info('delete_records called with names={}'.format(names))
        connection = connection_manager_instance.get_connection()
        logger.info("connection.del with input:{}".format(names))
        result = connection.delete(*names)
        logger.info('query result:{}'.format(result))

        return bool(result)

