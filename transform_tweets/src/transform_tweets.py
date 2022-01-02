import click
import logging
import os
import pandas
import typing
import sys

from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches

from .transformations import (
    tag_with_mult_bert,
    extract_place_candidates,
    normalize_places,
    get_duplicate_mask,
    apply_transformations,
)

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)


@click.command()
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--output-path", type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True), help="The path to which you want to save the task output.")
@click.option("--batch-size", type=click.INT, default=100, help="The size of each batch in which a file is split.")
@click.option("--debug", is_flag=True, default=False, help="Enables debugging mode.")
def cli(input_path, output_path, batch_size, debug):
    """
    Transform data point `text` field.

    Arguments\n
      input_path: The path from which you want to get input data,\n

    Exit Codes\n
      1: Invalid zip file,\n

    """

    if debug:
        console.setLevel(logging.DEBUG)

    # input path validation
    zip_file = ZipFileModel(input_path)
    if not zip_file.is_valid():
        console.error("{} is not a zip file.".format(input_path))
        sys.exit(1)

    # DeepPavlov NER algorithm uses prefixes to indicate B-egin,
    # and I-nside relative positions of tokens. For more details, visit
    # http://docs.deeppavlov.ai/en/master/features/models/ner.html#ner-task.
    allowed_tags = ["B-GPE", "I-GPE", "B-FAC", "I-FAC", "B-LOC", "I-LOC"]
    console.info("Allowed NER tags={}".format(allowed_tags))

    def gen_data():
        console.info("transform_tweets step - batch size={}...".format(batch_size))
        n_in = 0
        n_out = 0
        n_batches = 0

        for batch in iter_in_batches(zip_file.iter_jsonl(), batch_size=batch_size):
            n_batches += 1
            n_in += len(batch)

            # pandas dataframe makes data transformation easier
            batch_df = pandas.DataFrame(batch)
            # get boolean mask of duplicated datapoints
            dupmask = get_duplicate_mask(batch_df)

            # duplication stats
            abs_dup = dupmask.sum()
            dup_ratio = abs_dup / n_in
            console.debug("batch #{} duplication ratio {:.4f} ({}/{})".format(n_batches, dup_ratio, abs_dup, n_in))

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
            n_out += len(batch_transformed)
            yield batch_transformed.to_json(orient="records", force_ascii=False, lines=True)

        # metrics
        console.info("input   = {}".format(n_in))
        console.info("output  = {}".format(n_out))
        console.info("batches = {}".format(n_batches))

    # cache pipeline output
    if not output_path:
        output_path = input_path.replace(".zip", "_tra.zip")
    zip_file.cache(output_path, gen_data())


if __name__ == "__main__":
    cli()
