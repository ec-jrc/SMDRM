import logging
import os
import pandas
import typing
import sys

from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches, get_version, path_arg, log_execution
from libdrm.pipelines import Pipeline

from transformations import (
    tag_with_mult_bert,
    extract_place_candidates,
    normalize_places,
    apply_transformations,
)

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("transform_tweets")


def convert_to_dataframe(datapoints_batches: typing.Iterable[list]) -> typing.Iterable[pandas.DataFrame]:
    """Converts datapoints batches i.e. list of JSON into Pandas DataFrame."""
    for datapoints_batch in datapoints_batches:
        yield pandas.DataFrame(datapoints_batch)


def get_duplicates_filter(batch_df: pandas.DataFrame) -> pandas.Series:
    """Get boolean mask of duplicated datapoints."""
    return batch_df.duplicated(subset="text", keep='first')


def merge_duplicates_on_transformed(unique_transformed, duplicates):
    """Merge transformed unique datapoints onto duplicates.
    Drop target columns to avoid pandas suffix patching (i.e. <col>_x, <col>_y)."""
    enriched_duplicates = duplicates.drop(columns=["place", "text_clean"]).merge(unique_transformed[["place", "text", "text_clean"]], on="text")
    return pandas.concat([unique_transformed, enriched_duplicates]).reset_index(drop=True)


def transform_datapoints(
        datapoints_batches: typing.Iterable[pandas.DataFrame],
        allowed_tags: typing.List[str],
) -> typing.Iterable[pandas.DataFrame]:
    for batch_id, batch_df in enumerate(datapoints_batches, start=1):

        # find duplicated datapoints in batch
        duplicates = get_duplicates_filter(batch_df)
        console.debug("duplication ratio {:.4f}".format(duplicates.sum() / len(duplicates)))

        # split batch into unique and duplicated datapoints
        # only unique datapoints are tagged with the NER algorithm
        unique_datapoints = batch_df[~duplicates].copy()
        duplicated_datapoints = batch_df[duplicates].copy() 

        # tag texts with DeepPavlov (multilingual BERT) NER model
        y_hat = tag_with_mult_bert(list(unique_datapoints.text))
        # get place candidates using allowed tags
        unique_datapoints["place"] = extract_place_candidates(y_hat, allowed_tags)
        # normalize place candidates and non-alphanumeric chars in text
        unique_datapoints["text_clean"] = unique_datapoints.apply(lambda row: normalize_places(row.text, row.place["candidates"]), axis=1).apply(apply_transformations)
        # merge the transformation applied to unique datapoints onto the duplicated
        yield merge_duplicates_on_transformed(unique_datapoints, duplicated_datapoints)


def task_metrics(datapoints_batches: typing.Iterable[pandas.DataFrame]) -> typing.Iterable[pandas.DataFrame]:
    """Compute task metrics."""
    batches=0
    datapoints=0
    with_place_candidates=0
    for datapoints_batch in datapoints_batches:
        # number of batches
        batches += 1
        # number of datapoints in batch
        datapoints += len(datapoints_batch)
        # number of datapoints in batch with place candidates
        with_place_candidates += datapoints_batch.place.apply(lambda row: bool(row["candidates"])).sum()
        yield datapoints_batch
    console.info(dict(batches=batches, datapoints=datapoints, with_place_candidated=with_place_candidates))


def log_datapoints(datapoints_batches: typing.Iterable[pandas.DataFrame]) -> typing.Iterable[pandas.DataFrame]:
    """Log datapoints to console."""
    for batch_id, datapoints_batch in enumerate(datapoints_batches, start=1): 
        console.debug("processing datapoints batch ID #{}... Below, a sample of 5.".format(batch_id))
        console.debug(datapoints_batch.head(5))
        yield datapoints_batch


def make_ndjson_batches(datapoints_batches: typing.Iterable[pandas.DataFrame]) -> typing.Iterable[str]:
    """Convert datapoints batched from pandas.DataFrame to NDJSON format."""
    for batch_df in datapoints_batches:
        yield batch_df.to_json(orient="records", force_ascii=False, lines=True)


@log_execution(console)
def run(args):
    console.info("opts={}...".format(vars(args)))
    if args.debug:
        console.setLevel(logging.DEBUG)

    # make output path
    if not args.output_path:
        args.output_path = args.input_path.replace(".zip", "_tra.zip")
        console.warning("Default output path is {}".format(args.output_path))

    # input path validation
    zip_file = ZipFileModel(args.input_path)
    if not zip_file.is_valid():
        console.error("Not a valid zip file.")
        sys.exit(13)

    # DeepPavlov NER algorithm uses prefixes to indicate B-egin,
    # and I-nside relative positions of tokens. For more details, visit
    # http://docs.deeppavlov.ai/en/master/features/models/ner.html#ner-task.
    allowed_tags = ["B-GPE", "I-GPE", "B-FAC", "I-FAC", "B-LOC", "I-LOC"]
    console.info("Allowed NER tags={}".format(allowed_tags))

    # build transformation pipeline
    transform_pipeline = Pipeline()
    transform_pipeline.add(iter_in_batches, dict(batch_size=args.batch_size))
    transform_pipeline.add(convert_to_dataframe)
    transform_pipeline.add(transform_datapoints, dict(allowed_tags=allowed_tags))
    transform_pipeline.add(task_metrics)
    transform_pipeline.add(log_datapoints)
    transform_pipeline.add(make_ndjson_batches)

    # execute pipeline on extracted datapoints
    datapoints = zip_file.iter_jsonl()
    transformed_datapoints = transform_pipeline.execute(datapoints)

    # cache
    zip_file.cache(args.output_path, transformed_datapoints)


if __name__ == "__main__":
    """
    Exit Codes
      1 - Path not found
      2 - Path is a directory, but a zip file is expected
      3 - Not a valid zip file
    """

    from argparse import ArgumentParser

    parser = ArgumentParser(
        description="Transform data point `text` field."
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
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())

