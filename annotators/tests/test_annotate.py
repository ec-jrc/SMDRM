import logging
import os
import time
import libdrm.pipeline


root = os.path.join(os.path.dirname(os.path.abspath(__file__)))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Integration/Performance tests for annotators.")
    parser.add_argument("--batch-size", default=1000, help="The data points in each batch. Default is %(default)s.")
    parser.add_argument("--data", default=os.path.join(root, "cid_1210_dp_5000.zip"), help="The data to test with. Default is %(default)s.")
    parser.add_argument("--url", required=True, help="The Annotator API URL for which to run the tests.")
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=logging.INFO,
    )
    console = logging.getLogger("annotators.perftests")

    # data pipeline steps
    steps = [
        libdrm.pipeline.ZipFilesToJSONFiles(),
        libdrm.pipeline.JSONFilesToJSONLines(),
        libdrm.pipeline.LegacyJSONLinesParser(),
        libdrm.pipeline.JSONLinesToDataPoints(deserialize=True),
        libdrm.pipeline.InBatches(batch_size=args.batch_size),
        libdrm.pipeline.AnnotateInBatches(args.url)
    ]
    # build pipeline
    data_pipeline = libdrm.pipeline.Pipeline([args.data], steps).build()
    # run integration/performance test
    console.info("Performance test: {}".format(args.url))
    t_start = time.time()
    for _ in data_pipeline:
        continue
    t_end = time.time() - t_start
    console.info("Completed in {:.2f}s".format(t_end))
