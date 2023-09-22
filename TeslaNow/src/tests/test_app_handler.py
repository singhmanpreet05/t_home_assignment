from src.repositories.timezone_repository_mysql import TimezoneRepositoryMysql
import unittest
from src.app_handler import AppHandler
from datetime import datetime

class TestAppHandler(unittest.TestCase):

    def test_wierd_character_input(self):
        command  = b'!@#R'
        response = AppHandler()(command)
        self.assertEqual(response, b'')


    def test_happy(self):
        command = b"read UTC"
        timestamp_encoded_with_newline = AppHandler()(command)
        timestamp_encoded = timestamp_encoded_with_newline[:-1]
        timestamp = timestamp_encoded.decode()
        try:
            datetime.fromisoformat(timestamp)
        except:
            self.fail("AppHandler raised exception unexpectedly!")
