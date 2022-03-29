import logging
from flask import render_template, request, abort, current_app, jsonify
from . import annotate_blueprint
from .annotator import FloodsAnnotator

# load Floods annotator
annotator = FloodsAnnotator()


@annotate_blueprint.route("/test", methods=["GET"])
def test_model():
    """Test annotation."""
    result = "failed"
    proba = annotator.infer(["string"])
    if proba:
        result = "passed"
    current_app.logger.debug(result)
    return jsonify(result), 200


@annotate_blueprint.route("/annotate", methods=["POST"])
def annotate():
    """Annotate batch of texts.
    Input: {"texts": typing.List[str]}
    Ouptut: typing.List[str]
    """
    texts = request.json.get("texts", None)
    if not texts:
        abort(400, description="JSON input texts missing.")

    # predict floods probability from texts
    proba = annotator.infer(texts)
    # return scores as valid JSON format
    response = jsonify(["{:.6f}".format(round(p, 6)) for p in proba])
    current_app.logger.debug(response)
    return response, 201

