"""
Engine:
    - Observe path for new files to add to the processing pipeline
    - Pipeline is made of 5 steps to read, validate, prepare, annotate, and log disaster data points.
"""

import os
import pathlib
import time
import typing

import libdrm.datamodels
import libdrm.deploy
import libdrm.elastic
import libdrm.nicelogging
import libdrm.pipeline

import apis

# logging
console = libdrm.nicelogging.console_logger("engine.start")

# current directory
root = pathlib.Path(__file__).resolve().parent

# filesystem
uploads_path = root / "uploads"
uploads_path.mkdir(parents=True, exist_ok=True)

# env variables
disaster_type = os.getenv("DISASTER_TYPE").lower()
observe_freq_sec = int(os.getenv("OBSERVE_FREQ_SEC", 5))


def iter_annotate_batches(batches: typing.Iterable[dict]) -> typing.Iterable[dict]:
    for batch in batches:
        annotated = apis.api_annotate(disaster_type, batch)
        console.debug(
            "{}API: status_code={}".format(disaster_type.title(), annotated.status_code)
        )
        yield annotated.json()


def iter_save_batches(batches: typing.Iterable[dict]) -> None:
    for batch in batches:
        console.debug(batch)
        es.bulk_insert(batch["batch"])


def observe():
    console.info("Observing {}...".format(uploads_path))
    files = [_file for _file in uploads_path.glob("*.zip")]
    if files:
        console.info("New files observed")
        # Docker annotator API service must run to get annotations
        libdrm.pipeline.process_uploads(
            files, extra_steps=[iter_annotate_batches, iter_save_batches]
        )
        for file in files:
            file.unlink()
            console.debug("{} removed".format(file))
        console.info("Processed. Waiting on new files...")
    else:
        console.debug("Unchanged. Sleeping {}s ...".format(observe_freq_sec))
        time.sleep(observe_freq_sec)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Observe a defined path for user interactions."
    )

    # wait for API availability
    libdrm.deploy.wait_for("http://floods:5001", max_attempts=10)
    libdrm.deploy.wait_for("http://elasticsearch:9200", max_attempts=10)

    # create elasticsearch index
    es = libdrm.elastic.ElasticSearchClient("http://elasticsearch:9200", "smdrm-dev")
    es.create_index()

    # start observing defined paths
    OBSERVING = True
    while OBSERVING:
        try:
            observe()
        except KeyboardInterrupt:
            OBSERVING = False
