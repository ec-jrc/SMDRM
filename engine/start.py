# -*- coding: utf-8 -*-

import os
import pathlib
import time

from src import pipelines

import libdrm.datamodels
import libdrm.deploy
import libdrm.observer


# current directory
root = pathlib.Path(__file__).resolve().parent

# filesystem
data_dir = root / "data"
data_dir.mkdir(parents=True, exist_ok=True)


def observe():
    # subject concrete class implements state and observation logic
    subject = libdrm.observer.FileUploadSubject(observed_path=data_dir)
    # observe the subject's state for updates
    upload_observer = libdrm.observer.FileUploadObserver(
        pipelines.pipe_and_filter,
        pipelines.processing_steps,
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
    args = parser.parse_args()
    # wait for annotations API to be available
    libdrm.deploy.wait_for(os.getenv("FLOODS_API_URL", "http://localhost:5100"))
    # start observing defined paths
    observe()
