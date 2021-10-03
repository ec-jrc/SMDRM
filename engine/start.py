# -*- coding: utf-8 -*-

import os
import time

from libdrm import (
    observer,
    pipelines,
)


def foo():
    # check if ml APIs are up
    # client_floods.wait_for_it()
    # block until APIs are up
    pass


def observe(path):
    # subject concrete class implements state and observation logic
    subject = observer.FileUploadSubject(observed_path=path)
    # observe the subject's state for updates
    upload_observer = observer.FileUploadObserver(
        pipelines.pipe_and_filter, pipelines.processing_steps
    )
    subject.attach(upload_observer)
    # start observing every OBSERVE_INTERVAL_SEC
    observing = True
    while observing:
        try:
            subject.observe()
            time.sleep(int(os.getenv("OBSERVE_INTERVAL_SEC", 5)))
        except KeyboardInterrupt:
            observing = False


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Observe path for new files to add to the processing pipeline."
    )
    parser.add_argument(
        "-p",
        "--path-to-observe",
        required=True,
        help="The directory path under observation.",
    )
    args = parser.parse_args()
    # start observing defined paths
    observe(args.path_to_observe)
