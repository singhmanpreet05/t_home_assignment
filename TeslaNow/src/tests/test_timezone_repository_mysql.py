from src.repositories.timezone_repository_mysql import TimezoneRepositoryMysql
import os
from datetime import datetime
import unittest

class TestTimezoneRepositoryMysql(unittest.TestCase):
    """Oracle MySQL for Python Connector tests."""

    # connection = None
    #
    # def setUp(self):
    #     pass
    #
    # def tearDown(self):
    #     pass
    def test_read(self):
        repo = TimezoneRepositoryMysql()
        timezones = repo.read_by_names(['UTC'])
        timezone = timezones[0]
        self.assertEqual(timezone.name, 'UTC')


    def test_upsert(self):
        repo = TimezoneRepositoryMysql()
        repo.upsert_records([['a', 1]])
        timezones = repo.read_by_names(['a'])
        timezone = timezones[0]
        self.assertEqual(timezone.offset, 1)

    def test_delete(self):
        repo = TimezoneRepositoryMysql()
        repo.upsert_records([['a', 1]])
        timezones = repo.read_by_names(['a'])
        timezone = timezones[0]
        self.assertEqual(timezone.offset, 1)