from src.repositories.base_repository import BaseRepository
from src.entities.timezone import Timezone
import logging
logger = logging.getLogger(__name__)
from src.datasources.mysql.connection_manager import connection_manager_instance
import itertools

class TimezoneRepositoryMysql(BaseRepository):
    def __init__(self):
        super().__init__()

    # TODO: Make it use dependency injection to use specific datasource
    def read_by_names(self, names):
        logger.info('read_by_names called with names={}'.format(names))
        connection = connection_manager_instance.get_connection()
        with connection.cursor() as cursor:
            format_strings = ','.join(['%s'] * len(names))
            query = """SELECT * from timezones where name in ({})""".format(format_strings)
            logger.info('About to fire query: {} with args {}'.format(query, names))
            cursor.execute(query, names)
            timezone_tuples = cursor.fetchall()
            logger.info('query result:{}'.format(timezone_tuples))

        timezone_map = dict([ [timezone_tuple[0], Timezone(*timezone_tuple)] for timezone_tuple in  timezone_tuples])
        timezone_objs = list(map(lambda name: timezone_map.get(name, None), names))
        logger.info('Timezone Repo about to return:{}'.format(timezone_objs))
        return timezone_objs

    def upsert_records(self, name_offset_list):
        logger.info('upser_records called with timezone_offset_list={}'.format(name_offset_list))
        connection = connection_manager_instance.get_connection()
        values_template = ','.join(["(%s, %s, %s)"] * len(name_offset_list))

        query = """INSERT INTO timezones (name,is_custom,offset) VALUES {} ON DUPLICATE KEY UPDATE is_custom=VALUES(is_custom), offset=VALUES(offset);""".format(values_template)
        params = [[name, 1, offset] for name, offset in name_offset_list]
        flat_values = list(itertools.chain(*params))
        with connection.cursor() as cursor:
            logger.info('About to fire query: {} with args {}'.format(query, flat_values))
            cursor.execute(query, flat_values)
            timezone_tuples = cursor.fetchall()
            connection.commit()
            logger.info('query result:{}'.format(timezone_tuples))

        return True

    def delete_records(self, names):
        logger.info('delete_records called with names={}'.format(names))
        connection = connection_manager_instance.get_connection()
        values_template = ','.join(["%s"] * len(names))

        query = """DELETE FROM timezones where name in ({});""".format(values_template)
        with connection.cursor() as cursor:
            logger.info('About to fire query: {} with args {}'.format(query, names))
            cursor.execute(query, names)
            timezone_tuples = cursor.fetchall()
            connection.commit()
            logger.info('query result:{}'.format(timezone_tuples))

        return True

