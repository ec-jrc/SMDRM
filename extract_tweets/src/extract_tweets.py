import click
import logging
import sys
import typing as t

from libdrm.datamodels import DataPointModel, ZipFileModel


def extend_text_field(data: dict) -> str:
    """Extend text of original tweet with nested search."""
    try:
        text = data['retweeted_status']['extended_tweet']['full_text']
    except:
        # Try for extended text of an original tweet, if RT'd (REST API)
        try:
            text = data['retweeted_status']['full_text']
        except:
            # Try for extended text of an original tweet (streamer)
            try:
                text = data['extended_tweet']['full_text']
            except:
                # Try for extended text of an original tweet (REST API)
                try:
                    text = data['full_text']
                except:
                    # Try for basic text of original tweet if RT'd
                    try:
                        text = data['retweeted_status']['text']
                    except:
                        # Try for basic text of an original tweet
                        try:
                            text = data['text']
                        except:
                            # Nothing left to check for
                            text = ''
    return text


@click.command()
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--output-path", type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--batch-size", type=click.INT, default=1000, help="The size of each batch in which a file is split.")
@click.option("--debug", is_flag=True, default=False, help="Enables debugging mode.")
def cli(input_path, output_path, batch_size, debug):
    """
    It minimizes the memory consumption footprint by removing unnecessary data.

    Arguments\n
      input_path: The path from which you want to get input data,\n

    Options\n
      --output-path: The path to which you want to save the task output.\n
      --batch-size: bla,\n
      --debug: bla,\n

    Exit Codes\n
      1: Invalid zip file

    """
    # setup logging
    logging.basicConfig(level="DEBUG" if debug else "INFO")
    console = logging.getLogger(__name__)

    # input path validation
    zip_file = ZipFileModel(input_path)
    if not zip_file.is_valid():
        console.error("{} is not a zip file.".format(input_path))
        sys.exit(1)

    def gen_data():
        console.info("extract_tweets step - batch size={}...".format(batch_size))
        n_in = 0
        n_out = 0

        for jsonl in zip_file.iter_jsonl():
            n_in += 1

            if not jsonl:
                console.debug("Invalid JSON.")
                continue

            # get raw tweet if exists
            jsonl = jsonl.get('tweet', jsonl)
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
            n_out += 1

        # metrics
        console.info("input: {}".format(n_in))
        console.info("output: {}".format(n_out))

    # cache pipeline output
    if not output_path:
        output_path = input_path.replace(".zip", "_ext.zip")
    zip_file.cache(output_path, gen_data(), batch_size=batch_size)


if __name__ == "__main__":
    cli()
