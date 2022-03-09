import logging
import os
import pandas
import requests
import sys
import typing

from libdrm.common import iter_in_batches, get_version, path_arg, log_execution
from libdrm.datamodels import DataPointModel, ZipFileModel
from libdrm.pipelines import Pipeline

# setup logging
logging.basicConfig(level=logging.INFO)
console = logging.getLogger("floods_annotate")

# API url from within the (default) Docker networks created with docker-compose
base_url = "http://{host}:{port}/".format(host="floods", port=5000)

# typing
pandas_groupby = pandas.core.groupby.generic.DataFrameGroupBy


def get_languages() -> typing.List[str]:
    """Floods Named Entity Recognition REST API call to get the list of languages enabled for annotation."""
    return requests.get(base_url + "model/languages").json()


def get_annotation_scores(texts: list, lang: str) -> typing.List[str]:
    """Floods Named Entity Recognition REST API call to annotate a list of texts."""
    return requests.post(
        base_url + "model/annotate/" + lang, json={"texts": texts}
    ).json()


def group_batch_by_language(
    datapoints_batch: pandas.DataFrame, languages: typing.List[str]
) -> pandas_groupby:
    # a temp field with a normalized version of the lang field
    # as we developed a multilingual embeddings, we can vectorize any language if comes as "ml"
    lang_tmp = datapoints_batch.lang.apply(
        lambda lang: lang if lang in languages else "ml"
    )
    # group df by (normalized) language
    return datapoints_batch.groupby(lang_tmp)


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
        scores = get_annotation_scores(texts, lang)
        g["annotation"] = [dict(floods=score) for score in scores]
        # return annotated group
        yield g


def convert_to_dataframe(
    datapoints_batches: typing.Iterable[list],
) -> typing.Iterable[pandas.DataFrame]:
    """Converts datapoints batches i.e. list of JSON into Pandas DataFrame."""
    for datapoints_batch in datapoints_batches:
        yield pandas.DataFrame(datapoints_batch)


def task_metrics(
    datapoints_batches: typing.Iterable[pandas.DataFrame],
) -> typing.Iterable[pandas.DataFrame]:
    """Compute task metrics."""
    batches = 0
    annotated = 0
    for datapoints_batch in datapoints_batches:
        batches += 1
        annotated += len(datapoints_batch)
        yield datapoints_batch
    console.info(dict(batches=batches, annotated=annotated))


def log_datapoints(
    datapoints_batches: typing.Iterable[pandas.DataFrame],
) -> typing.Iterable[pandas.DataFrame]:
    """Log datapoints to console."""
    for batch_id, datapoints_batch in enumerate(datapoints_batches, start=1):
        console.debug(
            "processing datapoints batch ID #{}... Below, a sample of 5.".format(
                batch_id
            )
        )
        console.debug(datapoints_batch.head(5))
        yield datapoints_batch


def annotate_batches(
    datapoints_batches: typing.Iterable[pandas.DataFrame],
) -> typing.Iterable[pandas.DataFrame]:
    """Annotate datapoints batches dataframe by language group."""
    # api call to get the list of annotation-ready languages
    languages = get_languages()

    for datapoints_batch in datapoints_batches:
        # make groups of texts by language
        groups = group_batch_by_language(datapoints_batch, languages)
        # iter annotate groups
        yield from annotate_language_groups(groups)


def make_ndjson_batches(
    datapoints_batches: typing.Iterable[pandas.DataFrame],
) -> typing.Iterable[pandas.DataFrame]:
    for datapoints_batch in datapoints_batches:
        yield datapoints_batch.to_json(orient="records", force_ascii=False, lines=True)


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
    annotate_pipeline.add(convert_to_dataframe)
    annotate_pipeline.add(annotate_batches)
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
    parser.add_argument("--debug", action="store_true", default=False)
    parser.add_argument(
        "--version",
        action="version",
        version=get_version(os.path.join(os.path.dirname(__file__), "VERSION.txt")),
    )
    # run task
    run(parser.parse_args())
