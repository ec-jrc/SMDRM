from flask import Flask, request
from flask_restful import Resource, Api

from src import (
    annotator,
    batch,
    text_sanitizer,
)


name = "FloodsAPI"
app = Flask(name)
api = Api(app)

# preload models at initialization
preloaded = {}
available_languages = annotator.FloodsAnnotator.available_languages()
for lang in available_languages:
    preloaded[lang] = annotator.FloodsAnnotator(lang=lang)


class FloodsAPI(Resource):
    def get(self):
        return {"api_name": name, "is_alive": True}, 200

    def post(self):
        response = batch.batch_annotate(request.get_json(), text_sanitizer.sanitize, preloaded, available_languages)
        return response, 201


api.add_resource(FloodsAPI, "/", "/annotate")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Floods API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5001, help="The host port.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debugging."
    )
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
