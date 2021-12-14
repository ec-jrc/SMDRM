"""Download DeepPavlov NER model."""

import deeppavlov
import tensorflow
tensorflow.compat.v1.logging.set_verbosity(tensorflow.compat.v1.logging.ERROR)

# download deeppavlov ner bert algorithm
deeppavlov.build_model(deeppavlov.configs.ner.ner_ontonotes_bert_mult, download=True)
