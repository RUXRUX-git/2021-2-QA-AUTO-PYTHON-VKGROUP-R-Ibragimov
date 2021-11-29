import time
import requests

from faker import Faker

fake = Faker()


def create_random_first_name():
    return {
        'name': fake.first_name()
    }


def create_random_last_name():
    return {
        'surname': fake.last_name()
    }


def create_random_user():
    return create_random_first_name() | create_random_last_name()


def wait_ready(host, port):
    started = False
    st = time.time()
    while time.time() - st <= 5:
        try:
            requests.get(f'http://{host}:{port}')
            started = True
            break
        except ConnectionError:
            pass
    if not started:
        raise RuntimeError(f'{host}:{port} did not started in 5s!')