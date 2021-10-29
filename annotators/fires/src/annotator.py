import os
import torch
from scipy.special import softmax

from transformers import (
    AutoModel,
    AutoTokenizer,
    RobertaForSequenceClassification,
    Trainer,
)


class DataPointsBatch(torch.utils.data.Dataset):
    def __init__(self, encodings, labels):
        self.encodings = encodings
        self.labels = labels

    def __getitem__(self, idx):
        item = {key: torch.tensor(val[idx]) for key, val in self.encodings.items()}
        return item

    def __len__(self):
        return len(self.labels)


class FiresAnnotator:
    """Load Machine Learning Annotation Fires. Developed by Ivan Kitanovski."""

    # the path to the floods models
    MODELS_PATH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "models")

    def __init__(self):
        # load model at init
        self._model = RobertaForSequenceClassification.from_pretrained(self.MODELS_PATH)
        # tokenizer model is available only for in-house built models
        self._tokenizer = AutoTokenizer.from_pretrained("xlm-roberta-base", normalization=True)

    def infer(self, input_data: list):
        encodings = self._tokenizer(input_data, truncation=True, padding=True)
        dataset = DataPointsBatch(encodings, [0] * len(input_data))
        trainer = Trainer(model=self._model)
        # predict everything
        res = trainer.predict(dataset)
        # get the probs
        probs = softmax(res.predictions, axis=1)
        # return the score for the `positive` class only
        return [float(prob[1] if prob[1] > prob[0] else 1 - prob[1]) for prob in probs]
