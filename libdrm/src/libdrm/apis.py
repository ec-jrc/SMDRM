import logging
import requests
import sys
import time


console = logging.getLogger("libdrm.apis")


# dictionary key should match the libdrm.schemas.MetadataUploadSchema *_annotator properties
APIs_lookup = {
    "elastic": "http://elasticsearch:9200",
    "fires_annotator": "http://fires:5002/annotate",
    "floods_annotator": "http://floods:5001/annotate",
}


def get_annotators_lookup() -> dict:
    """Method to get Annotator API endpoints ONLY from name.
    This is used by Engine API to get the Annotation API endpoints selected by the user."""
    annotators_only = {name: url for name, url in APIs_lookup.items() if "_annotator" in name}
    return annotators_only


def check_status(url: str = None, sleep: int = 10, attempts: int = 6) -> None:
    """
    An helper function to wait for a web service to be up and running.
    An HTTP GET request is fired after a sleep time to obtain a successful response.
    Useful during Docker service deployment to ensure dependent services are available.
    """
    attempt = 0
    ready = False
    console.info("Ping {url}, then sleep {sleep}s".format(url=url, sleep=sleep))
    while not ready:
        attempt += 1
        try:
            console.info("Attempt {a}/{t}".format(a=attempt, t=attempts))
            requests.get(url)
        except requests.exceptions.ConnectionError:
            time.sleep(sleep)
            if attempt == attempts:
                console.info("Maximum number of attempts reached. Calling sys.exit().")
                sys.exit(35)
            continue
        ready = True
