from flask import Flask, request
from flask_restful import Resource, Api
import logging
import os

from src import (
    annotator,
    batches,
    text_sanitizer,
)


NAME = "FloodsAPI"
app = Flask(NAME)
api = Api(app)

# preload models at initialization
preloaded = {}
available_languages = annotator.FloodsAnnotator.available_languages()
for lang in available_languages:
    preloaded[lang] = annotator.FloodsAnnotator(lang=lang)


class FloodsAPI(Resource):
    def get(self):
        response = {"api_name": NAME, "resource": "/", "is_alive": True}
        console.debug(response)
        return response, 200

    def post(self):
        payload = request.get_json()
        batch = payload["batch"]
        # group data points by language
        by_lang = batches.data_points_by_lang(batch, available_languages)
        # annotate batch and and merge with original batch
        annotated_batch = batches.add_annotations_to_batch(
            batches.annotate_batch(
                batches.iter_array_of_data_points(by_lang),
                text_sanitizer.sanitize,
                preloaded,
            ), by_lang)
        # return payload in the same format as received i.e., {"batch": [{}, {}, ...]}
        response = {"batch": [annotated_data_point for annotated_data_point in annotated_batch]}
        console.info(response)
        return response, 201


api.add_resource(FloodsAPI, "/", "/annotate")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Floods API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5001, help="The host port.")
    parser.add_argument(
        "--debug",
        action="store_true",
        default=False,
        help="Enable debugging. Default is %(default)s.",
    )
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=os.getenv("LOG_LEVEL", "INFO"),
    )
    console = logging.getLogger("floods.api")

    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
