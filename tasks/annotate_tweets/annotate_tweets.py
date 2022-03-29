import json
import logging
import os
import requests
import sys
import typing

from libdrm.common import iter_in_batches, get_version, path_arg, log_execution
from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.pipelines import Pipeline

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("annotate_tweets")

def get_annotation_scores(texts: list, annotator_id: str) -> typing.List[str]:
    """Template HTTP POST call to REST API annotator to annotate a list of texts."""
    url = "http://{host}:{port}/model/annotate".format(host=annotator_id, port=5000)
    response = requests.post(url, json={"texts": texts})
    response.raise_for_status()
    return response.json()


def get_cnn_texts_from_batch(batch: typing.Iterable[dict]) -> typing.List[str]:
    # get cleaned texts ready for NER model prediction
    cnn_texts = [datapoint["text_clean"] for datapoint in batch]
    if not cnn_texts:
        msg = "`text_clean` field not found. Make sure you use data that passed the transform_tweets task."
        console.warning(msg)
        raise ValueError(msg)
    return cnn_texts


def annotate_batches(
    datapoints_batches: typing.Iterable[dict],
    annotator_id: str,
) -> typing.Iterable[dict]:
    """Annotate datapoints batches.
    Batches are required only for annotation to reduce the number of calls to the annotator."""

    for datapoints_batch in datapoints_batches:
        # annotate texts
        scores = get_annotation_scores(
            get_cnn_texts_from_batch(datapoints_batch),
            annotator_id=annotator_id
        )
        # update annotation field in batch
        for datapoint, score in zip(datapoints_batch, scores):
            datapoint["annotation"] = {annotator_id: score}

        # return annotated datapoints
        yield from datapoints_batch 


def task_metrics(
    datapoints: typing.Iterable[dict],
) -> typing.Iterable[dict]:
    """Compute task metrics."""
    annotated = 0
    for datapoint in datapoints:
        if datapoint["annotation"] is not None: 
            annotated += 1
        yield datapoint
    console.info(dict(annotated=annotated))


def log_datapoints(
    datapoints: typing.Iterable[dict],
) -> typing.Iterable[dict]:
    """Log datapoints to console."""
    for datapoint in datapoints:
        console.debug(datapoint)
        yield datapoint


def make_ndjson_batches(
    datapoints: typing.Iterable[dict],
    batch_size: int = 1000,
) -> typing.Iterable[str]:
    """Iterate NDJSON batches from a generator of JSON datapoints."""
    for batch in iter_in_batches(datapoints, batch_size=batch_size):
        yield "".join(
            [json.dumps(datapoint, ensure_ascii=False) + "\n" for datapoint in batch]
        )


@log_execution(console)
def run(args):
    console.info("opts={}...".format(vars(args)))
    if args.debug:
        console.setLevel(logging.DEBUG)

    # make output path
    if not args.output_path:
        args.output_path = args.input_path.replace(".zip", "_ann.zip")
        console.warning("Default output path is {}".format(args.output_path))

    # input path validation
    zip_file = ZipFileModel(args.input_path)
    if not zip_file.is_valid():
        raise TypeError("Not a valid zip file.")

    # build annotation pipeline
    annotate_pipeline = Pipeline()
    annotate_pipeline.add(iter_in_batches, dict(batch_size=args.batch_size))
    annotate_pipeline.add(annotate_batches, dict(annotator_id=args.annotator_id))
    annotate_pipeline.add(task_metrics)
    annotate_pipeline.add(log_datapoints)
    annotate_pipeline.add(make_ndjson_batches)

    # execute pipeline on raw datapoints
    datapoints = zip_file.iter_jsonl()
    annotated_datapoints = annotate_pipeline.execute(datapoints)

    # cache
    zip_file.cache(args.output_path, annotated_datapoints)


if __name__ == "__main__":
    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Annotate `text` data with Named Entity Recognition algorithms."
    )
    parser.add_argument(
        "--input-path",
        required=True,
        type=path_arg,
        help="The path from which you want to get input data.",
    )
    parser.add_argument(
        "--output-path",
        default=False,
        help="The path to which you want to save the task output.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="The size of each batch in which a file is split.",
    )
    parser.add_argument(
        "--annotator-id",
        default=os.getenv("ANNOTATOR_ID", "floods"),
        help="The annotator ID to send the HTTP POST requests to. Default is %(default)s.",
    )
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
