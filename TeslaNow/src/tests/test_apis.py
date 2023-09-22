import unittest
from src.apis.read_timezone import ReadTimezone
from src.apis.upsert_timezone import UpsertTimezone
from src.apis.delete_timezone import DeleteTimezone

from datetime import datetime

class TestApis(unittest.TestCase):
    def test_read_api(self):
        timestamps = ReadTimezone()(['UTC', 'Asia/Kolkata'])

        for timestamp in timestamps:
            try:
                datetime.fromisoformat(timestamp)
            except:
                self.fail("TimezoneValidator raised ExceptionType unexpectedly!")

    def test_upsert_api(self):
        result = UpsertTimezone()(['a,1', 'b,2'])
        self.assertEqual(result, [True])

        timestamps = ReadTimezone()(['a', 'b', 'UTC'])
        a_timezone, b_timezone, utc_timestamp = timestamps

        utc_time = datetime.fromisoformat(utc_timestamp).timestamp()
        a_time = datetime.fromisoformat(a_timezone).timestamp()
        b_time = datetime.fromisoformat(b_timezone).timestamp()


        self.assertEqual(a_time - utc_time, 1)
        self.assertEqual(b_time - utc_time, 2)

    def test_delete_api(self):
        result = UpsertTimezone()(['a,1', 'b,2'])
        self.assertEqual(result, [True])

        timestamps = ReadTimezone()(['a', 'b'])
        a_timestamp, b_timestamp = timestamps
        self.assertNotEqual(a_timestamp, 'null')
        self.assertNotEqual(b_timestamp, 'null')

        result = DeleteTimezone()(['a', 'b'])
        self.assertEqual(result, [True])

        timestamps = ReadTimezone()(['a', 'b'])
        a_timestamp, b_timestamp = timestamps
        self.assertEqual(a_timestamp, 'null')
        self.assertEqual(b_timestamp, 'null')







