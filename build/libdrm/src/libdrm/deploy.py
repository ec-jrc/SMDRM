import requests
import sys
import time

import libdrm.nicelogging

console = libdrm.nicelogging.console_logger("libdrm.deploy")


def wait_for(url, freq: int = 10, max_attempts: int = 5) -> None:
    """
    An helper function to wait for a web service to be up and running.
    An HTTP GET request is fired at a user-defined frequency to obtain a successful response.
    Useful during Docker service deployment to ensure dependent services are available.
    """
    ready = False
    attempts = 0
    console.info("Ping {url} every {freq}s".format(url=url, freq=freq))
    while not ready:
        attempts += 1
        try:
            console.info("Attempt {a}/{t}".format(a=attempts, t=max_attempts))
            requests.get(url)
        except requests.exceptions.ConnectionError:
            time.sleep(freq)
            if attempts == max_attempts:
                console.info("Max attempts reached. exiting...")
                sys.exit(35)
            continue
        ready = True
    console.info("API is ready!")
