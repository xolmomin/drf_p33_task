from random import randint


def random_code():
    return randint(100_000, 999_999)  #


def send_sms_code(phone: str, code: int):
    print(phone, code)
    # TODO send sms
