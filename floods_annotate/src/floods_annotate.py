import click
import logging
import os
import pandas
import requests
import sys
import typing as t

from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.common import iter_in_batches


# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger(__name__)

# development flag
development = bool(int(os.getenv("DEVELOPMENT", 0)))

# build floods url
host = "localhost" if development else "floods"
port = 5001
base_url = "http://{host}:{port}".format(host=host, port=port)

# typing
pandas_groupby = pandas.core.groupby.generic.DataFrameGroupBy

def get_languages() -> requests.Response:
    """Floods Named Entity Recognition REST API call to get the list of languages enabled for annotation."""
    url = base_url+"/model/languages"
    r = requests.get(url)
    return r.json()


def annotate(texts: list, lang: str) -> requests.Response:
    """Floods Named Entity Recognition REST API call to annotate a list of texts."""
    url = base_url+"/model/annotate/"+lang
    r = requests.post(url, json={"texts": texts})
    return r.json()


def group_batch_by_language(batch: t.List[dict], languages: t.List[str]) -> pandas_groupby:
    # transform to DataFrame
    batch_df = pandas.DataFrame(batch)
    # a temp field with a normalized version of the lang field
    # as we developed a multilingual embeddings, we can vectorize any language if comes as "ml"
    lang_tmp = batch_df.lang.apply(lambda lang: lang if lang in languages else "ml")
    # group df by (normalized) language
    groups = batch_df.groupby(lang_tmp)
    return groups


def get_cnn_texts_from_group(g: pandas.DataFrame) -> t.List[str]:
    # get texts prepared for CNN from DataFrame
    cnn_texts = g.text_clean.values.tolist()
    if not cnn_texts:
        msg = "`text_clean` field not found. Make sure you use data that passed the transform_tweets task."
        console.warning(msg)
        raise ValueError(msg)

    return cnn_texts


def annotate_language_groups(groups: pandas_groupby) -> t.Iterable[dict]:
    """Annotate batch by groups of texts of same language."""
    for lang, g in groups:
        # get texts of same language as list
        texts = get_cnn_texts_from_group(g)
        # annotate texts by language and add to the group
        g["floods_proba"] = annotate(texts, lang)
        # return annotated group
        yield g


@click.command()
@click.argument("input_path", type=click.Path(exists=True, file_okay=True, dir_okay=False, resolve_path=True))
@click.option("--output-path", type=click.Path(exists=False, file_okay=True, dir_okay=False, resolve_path=True), help="The path to which you want to save the task output.")
@click.option("--batch-size", type=click.INT, default=1000, help="The size of each batch in which a file is split.")
@click.option("--debug", is_flag=True, default=False, help="Enables debugging mode.")
def cli(input_path, output_path, batch_size, debug):
    """
    Annotate `text` data with Named Entity Recognition algorithms.

    Arguments\n
      input_path: The path from which you want to get input data,\n

    Exit Codes\n
      1: Invalid zip file

    """

    if debug:
        console.setLevel(logging.DEBUG)

    # input path validation
    zip_file = ZipFileModel(input_path)
    if not zip_file.is_valid():
        console.error("{} is not a zip file.".format(input_path))
        sys.exit(1)

    def gen_data():
        console.info("floods_annotate step - batch size={}...".format(batch_size))
        n_in = 0
        n_out = 0
        n_batches = 0

        # api call to get the list of annotation-ready languages
        languages = get_languages()

        for batch in iter_in_batches(zip_file.iter_jsonl(), batch_size=batch_size):
            n_batches += 1
            n_in += len(batch)

            # make groups of texts by language
            groups = group_batch_by_language(batch, languages)
            # iter annotate groups
            for annotated in annotate_language_groups(groups):
                console.debug(annotated)
                n_out += len(annotated)
                yield annotated.to_json(orient="records", force_ascii=False, lines=True)

        # metrics
        console.info("input   = {}".format(n_in))
        console.info("output  = {}".format(n_out))
        console.info("batches = {}".format(n_batches))

    # cache pipeline output
    if not output_path:
        output_path = input_path.replace(".zip", "_ann.zip")
    zip_file.cache(output_path, gen_data())


if __name__ == "__main__":
    cli()
