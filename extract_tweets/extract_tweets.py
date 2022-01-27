import json
import logging
import os
import sys
import typing

from libdrm.common import iter_in_batches, get_version, path_arg, log_execution
from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.pipelines import Pipeline


# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("extract_tweets")


def extend_text_field(data: dict) -> str:
    """Extend text of original tweet with nested search."""
    try:
        return data["retweeted_status"]["extended_tweet"]["full_text"]
    except:
        # Try for extended text of an original tweet, if RT'd (REST API)
        try:
            return data["retweeted_status"]["full_text"]
        except:
            # Try for extended text of an original tweet (streamer)
            try:
                return data["extended_tweet"]["full_text"]
            except:
                # Try for extended text of an original tweet (REST API)
                try:
                    return data["full_text"]
                except:
                    # Try for basic text of original tweet if RT'd
                    try:
                        return data["retweeted_status"]["text"]
                    except:
                        # Try for basic text of an original tweet
                        try:
                            return data["text"]
                        except:
                            # Nothing left to check for
                            return ""


def filter_invalid_datapoints(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]: 
    """Remove invalid datapoints from the pipeline."""
    invalid=0
    for datapoint in datapoints:
        if datapoint is None:
            invalid += 1
            continue
        yield datapoint
    console.info(dict(invalid=invalid))


def parse_raw_datapoints(
        datapoints: typing.Iterable[dict],
        raw_datapoint_field="tweet",
) -> typing.Iterable[dict]:
    """Parse raw (unprocessed) datapoints from given field,
    and extend text using other fields when possible."""
    missing_text=0
    for datapoint in datapoints:
        # get raw datapoint from `tweet` field if exists
        datapoint = datapoint.get(raw_datapoint_field, datapoint)
        # extend text field from tweet object
        extended_text = extend_text_field(datapoint)
        if not extended_text:
            missing_text += 1
        yield datapoint
    console.info(dict(missing_text=missing_text))



def build_datamodel(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
    """Build datapoint model
        base fields
          - id
          - created_at
          - lang
          - text
        optional (set to null if not found in raw datapoint)
          - annotation
          - place
          - text_clean
    """
    for datapoint in datapoints:
        # build datapoint model from dictionary
        datamodel = DataPointModel.parse_obj(datapoint)
        # yield as dictionary
        yield datamodel.dict()


def task_metrics(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
    """Compute task metrics."""
    extracted=0
    for datapoint in datapoints:
        extracted += 1
        yield datapoint
    console.info(dict(extracted=extracted))


def log_datapoints(datapoints: typing.Iterable[dict]) -> typing.Iterable[dict]:
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
        args.output_path = args.input_path.replace(".zip", "_ext.zip")
        console.warning("Default output path is {}".format(args.output_path))

    # input path validation
    zip_file = ZipFileModel(args.input_path)
    if not zip_file.is_valid():
        console.error("Not a valid zip file.")
        sys.exit(13)

    # build extraction pipeline
    extract_pipeline = Pipeline()
    extract_pipeline.add(filter_invalid_datapoints)
    extract_pipeline.add(parse_raw_datapoints, dict(raw_datapoint_field="tweet"))
    extract_pipeline.add(build_datamodel)
    extract_pipeline.add(task_metrics)
    extract_pipeline.add(log_datapoints)
    extract_pipeline.add(make_ndjson_batches, dict(batch_size=args.batch_size))

    # execute pipeline on raw datapoints
    raw_datapoints = zip_file.iter_jsonl()
    extracted_datapoints = extract_pipeline.execute(raw_datapoints)

    # cache
    zip_file.cache(args.output_path, extracted_datapoints)


if __name__ == "__main__":
    """
    Exit Codes
      1 - Path not found
      2 - Path is a directory, but a zip file is expected
      3 - Not a valid zip file
    """

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="It minimizes the memory consumption footprint by removing unnecessary data."
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
        type=path_arg,
        help="The path to which you want to save the task output.",
    )
    parser.add_argument(
        "--batch-size",
        type=int,
        default=1000,
        help="The size of each batch in which a file is split.",
    )
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
