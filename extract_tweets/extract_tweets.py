import json
import logging
import os
import sys
import typing

from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.common import iter_in_batches, get_version, path_arg, log_execution

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


def parse_required_fields(zip_file: typing.Type[ZipFileModel]) -> typing.Iterable[dict]:
    """Parse unprocessed datapoint, and required fields yield from the input zip file."""
    for jsonl in zip_file.iter_jsonl():

        if not jsonl:
            console.debug("Invalid JSON.")
            continue

        # get raw tweet if exists
        jsonl = jsonl.get("tweet", jsonl)
        # build datapoint model
        # extract the following:
        #  - id
        #  - created_at
        #  - lang
        #  - text
        datapoint = DataPointModel.parse_obj(jsonl)
        # extend text field from tweet object
        datapoint.text = extend_text_field(jsonl)
        yield datapoint.dict()


def make_ndjson_batches(
    parsed_json_gen: typing.Iterable[dict], batch_size: int = 1000
) -> typing.Iterable[str]:
    """Iterate NDJSON batches from a generator of JSON datapoints."""
    for batch in iter_in_batches(parsed_json_gen, batch_size=batch_size):
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

    # extract/parse/model raw data
    ndjson_batches = make_ndjson_batches(
        parse_required_fields(zip_file), batch_size=args.batch_size
    )
    # cache
    metrics = zip_file.cache(args.output_path, ndjson_batches)
    console.info(metrics)


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
