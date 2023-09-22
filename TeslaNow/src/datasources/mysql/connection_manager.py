import MySQLdb
import os

class ConnectionManager:
    def __init__(self):
        # TODO: Move these secrets to env variables
        self.connection = None
        try:
            self.connection = self._new_connection()
        except MySQLdb.OperationalError as e:
            pass

    def get_connection(self):
        if (not self.connection) or (not self.connection.open):
            self.connection = self._new_connection()
        return self.connection
    # private

    def _new_connection(self):
        mysql_host = os.environ['MYSQL_HOST']
        mysql_database = os.environ['MYSQL_DATABASE']
        mysql_user = os.environ['MYSQL_USER']
        mysql_password = os.environ['MYSQL_PASSWORD']
        return MySQLdb.connect(host=mysql_host, user=mysql_user, password=mysql_password, database=mysql_database)

connection_manager_instance = ConnectionManager()

