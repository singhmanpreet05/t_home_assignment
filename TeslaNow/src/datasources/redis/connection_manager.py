import redis
import os

class ConnectionManager:
    def __init__(self):
        # TODO: Move these secrets to env variables
        self.connection = None
        try:
            self.connection = self._new_connection()
        except Exception:
            pass

    def get_connection(self):
        if (not self.connection) or (not self.connection.ping()):
            self.connection = self._new_connection()
        return self.connection

    # private

    def _new_connection(self):
        redis_host = os.environ['REDIS_HOST']
        redis_database = os.environ['REDIS_DATABASE']
        redis_port = os.environ['REDIS_PORT']
        redis_password = os.environ['REDIS_PASSWORD']
        return redis.Redis(host=redis_host, port=redis_port, db=redis_database, password=redis_password)

connection_manager_instance = ConnectionManager()

