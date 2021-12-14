import click
import logging
import os
import sys
import typing as t

from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches

from .transformations import (
    tag_with_mult_bert,
    extract_place_candidates,
    normalize_places,
    apply_transformations,
)


@click.command()
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--output-path", type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--batch-size", type=click.INT, default=100, help="The size of each batch in which a file is split.")
@click.option("--debug", is_flag=True, default=False, help="Enables debugging mode.")
def cli(input_path, output_path, batch_size, debug):
    """
    Transform data point `text` field.

    Arguments\n
      input_path: The path from which you want to get input data,\n

    Options\n
      --output-path: The path to which you want to save the task output.\n
      --batch-size: bla,\n
      --debug: bla.

    Exit Codes\n
      1: Invalid zip file,\n

    """
    # setup logging
    logging.basicConfig(level="DEBUG" if debug else "INFO")
    console = logging.getLogger(__name__)

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
            # isolate texts
            texts = [datapoint["text"] for datapoint in batch]
            # # deeppavlov model output: tagged and tokenized sentences
            y_hat = tag_with_mult_bert(texts)
            # places
            places = extract_place_candidates(y_hat, allowed_tags)
            # normalize places found in texts
            normalized = normalize_places(texts, places)
            # update datapoint in batch
            for datapoint, ntext, pnames in zip(batch, normalized, places):
                # apply natural text transformations
                # store in batch (required by Annotation steps)
                datapoint["text_clean"] = apply_transformations(ntext)
                # store places in batch (required by Geocode step)
                datapoint["places"] = pnames
                yield datapoint
                n_out += 1
        # metrics
        console.info("input   = {}".format(n_in))
        console.info("output  = {}".format(n_out))
        console.info("batches = {}".format(n_batches))

    # cache pipeline output
    if not output_path:
        output_path = input_path.replace(".zip", "_tra.zip")
    zip_file.cache(output_path, gen_data(), batch_size=batch_size)


if __name__ == "__main__":
    cli()
