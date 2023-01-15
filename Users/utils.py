import random
from datetime import datetime


def generate_otp():
    fixed_digits = 6
    return random.randrange(111111, 999999, fixed_digits)


class generateKey:
    @staticmethod
    def returnValue(phone):
        return str(phone) + str(datetime.date(datetime.now())) + "Some Random Secret Key"
