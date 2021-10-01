# -*- coding: utf-8 -*-

import os
import json

import joblib
import laserembeddings
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences


class FloodsAnnotator(object):
    """
    Load Machine Learning Annotation Flood models developed in the E1 unit by language.
    params
        - lang: the language of the incoming text
    """
    # the path to the floods models
    MODELS_PATH = os.path.join(os.path.abspath(os.path.dirname(__file__)), "../models")

    def __init__(self, lang: str):
        # lang
        self.lang = lang
        # model id (filename from config file)
        self._model_id = self._get_model_id()
        # load model at init
        self._model = load_model(os.path.join(self.MODELS_PATH, f"{self._model_id}.model.h5"), compile=False)
        # load embeddings if multi lingual model is selected
        if self.is_multi_lang:
            self._embeddings = laserembeddings.Laser(
                bpe_codes=os.path.join(self.MODELS_PATH, "embeddings", "93langs.fcodes"),
                bpe_vocab=os.path.join(self.MODELS_PATH, "embeddings", "93langs.fvocab"),
                encoder=os.path.join(self.MODELS_PATH, "embeddings", "bilstm.93langs.2018-12-26.pt"),
            )
        else:
            # tokenizer model is available only for in-house built models
            self._tokenizer = joblib.load(os.path.join(self.MODELS_PATH, f"{self._model_id}.tokenizer"))
            self._tokenizer.oov_token = None

    @classmethod
    def _load_filenames_by_lang(cls):
        # load config file (language mapping)
        _config_file = os.path.join(cls.MODELS_PATH, "current-model.json")
        if not os.path.exists(_config_file):
            raise ValueError(f"Model is not initialized. {_config_file} lookup table filepath not found")
        with open(_config_file) as _input:
            return json.load(_input)['model-by-language']

    @classmethod
    def available_languages(cls):
        return [lang for lang in cls._load_filenames_by_lang()]

    def _get_model_id(self):
        return self._load_filenames_by_lang()[self.lang]

    @property
    def is_multi_lang(self):
        return self.lang == "ml"

    def infer(self, input_data: list):
        if self.is_multi_lang:
            # vectorize unknown language using laserembeddings
            tokens = self._embeddings.embed_sentences(input_data, lang="ml")
        else:
            # tokenize using language specific in-house built models
            tokens = pad_sequences(self._tokenizer.texts_to_sequences(input_data),
                                   maxlen=self._model.layers[0].input_shape[0][1])

        return self._model.predict(tokens)[:, 1][0]
