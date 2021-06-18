import time
import logging
import io
import atexit
import sys

import requests


stringio_stream = io.StringIO()

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s [%(threadName)s] [%(levelname)s] %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    handlers=[logging.StreamHandler(stringio_stream)]
)
log = logging.getLogger(__name__)


def entrypoint(*args, **kwargs):
    # This function should contain the custom logic
    # of your application.
    # Make it as complicated as you need!
    y = 5 + 3
    log.debug('Computed y')
    z = y + 2
    #z = x + 2  # <---- This line has a typo that we'll use to test.
    log.debug('Computed z')


def save_logs(body):
    # This function should implement a robust solution
    # to store the log string.
    # E.g., it could upload a file to S3.
    # For the sake of this tutorial let's upload the string
    # to cl1p.net

    # In a real application you will want to save a file
    # with the name `app_name + timestamp`.
    #clip_name = app_name + '_' + str(int(time.time()))
    # To use it with cl1p.net we must use a fixed name
    clip_name = 'mmm'
    headers = {'Content-Type': 'text/html; charset=UTF-8'}
    endpoint = 'https://api.cl1p.net/' + clip_name
    requests.post(endpoint, headers=headers, data=body)


if __name__ == '__main__':
    app_name = 'CODE_SAMPLE'
    log.debug('Starting %s', app_name)
    try:
        entrypoint(sys.argv)
    except Exception:
        log.exception('Error on %s', app_name)
    else:
        log.debug('Done.')


atexit.register(
    save_logs,
    body=stringio_stream.getvalue() #   <-- This is the trick!
)