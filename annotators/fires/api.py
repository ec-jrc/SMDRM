import pandas
from flask import Flask, request
from flask_restful import Resource, Api
import logging
import os

from src import (
    annotator,
    text_sanitizer,
)


NAME = "FiresAPI"
app = Flask(NAME)
api = Api(app)


# preload model at initialization
model = annotator.FiresAnnotator()


def update_annotations(batch: pandas.DataFrame) -> pandas.DataFrame:
    """Pandas DataFrame helper to append annotated data points to dedicated `annotations` field."""
    batch.annotations.append(
        {
            "annotation_type": "fires",
            "annotation_prob": batch.annotation_prob,
            "sanitized_text": batch.sanitized_text
        }
    )
    # with updated annotations
    return batch


class FiresAPI(Resource):
    def get(self):
        return {"api_name": NAME, "resource": "/", "is_alive": True}, 200

    def post(self):
        payload = request.get_json()
        # as dataframe to take advantage of vectorization
        batch_df = pandas.DataFrame(payload["batch"])
        # sanitize and annotate the batch
        batch_df["sanitized_text"] = sanitized_text = text_sanitizer.sanitize(batch_df.text)
        batch_df["annotation_prob"] = model.infer(sanitized_text)
        # append enrich annotation fields to annotations field for each data point in batch
        annotated_batch_df = batch_df.apply(update_annotations, axis=1)
        annotated_batch_df.drop(columns=["sanitized_text", "annotation_prob"], inplace=True)
        # convert to JSON
        annotated_batch = [annotated_data_point for _, annotated_data_point in annotated_batch_df.T.to_dict().items()]
        # return payload in the same format as received i.e., {"batch": [{}, {}, ...]}
        response = {"batch": annotated_batch}
        console.debug(response)
        return response, 201


api.add_resource(FiresAPI, "/", "/annotate")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Fires API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5002, help="The host port.")
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
    console = logging.getLogger("fires.api")

    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
