import logging
from flask import render_template, request, abort, current_app, jsonify
from . import annotate_blueprint
from .annotator import init_annotators

# setup logger
logger = logging.getLogger()

# preload annotators
annotators = init_annotators()
languages = [lang for lang in annotators]
# log available languages
logger.info("annotation offered in {}".format(languages))


@annotate_blueprint.route('/languages', methods=['GET'])
def get_languages():
    """Get languages available for annotation."""
    return jsonify(languages), 200


@annotate_blueprint.route('/test', methods=['GET'])
def test_model():
    """Test annotation."""
    result = "failed"
    test_annotator = annotators["en"]
    proba = test_annotator.infer(["string"])
    if proba:
        result = "passed"
    logger.debug(result)
    return jsonify(result), 200


@annotate_blueprint.route('/annotate/<string:lang>', methods=['POST'])
def annotate(lang):
    """Annotate batch of texts of a specific language.
    Input: {"texts": t.List[str]}
    Ouptut: {"floods_proba": probas, "lang": lang}
    """
    if lang not in languages:
        current_app.logger.warning("Unkwnon language ISO code. Use `ml` to enable a multilingual annotation.")
        abort(400)

    texts = request.json.get("texts", None)
    if not texts:
        current_app.logger.error("JSON input texts missing.")
        abort(400)

    # select annotator with lang field and infer probability scores
    annotator = annotators[lang]
    proba = annotator.infer(texts)
    # return scores as valid JSON format
    response = jsonify(["{:.6f}".format(round(p, 6)) for p in proba])
    logger.debug(response)
    return response, 201
