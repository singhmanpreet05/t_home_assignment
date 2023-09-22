import re
class TimezoneValidator:
    TIMEZONE_NAME_DISSALLOWED_REGEX = r'[^a-zA-Z+0-9/_-]+'

    def __init__(self):
        pass

    def validate_names(self, names):
        violations = [re.search(TimezoneValidator.TIMEZONE_NAME_DISSALLOWED_REGEX, name) for name in names]
        if any(violations):
            raise AssertionError('One of the timezone names contains unallowed characters:{}'.format(names))