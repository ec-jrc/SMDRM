import deeppavlov
from flask import Flask, request, jsonify
from flask_restful import Resource, Api, abort
import os
import tensorflow

#tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

# api info
app = Flask("DeepPavlovAPI")
api = Api(app)

# download/initialize DeepPavlov NER bert algorithm
# DeepPavlov model returns 2 lists per sentence.
# A list of tokens as the words in the sentence, and a list of tags as the model predictions.
# e.g. [There,was,flood,in,London] [O,O,O,O,GPE]
model = deeppavlov.build_model(deeppavlov.configs.ner.ner_ontonotes_bert_mult, download=False)


class DeepPavlovStatus(Resource):
    """API status."""

    def get(self):
        return {"is_alive": True}, 200


class DeepPavlovProbe(Resource):
    """API test."""

    def post(self):
        try:
            y_hat = model(["string"])
            return jsonify(['Test passed'])
        except:
            return jsonify(['Test failed'])


class DeepPavlovModel(Resource):
    """
    A custom API hosting a ready-to-use instance of the DeepPavlov
    Named Entity Recongnition AI framework.
    It is an external plugin to tag input texts.
    Return a dictionary that contains two fields:
        tokens: the tokenized input texts
        tags: the NER tags for each token in each text.

    Notes
        DeepPavlov NER algorithm uses prefixes to indicate B-egin,
        and I-nside relative positions of tokens. For more details, visit
        http://docs.deeppavlov.ai/en/master/features/models/ner.html#ner-task.
    """

    def post(self):
        """
        Input: {"texts": t.List[str]}
        Ouptut: {"tags": tags_ext, "tokens": texts_tokens}
        """
        texts = request.json.get("x", None)
        if not texts:
            msg = "Missing input texts."
            console.error(msg)
            abort(400, message=msg)

        # run NER model against texts
        y_hat = model(texts)
        console.debug(y_hat)
        return y_hat, 201


# add API resources
api.add_resource(DeepPavlovStatus, "/status")
api.add_resource(DeepPavlovModel, "/model")
api.add_resource(DeepPavlovProbe, "/probe")


if __name__ == "__main__":
    import argparse
    import logging

    parser = argparse.ArgumentParser(
        description="""A custom API hosting a ready-to-use instance of the
        DeepPavlov Named Entity Recongnition AI framework."""
    )
    parser.add_argument("--host", default="0.0.0.0", help="The host IP address. Default is %(default)s.")
    parser.add_argument("--port", default=5000, help="The host port. Default is %(default)s.")
    parser.add_argument("--debug", action="store_true", default=False, help="Enable debugging. Default is %(default)s.")
    args = parser.parse_args()

    # setup logging
    logging.basicConfig(level="DEBUG" if args.debug else "INFO")
    console = logging.getLogger("deeppavlov")
    logging.getLogger("werkzeug").propagate = False

    # start api
    app.run(debug=args.debug, host=args.host, port=args.port)
