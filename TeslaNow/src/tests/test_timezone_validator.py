import unittest

from src.validators.timezone_validator import TimezoneValidator


class TestValidator(unittest.TestCase):
    def test_validate_names_pos(self):
        """
        Test if various kinds of timezone names do not throw error
        """
        timezones = ['US/Indiana-Starke', 'US/Michigan', 'US/Pacific', 'US/Samoa', 'UTC', 'W-SU', 'WET', 'Zulu']
        try:
            TimezoneValidator().validate_names(timezones)
        except Exception:
            self.fail("TimezoneValidator raised ExceptionType unexpectedly!")

    def test_validate_names_neg(self):
        timezones = ['!@#R', '^Gf', 'hello world']

        for timezone in timezones:
            with self.assertRaises(AssertionError):
                TimezoneValidator().validate_names([timezone])




