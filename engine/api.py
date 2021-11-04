from flask import Flask, request
from flask_restful import Resource, Api
import os
import typing

import libdrm.apis
import libdrm.elastic
import libdrm.pipeline
import libdrm.schemas


# api info
NAME = "EngineAPI"
app = Flask(NAME)
api = Api(app)


def parse_extra_annotation_steps_from_meta(metadata: dict) -> typing.Iterable:
    """Yield only annotation steps communicated by the user via *_annotator flag in metadata."""
    lookup = libdrm.apis.get_annotators_lookup()
    for annotator, endpoint in lookup.items():
        enabled = metadata.get(annotator, False)
        if not enabled:
            console.warning("{} annotator not found in metadata.".format(annotator))
            continue
        yield libdrm.pipeline.AnnotateInBatches(endpoint)


class EngineAPI(Resource):

    def get(self):
        return {"api_name": NAME, "resource": "/", "is_alive": True}, 200

    def post(self):
        metadata = request.get_json()
        # metadata contains the annotations to enable as csv string
        console.info("Metadata received: {}".format(metadata))
        # make pipeline
        input_files = [os.path.join(uploads_path, metadata["filename"])]
        # data pipeline steps to be extended with user metadata
        steps = [
            libdrm.pipeline.ZipFilesToJSONFiles(),
            libdrm.pipeline.JSONFilesToJSONLines(),
            libdrm.pipeline.LegacyJSONLinesParser(),
            libdrm.pipeline.JSONLinesToDataPoints(deserialize=True),
            libdrm.pipeline.InBatches(batch_size=args.batch_size),
        ]
        # add annotation steps using metadata
        steps.extend([step for step in parse_extra_annotation_steps_from_meta(metadata)])
        console.info("Pipeline steps: {}".format(steps))
        # build the pipeline to iterate batches of annotated data points from zip files (according to the given steps)
        annotated_data_points_in_batches = libdrm.pipeline.Pipeline(input_files, steps).build()
        # add elasticsearch caching step
        caching_step = libdrm.pipeline.BatchesToElasticSearch(client=es)
        # caching annotated batches to elasticsearch
        batch_num = 0
        for batch, response in caching_step.logic(annotated_data_points_in_batches):
            console.debug("Cached batch: {}".format(batch))
            console.debug(response)
            batch_num += 1
        return {"status": "processed", "batches": batch_num}, 201


# add API resources
api.add_resource(EngineAPI, "/")


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Engine API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address. Default is %(default)s.")
    parser.add_argument("--port", default=5555, help="The host port. Default is %(default)s.")
    parser.add_argument("--batch-size", default=100, help="The data points in each batch. Default is %(default)s.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging. Default is %(default)s.")
    args = parser.parse_args()

    # mounted filesystem
    uploads_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=os.getenv("LOG_LEVEL", "INFO")
    )
    console = logging.getLogger("engine.api")
    logging.getLogger("werkzeug").propagate = False

    # check status of required APIs
    libdrm.apis.check_statuses()

    # create elasticsearch index
    es = libdrm.elastic.ElasticSearchClient("http://elasticsearch:9200")
    es.create_index()

    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
