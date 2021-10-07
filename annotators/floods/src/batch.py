import collections
import numpy


def data_by_lang(data, available_languages):
    header = []
    by_lang = collections.defaultdict(list)
    for index, _batch in enumerate(data["batch"]):
        if index == 0:
            header.extend(list(_batch))
        lang = "ml" if _batch["lang"] not in available_languages else _batch["lang"]
        by_lang[lang].append(list(_batch.values()))
    return by_lang, header


def batch_annotate(data, sanitizer, annotator, available_languages):
    data_points, fields = data_by_lang(data, available_languages)
    text_iloc = fields.index("text")
    annotated = []
    fields.extend(["text_sanitized", "annotation"])
    for lang, batch in data_points.items():
        data_points_array = numpy.array(batch)
        texts = data_points_array[:, text_iloc]
        sanitized = sanitizer(texts)
        predictions = annotator[lang].infer(sanitized)
        res = numpy.column_stack((data_points_array, sanitized, predictions))
        for a in res:
            annotated.append(dict(zip(fields, a)))
    return {"batch": annotated}
