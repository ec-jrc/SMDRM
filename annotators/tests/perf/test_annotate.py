import glog
import logging
import os
import json
import requests
from libdrm.datamodels import ZipFileModel
from libdrm.common import iter_in_batches, log_execution

# setup root dir
root_dir = os.path.dirname(os.path.abspath(__file__))


# TODO: normalize interface between floods, fires, and deeppavlov annotators
def tag_with_mult_bert(url, texts: list) -> requests.Response:
    headers = {
        'accept': 'application/json',
        'Content-Type': 'application/json',
    }
    r = requests.post(url, headers=headers, data=json.dumps({"x": texts}))
    return r


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Integration/Performance tests for Annotation APIs.")
    parser.add_argument("--annotator-url", required=True, help="The Annotator API URL for which to run the tests.")
    parser.add_argument("--batch-size", default=100, type=int, help="The number of data points in each batch. Default is %(default)s.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging. Default is %(default)s.")
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    console = logging.getLogger("annotators.perftests")

    @log_execution(console)
    def run_perftest(path):
        zip_file = ZipFileModel(path)
        console.debug("Is valid zip file? {}".format(zip_file.is_valid()))
        url = args.annotator_url
        for index, batch in enumerate(iter_in_batches(zip_file.iter_jsonl(), batch_size=args.batch_size)):
            console.debug("processing batch #{}".format(index))
            texts = [d["text"] for d in batch]
            resp = tag_with_mult_bert(url, texts)
            resp.raise_for_status()

    console.info("Running performance test")
    console.debug("config={}".format(vars(args)))

    # get filepaths
    paths = glob.iglob(os.path.join(root_dir, 'data/*.zip'))
    for path in paths:
        console.info("processing {}".format(path))
        run_perftest(path)
