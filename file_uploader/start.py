# -*- coding: utf-8 -*-

from src.observer import (
    FileUpload,
    FileUploadObserver,
)

from src.config import get_config


if __name__ == "__main__":
    import argparse
    import time

    parser = argparse.ArgumentParser(
        description="Upload JSON events from uploaded zip file to a RabbitMQ server."
    )
    parser.add_argument(
        "--path",
        required=True,
        help="The directory path of the files to upload.",
    )
    args = parser.parse_args()

    # get configuration
    # export ENV=dev returns configuration for a specific environment
    config = get_config()

    # subject concrete class implements state and observation logic
    subject = FileUpload(path=args.path, config=config)
    # observe the subject's state for updates
    observer = FileUploadObserver()
    subject.attach(observer)

    observing = True
    while observing:
        try:
            subject.observe()
            time.sleep(config.observing_interval)
        except KeyboardInterrupt:
            observing = False
