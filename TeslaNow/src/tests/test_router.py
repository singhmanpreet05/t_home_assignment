from src.repositories.timezone_repository_mysql import TimezoneRepositoryMysql
import unittest
from src.router import Router
from datetime import datetime

class TestRouter(unittest.TestCase):

    def test_invalid_name(self):
        command  = 'readify'
        params = []

        with self.assertRaises(AssertionError):
            Router()(command, params)


    def test_happy(self):
        api = "read"
        names = ['UTC', 'US/Pacific']
        timestamps = Router()(api, names)
        for timestamp in timestamps:
            try:
                datetime.fromisoformat(timestamp)
            except:
                self.fail("TimezoneValidator raised ExceptionType unexpectedly!")
