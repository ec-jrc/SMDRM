"""
Uploader API awaits for a HTTP request with JSON formatted content, and a disaster type.

Examples:
    curl -v -F "file=@/home/ep/Downloads/fires/test_fires.zip" http://localhost:5000/upload/zip

The uploaded content is validate and its content stored into a Docker Volume.
For more info, see the Dockerfile in the directory of this Python file.
"""

from flask import Flask, request
from flask_restful import Resource, Api, abort
import os
import requests
import werkzeug
import libdrm.apis
import libdrm.schemas


# uploads filesystem
UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# api info
NAME = "UploadAPI"
app = Flask(NAME)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1000 * 1000
api = Api(app)

# upload schemas
zip_file_schema = libdrm.schemas.ZipFileUploadSchema()
metadata_schema = libdrm.schemas.MetadataUploadSchema()

# communicate successful upload
engine_endpoint = "http://engine:5555"


class ZipFileUploaderAPI(Resource):

    def get(self):
        return {"api_name": NAME, "resource": "/upload", "is_alive": True}, 200

    def post(self):
        # schema validation of upload metadata header
        meta_errors = metadata_schema.validate(request.form)
        if meta_errors:
            console.error(meta_errors)
            abort(404, message=meta_errors)
        # metadata for engine API
        meta = metadata_schema.load(request.form)

        # schema validation of zip file upload form
        zip_file_errors = zip_file_schema.validate(request.files)
        if zip_file_errors:
            console.error(zip_file_errors)
            abort(404, message=zip_file_errors)
        # cache zip file os successful validation
        f = request.files["zip_file"]
        filename = werkzeug.utils.secure_filename(f.filename)
        # move the file pointer back to the beginning
        f.stream.seek(0)
        f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        if args.stand_alone:
            # if stand alone do not contact other services
            return {"status": "uploaded", "meta": meta, "stand_alone": True}, 201

        # inform Engine API of new upload
        meta["filename"] = filename
        response = requests.post(engine_endpoint, json=meta)
        return {"status": "uploaded", "meta": meta, "engine": response.json()}, 201


# add API resources
api.add_resource(ZipFileUploaderAPI, "/", "/upload")


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(description="Upload API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address. Default is %(default)s.")
    parser.add_argument("--port", default=5000, help="The host port. Default is %(default)s.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging. Default is %(default)s.")
    parser.add_argument("--stand-alone", action="store_true", default=False, help="Disable communications with other containers. Default is %(default)s.")
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(
        format="[%(asctime)s] [%(name)s:%(lineno)d] [%(levelname)s]: %(message)s",
        datefmt="%Y-%m-%dT%H:%M:%S%z",
        level=os.getenv("LOG_LEVEL", "INFO")
    )
    console = logging.getLogger("upload.api")
    # stop log propagation
    logging.getLogger("werkzeug").propagate = False
    # wait for Engine API
    if not args.stand_alone:
        libdrm.apis.check_status(engine_endpoint)
    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
