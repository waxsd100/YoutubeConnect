import functools

import backoff
import requests

from const import API_TIMEOUT


def resend(function):
    @functools.wraps(function)
    def wrapped(*args, **kwargs):
        def fatal_code(e):
            """Too many Requests(429)のときはリトライする。それ以外の4XXはretryしない"""
            if e.response is None:
                return True
            code = e.response.status_code
            return 400 <= code < 500 and code != 429

        return backoff.on_exception(
            backoff.expo,
            requests.exceptions.RequestException,
            jitter=backoff.full_jitter,
            max_time=300,
            giveup=fatal_code
        )(function)(*args, **kwargs)

    return wrapped


@resend
def send_data(session, url, headers, json, timeout):
    return session.post(
        url=url,
        headers=headers,
        json=json,
        timeout=timeout
    )


class GatewayServer:

    def __init__(self):
        self.__session = requests.Session()

    @resend
    def post_json(self, url, headers, data):
        return self.__session.post(
            url=url,
            headers=headers,
            json=data,
            timeout=API_TIMEOUT
        )

    @property
    def session(self):
        return self.__session

    @session.setter
    def session(self, session):
        self.__session = session
