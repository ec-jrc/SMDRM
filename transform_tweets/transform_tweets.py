import logging
import os
import pandas
import typing
import sys

from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches, get_version, path_arg, log_execution

from transformations import (
    tag_with_mult_bert,
    extract_place_candidates,
    normalize_places,
    get_duplicate_mask,
    apply_transformations,
)

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("transform_tweets")


def make_ndjson_batches(
        zip_file: typing.Type[ZipFileModel],
        allowed_tags: typing.List[str],
        batch_size: int = 1000,
) -> typing.Iterable[str]:
    """Iterate NDJSON batches from a generator of JSON datapoints.
    It implements an ad hoc logic to tag unique datapoint only,
     and update their duplicates."""
    for batch_id, batch in enumerate(iter_in_batches(zip_file.iter_jsonl(), batch_size=batch_size)):
        # pandas dataframe makes data transformation easier
        batch_df = pandas.DataFrame(batch)
        # get boolean mask of duplicated datapoints
        dupmask = get_duplicate_mask(batch_df)

        # duplication stats
        abs_dup = dupmask.sum()
        # last batch may be smaller than batch_size
        this_batch_size = len(dupmask)
        dup_ratio = abs_dup / this_batch_size
        console.debug("batch #{} duplication ratio {:.4f} ({}/{})".format(batch_id, dup_ratio, abs_dup, this_batch_size))

        # reduce deeppavlov payload size by removing duplicates
        unique_datapoints = batch_df[~dupmask]
        # tag texts with DeepPavlov (multilingual BERT) NER model
        y_hat = tag_with_mult_bert(list(unique_datapoints.text))
        # get place candidates using allowed tags
        places = extract_place_candidates(y_hat, allowed_tags)

        # extend unique datapoints with places candidates (required by Geocode steps)
        unique_datapoints_index = unique_datapoints.index
        unique_datapoints.loc[unique_datapoints_index, "places"] = [tagged for index, tagged in places.items()]
        # remove place candidates from text
        unique_datapoints.loc[unique_datapoints_index, "text_clean"] = unique_datapoints.apply(normalize_places, axis=1)
        # apply natural text transformations on place-free text (required by Annotation steps)
        unique_datapoints.loc[unique_datapoints_index, "text_clean"] = unique_datapoints.text_clean.apply(apply_transformations)

        # merge transformed unique datapoints onto duplicates
        # drop target columns to avoid pandas suffix patching (i.e. <col>_x, <col>_y)
        duplicates = batch_df[dupmask].drop(columns=["places", "text_clean"])
        enriched_duplicates = duplicates.merge(unique_datapoints[["places", "text", "text_clean"]], on="text")
        batch_transformed = pandas.concat([unique_datapoints, duplicates]).reset_index(drop=True)
        # ndjson batch
        yield batch_transformed.to_json(orient="records", force_ascii=False, lines=True)


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

    # ad hoc logic to transform unique datapoint only and update their duplicates
    ndjson_batches = make_ndjson_batches(zip_file, allowed_tags, batch_size=args.batch_size)

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
