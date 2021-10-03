# -*- coding: utf-8 -*-

"""
Uploader API awaits for a HTTP request with JSON formatted content, and a disaster type.

Examples:
    curl -v -F "file=@/home/ep/Downloads/fires/test_fires.zip" http://localhost:5000/upload/zip
    curl -v -H "Content-Type: application/json" -d '{"created_at":"Sat May 15 14:25:35 +0000 2021", "id":"1", "text":"A text information.", "lang":"en", "disaster_type":"floods"}' http://localhost:5000/upload/event

The uploaded content is validate and its content stored into a Docker Volume.
For more info, see the Dockerfile in the directory of this Python file.
"""

from flask import Flask, request
from flask_restful import Resource, Api, reqparse, abort
import pathlib
import werkzeug

from libdrm import (
    datamodels,
    nicelogging,
)

# current directory
root = pathlib.Path(__file__).resolve().parent

# api info
name = "UploaderAPI"
app = Flask(name)
api = Api(app)

# filesystem
data_dir = root / "data"
data_dir.mkdir(parents=True, exist_ok=True)

# loggers
file_log = nicelogging.file_logger("uploads", data_dir)
console = nicelogging.console_logger("uploader.api")


class UploaderAPI(Resource):
    def get(self):
        response = {
            "api_name": name,
            "resources": ["/", "/upload"],
            "is_alive": True,
            "usage": "add usage",
        }
        console.debug(response)
        return response, 200


class EventUploaderAPI(Resource):
    def get(self):
        response = {"api_name": name, "resource": "/upload/event", "is_alive": True}
        console.debug(response)
        return response, 200

    def post(self):
        upload_data = request.get_json()
        errors = datamodels.schemas.DisasterSchema().validate(upload_data)
        if errors:
            console.error(errors)
            abort(404, message=errors)
        # parse data as per schema
        data = datamodels.disaster.DisasterModel.serialize_from_dict(upload_data)
        file_log.info(data.deserialize_to_dict())
        response = {"uploaded": True, "type": "json", "status_code": 201}
        console.info(response)
        return response, 201


class ZipFileUploaderAPI(Resource):
    def get(self):
        response = {"api_name": name, "resource": "/upload/zip", "is_alive": True}
        console.debug(response)
        return response, 200

    def post(self):
        parse = reqparse.RequestParser()
        parse.add_argument(
            "file", type=werkzeug.datastructures.FileStorage, location="files"
        )
        req_args = parse.parse_args()
        file = req_args["file"]
        # validate uploaded form data
        errors = datamodels.schemas.ZipFileUploadSchema().validate({"upload_file": file})
        if errors:
            console.error(errors)
            abort(404, message=errors)
        # cache file if passes validation
        file.save(data_dir / file.filename)
        file.close()
        response = {"uploaded": True, "type": "zip", "filename": file.filename, "status_code": 201}
        console.info(response)
        return response, 201


# add API resources
api.add_resource(UploaderAPI, "/", "/upload")
api.add_resource(EventUploaderAPI, "/upload/event")
api.add_resource(ZipFileUploaderAPI, "/upload/zip")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="FileUploader API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5000, help="The host port.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debugging."
    )
    args = parser.parse_args()
    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
