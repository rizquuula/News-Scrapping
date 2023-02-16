import time


def get_timestamp():
    return str(time.time()).split('.')[0]
