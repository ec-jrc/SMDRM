# -*- coding: utf-8 -*-

import json
from flask import Flask, request
from flask_restful import Resource, Api, abort
import requests

from libdrm.datamodels import DisasterEventModel
from libdrm.elastic import ElasticSearchClient
from libdrm.nicelogging import setup_logger


# api info
name = "Orchestrator"
app = Flask(name)
api = Api(app)

# api cached data points
CACHE = {}

logger = setup_logger(name)


class OrchestratorAPI(Resource):

    def get(self):
        response = {"api_name": name, "resource": "/upload", "is_alive": True, "uploads": CACHE}
        logger.debug(response)
        return response, 200

    def post(self):
        data = request.get_json()
        if not data:
            abort(404, message="No data points received.")
        data_point = DisasterEventModel.from_dict(data)
        CACHE[data_point.id] = data_point.to_dict()
        logger.debug("[{}] cached".format(data_point.id))
        return {"status": "uploaded"}, 201


# class DataPointAnnotator(Resource):
#
#     def get(self):
#         return {"api_name": name, "resource": "/annotate", "is_alive": True}, 200
#
#     def post(self):
#         # call AnnotatorAPI and annotate the data point using the text
#         response = requests.post("http://floods:5010", json=data_point.to_dict())
#         data_point.annotations.update(response.json())
#
#
# class DataPointPersister(Resource):
#
#     def __init__(self, es_client):
#         self.es_client = es_client
#
#     def get(self):
#         response = {"api_name": name, "resource": "/persist", "is_alive": True}
#         logger.debug(response)
#         return response, 200
#
#     def post(self):
#         # get data point from CACHE and save to elasticsearch
#         # Visualizations available @ http://kibana:5601
#         if not CACHE:
#             abort(404, message="The request data is empty.")
#         response = self.es_client.bulk_insert(CACHE).json()
#         if "errors" in response:
#             abort(404, **response)
#         return response, 201
#
#
# # init ElasticSearch client
# # block process until elasticsearch is up or attempts limit
# es = ElasticSearchClient()
# es.wait_for_it()
# es.create_index()

# add API resources
api.add_resource(OrchestratorAPI, "/")

#api.add_resource(DataPointPersister, "/persist", resource_class_kwargs={'es_client': es})
#api.add_resource(DataPointAnnotator, "/annotate")


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Orchestrator API.")
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address.")
    parser.add_argument("--port", default=5000, help="The host port.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Enable debugging."
    )
    args = parser.parse_args()
    app.run(debug=args.debug, host=args.host, port=args.port)
