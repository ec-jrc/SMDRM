# -*- coding: utf-8 -*-

from flask import Flask, request
from flask_restful import Resource, Api

from src import (
    annotator,
    text_sanitizer,
)

from libdrm import datamodels, nicelogging

console = nicelogging.console_logger("smdrm.floods.api")

name = "FloodsAPI"
app = Flask(name)
api = Api(app)

# preload models at initialization
preloaded = {}
available_languages = annotator.FloodsAnnotator.available_languages()
for lang in available_languages:
    print("preloading", lang)
    preloaded[lang] = annotator.FloodsAnnotator(lang=lang)


class FloodsAPI(Resource):

    def get(self):
        return {"api_name": name, "is_alive": True}, 200

    def post(self):
        disaster_event = datamodels.DisasterEventModel.from_dict(request.get_json())
        # sanitize text
        disaster_event.sanitize_text(text_sanitizer.sanitize)
        # annotate text
        disaster_event.annotate_text(preloaded[disaster_event.lang].infer)
        # json response
        response = disaster_event.to_dict()
        console.debug(response)
        return response, 201


api.add_resource(FloodsAPI, "/", "/annotate")


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(description="Floods API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5000, help="The host port.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging.")
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
