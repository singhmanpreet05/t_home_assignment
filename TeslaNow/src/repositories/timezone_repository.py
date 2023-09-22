from src.repositories.timezone_repository_mysql import TimezoneRepositoryMysql
from src.repositories.timezone_repository_redis import TimezoneRepositoryRedis
import os

if os.environ['DATASOURCE'] == 'MYSQL':
    TimezoneRepository = TimezoneRepositoryMysql
elif os.environ['DATASOURCE'] == 'REDIS':
    TimezoneRepository = TimezoneRepositoryRedis
else:
    pass