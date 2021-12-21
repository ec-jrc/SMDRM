import logging
from . import info_blueprint
from flask import abort, jsonify, current_app

# setup logger
logger = logging.getLogger()


@info_blueprint.route('/', methods=['GET'])
def index():
    # TODO: create swagger doc
    logger.debug("TODO: create swagger doc")
    return jsonify("Index page")


@info_blueprint.route('/status', methods=['GET'])
def status():
    response = {"is_alive": True}
    logger.debug(response)
    return response, 200
