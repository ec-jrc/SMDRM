"""
Text Normalize API normalizes JSON formatted content of HTTP POST requests that contain a batch of raw texts

Examples
    curl -v -X POST http://localhost:5050 \
        -H "Content-Type: application/json" \
        -d '{"batch": ["RT a text string, to be normalized @API #NothingSpecial https://example.com http"]}'
    Returns:
    {
        "text_normalized": [
            "a text string to be sanitized nothingspecial url"
        ]
    }
"""

from flask import Flask, request
from flask_restful import Resource, Api, abort
import os
import normalizer


# api info
NAME = "TextNormalizeAPI"
app = Flask(NAME)
api = Api(app)


class TextNormalizeAPI(Resource):

    def get(self):
        return {"api_name": NAME, "resources": ["/", "/normalize"], "is_alive": True}, 200

    def post(self):
        # batch of texts in format {"batch": ["Text1", "Text2", ...]}
        texts = request.json.get("batch", None)
        if not texts:
            msg = "Missing batch payload."
            console.error(msg)
            abort(400, message=msg)
        return {"text_normalized": normalizer.batch_normalize(texts)}, 201


# add API resources
api.add_resource(TextNormalizeAPI, "/", "/normalize")


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Text Normalize API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address. Default is %(default)s.")
    parser.add_argument("--port", default=5050, help="The host port. Default is %(default)s.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging. Default is %(default)s.")
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=os.getenv("LOG_LEVEL", "INFO")
    )
    console = logging.getLogger("transformers.text_normalize.api")
    logging.getLogger("werkzeug").propagate = False
    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
