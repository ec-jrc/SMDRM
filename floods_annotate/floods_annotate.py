import logging
import os
import pandas
import requests
import sys
import typing

from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.common import iter_in_batches, get_version, path_arg, log_execution


# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("floods_annotate")

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


def group_batch_by_language(batch: typing.List[dict], languages: typing.List[str]) -> pandas_groupby:
    # transform to DataFrame
    batch_df = pandas.DataFrame(batch)
    # a temp field with a normalized version of the lang field
    # as we developed a multilingual embeddings, we can vectorize any language if comes as "ml"
    lang_tmp = batch_df.lang.apply(lambda lang: lang if lang in languages else "ml")
    # group df by (normalized) language
    groups = batch_df.groupby(lang_tmp)
    return groups


def get_cnn_texts_from_group(g: pandas.DataFrame) -> typing.List[str]:
    # get texts prepared for CNN from DataFrame
    cnn_texts = g.text_clean.values.tolist()
    if not cnn_texts:
        msg = "`text_clean` field not found. Make sure you use data that passed the transform_tweets task."
        console.warning(msg)
        raise ValueError(msg)

    return cnn_texts


def annotate_language_groups(groups: pandas_groupby) -> typing.Iterable[dict]:
    """Annotate batch by groups of texts of same language."""
    for lang, g in groups:
        # get texts of same language as list
        texts = get_cnn_texts_from_group(g)
        # annotate texts by language and add to the group
        g["floods_proba"] = annotate(texts, lang)
        # return annotated group
        yield g


def make_ndjson_batches(
    zip_file: typing.Type[ZipFileModel], batch_size: int = 1000
) -> typing.Iterable[str]:
    """Iterate NDJSON batches from a generator of JSON datapoints.
    It implements an ad hoc logic to annotate datapoints grouped by language."""
    # api call to get the list of annotation-ready languages
    languages = get_languages()

    for batch in iter_in_batches(zip_file.iter_jsonl(), batch_size=batch_size):
        # make groups of texts by language
        groups = group_batch_by_language(batch, languages)
        # iter annotate groups
        for annotated in annotate_language_groups(groups):
            console.debug(annotated)
            yield annotated.to_json(orient="records", force_ascii=False, lines=True)


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
        console.error("Not a valid zip file.")
        sys.exit(13)

    # ad hoc logic to annotate datapoints grouped by language
    ndjson_batches = make_ndjson_batches(zip_file, batch_size=args.batch_size)

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
