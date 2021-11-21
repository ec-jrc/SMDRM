from flask import Flask, request
from flask_restful import Resource, Api, abort
import logging
import os
import annotator

NAME = "FiresAPI"
app = Flask(NAME)
api = Api(app)


# preload model at initialization
model = annotator.FiresAnnotator()


class FiresAPI(Resource):

    def get(self):
        """API status."""
        return {"api_name": NAME, "resources": ["/", "/annotate"], "is_alive": True}, 200

    def post(self):
        """Annotate batch of texts of a specific language.
        Input:
            JSON formatted payload
            {"batch" {"lang": str, "texts": List[str]}}
        Returns:
            API response with extra field holding the computed probability scores."""
        batch = request.json.get("batch", {})
        if not batch:
            msg = "Invalid/missing input payload."
            console.error(msg)
            abort(400, message=msg)
        if "texts" not in batch:
            msg = "Missing input texts."
            console.error(msg)
            abort(400, message=msg)
        # infer probability scores
        probability_scores = model.infer(batch["texts"])
        # add scores to payload as valid JSON format
        batch["annotation_probs"] = ["{:.6f}".format(round(s, 6)) for s in probability_scores]
        batch["annotation_type"] = "fires"
        response = {"batch": batch}
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
    logging.getLogger("werkzeug").propagate = False

    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
