import json
import os
import joblib
from laserembeddings import Laser
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences

# ner models directory (inside Docker)
models_dir = "/home/user/models"

# load floods models config
# fail if not found
config_file = os.path.join(models_dir, "models", "current-model.json")
if not os.path.exists(config_file):
    raise ValueError(
        "Configuration file not found. Check if $MODELS_DIR is set, and has valid content."
    )
with open(config_file) as conf:
    floods_config = json.load(conf)["model-by-language"]

# languages for which a NER model trained for floods exists
available_languages = [lang for lang in floods_config]

# laserembeddings config (multilingual tokenizazion)
embeddings_dir = os.path.join(models_dir, "embeddings")
codes_path = os.path.join(embeddings_dir, "93langs.fcodes")
vocab_path = os.path.join(embeddings_dir, "93langs.fvocab")
encoder_path = os.path.join(embeddings_dir, "bilstm.93langs.2018-12-26.pt")
# embeddings instance
laser = Laser(codes_path, vocab_path, encoder_path)


class FloodsAnnotator(object):
    """
    Load Machine Learning Annotation Flood models developed in the E1 unit by language.
    params
        - lang: the language of the incoming text
    """

    def __init__(self, lang: str):
        # lang
        self.lang = lang
        # model id (filename from config file)
        self._model_id = floods_config[self.lang]
        # load model at init
        self._model = load_model(
            os.path.join(models_dir, "models", f"{self._model_id}.model.h5"),
            compile=False,
        )
        # load language based tokenizer if lang is not multilingual
        if not self.is_multi_lang:
            # tokenizer model is available only for in-house built models
            self._tokenizer = joblib.load(
                os.path.join(models_dir, "models", f"{self._model_id}.tokenizer")
            )
            self._tokenizer.oov_token = None

    @property
    def is_multi_lang(self):
        return self.lang == "ml"

    def infer(self, input_data: list):
        if self.is_multi_lang:
            # vectorize unknown language using laserembeddings
            tokens = laser.embed_sentences(input_data, lang=self.lang)
        else:
            # tokenize using language specific in-house built models
            tokens = pad_sequences(
                self._tokenizer.texts_to_sequences(input_data),
                maxlen=self._model.layers[0].input_shape[0][1],
            )

        return self._model.predict(tokens)[:, 1]


def init_annotators():
    """Floods Annotators Factory
    preload Floods models by language at initialization
    to have them ready on incoming HTTP requests."""
    annotators_by_lang = {}
    for lang in available_languages:
        annotators_by_lang[lang] = FloodsAnnotator(lang=lang)
    return annotators_by_lang
