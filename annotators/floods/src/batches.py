import collections
import typing
import numpy


def data_points_by_lang(batch: typing.List[dict], available_languages: typing.List[str]):
    """Group data points by language to be annotated with the right annotator."""
    by_lang = collections.defaultdict(list)
    for index, data_point in enumerate(batch):
        lang = data_point["lang"] if data_point["lang"] in available_languages else "ml"
        by_lang[lang].append(data_point)
    return by_lang


def iter_array_of_data_points(by_lang: typing.Dict):
    """Yield data points as array of texts for sanitation and annotation."""
    for lang, data_points in by_lang.items():
        texts = numpy.array([data_point["text"] for data_point in data_points])
        yield lang, texts


# define the FloodsAnnotator type without importing it
FloodsAnnotator = typing.TypeVar("FloodsAnnotator")


def annotate_batch(
    data_points_array_by_lang: typing.Iterable,
    sanitizer: typing.Callable[[typing.List[str]], typing.List[str]],
    annotators: typing.Dict[str, FloodsAnnotator],
):
    """Yield annotated and sanitized texts by language."""
    for lang, texts in data_points_array_by_lang:
        sanitized_texts = sanitizer(texts)
        annotated_texts = annotators[lang].infer(sanitized_texts)
        yield lang, annotated_texts, sanitized_texts


def add_annotations_to_batch(annotated_batch, by_lang):
    for lang, annotated, sanitized in annotated_batch:
        batch_by_lang = by_lang[lang]
        for index in range(len(batch_by_lang)):
            batch_data_point = batch_by_lang[index]
            batch_data_point["annotations"] = [
                {
                    "annotation_type": "floods",
                    "annotation_prob": str(annotated[index]),
                    "sanitized_text": sanitized[index]
                }
            ]
            yield batch_data_point
