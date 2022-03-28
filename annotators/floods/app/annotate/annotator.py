import json
import os
from laserembeddings import Laser
from tensorflow.keras.models import load_model

# ner models directory (inside Docker)
models_dir = "/home/user/models"

# laserembeddings config (multilingual tokenizazion)
model_path = os.path.join(models_dir, "lasermultilingual.model.h5")
codes_path = os.path.join(models_dir, "93langs.fcodes")
vocab_path = os.path.join(models_dir, "93langs.fvocab")
encoder_path = os.path.join(models_dir, "bilstm.93langs.2018-12-26.pt")
# embeddings instance
laser = Laser(codes_path, vocab_path, encoder_path)


class FloodsAnnotator(object):
    """Load Machine Learning Annotation Flood models developed in the E1 unit."""

    def __init__(self):
        self._model = load_model(model_path, compile=False)

    def vectorize(self, texts: list):
        """Vectorize any language."""
        return laser.embed_sentences(texts, lang="ml")

    def infer(self, texts: list):
        """Predict floods probability."""
        return self._model.predict(self.vectorize(texts))[:, 1]

