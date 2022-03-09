import glob
import logging
import os
import json
import requests
from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches, log_execution

# setup root dir
root_dir = os.path.dirname(os.path.abspath(__file__))


def annotate(annotator, texts: list, lang: str = None) -> requests.Response:
    """Get annotation payload from API endpoint of given annotator."""
    headers = {
        "accept": "application/json",
        "Content-Type": "application/json",
    }
    endpoint = "model/annotate"
    if annotator in ("floods",):
        # floods annotator is language dependent
        endpoint += "/{lang}".format(lang=lang)
    url = "http://{host}:{port}/{endpoint}".format(
        host=annotator, port=5000, endpoint=endpoint
    )
    return requests.post(url, headers=headers, data=json.dumps({"texts": texts}))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(
        description="Integration/Performance tests for Annotation APIs."
    )
    parser.add_argument(
        "--annotator",
        required=True,
        choices=[
            "deeppavlov",
            "floods",
        ],
        help="The Annotator API URL for which to run the tests.",
    )
    parser.add_argument(
        "--batch-size",
        default=100,
        type=int,
        help="The number of data points in each batch. Default is %(default)s.",
    )
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debugging. Default is %(default)s.",
    )
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    console = logging.getLogger("annotators.perftests")

    @log_execution(console)
    def run_perftest(path):
        zip_file = ZipFileModel(path)
        console.debug("Is valid zip file? {}".format(zip_file.is_valid()))
        # get dataset language i.e. first 2 chars of filename
        lang = os.path.basename(path)[:2]
        for index, batch in enumerate(
            iter_in_batches(zip_file.iter_jsonl(), batch_size=args.batch_size)
        ):
            console.debug("processing batch #{}".format(index))
            texts = [d["text"] for d in batch]
            annotate(args.annotator, texts, lang).raise_for_status()

    console.info("Running performance test")
    console.debug("config={}".format(vars(args)))

    # get filepaths
    paths = glob.iglob(os.path.join(root_dir, "data/*.zip"))
    for path in paths:
        console.info("processing {}".format(path))
        run_perftest(path)
