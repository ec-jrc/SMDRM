import marshmallow.validate
from .upload import ZipFileModel


def validate_zipfile(file):
    uploaded_file = ZipFileModel(file)
    valid = uploaded_file.is_valid_file()
    bad_files = uploaded_file.has_valid_content()
    if not valid:
        raise marshmallow.ValidationError("Uploaded file is not a zip file.")
    if bad_files is not None:
        raise marshmallow.ValidationError("[{}]: invalid uploaded file content.".format(bad_files))


class ZipFileUploadSchema(marshmallow.Schema):
    upload_file = marshmallow.fields.Raw(
        type='file',
        required=True,
        validate=validate_zipfile,
    )


class EventUploadSchema(marshmallow.Schema):
    # default data fields
    id = marshmallow.fields.String(required=True)
    created_at = marshmallow.fields.String(required=True)
    lang = marshmallow.fields.String(required=True)
    text = marshmallow.fields.String(required=True)
    # created at model init
    uploaded_at = marshmallow.fields.String()
    # we expect the disaster type coming from the user
    disaster_type = marshmallow.fields.String(
        validate=marshmallow.validate.OneOf(["floods", "fires", ]),
        required=True
    )
    # runtime event properties to be populated by internal APIs
    # sanitized text contains the text prepared for the machine learning models
    text_sanitized = marshmallow.fields.String(required=False)
    # annotation dictionary will be the placeholder for disaster type related model probability score
    annotations = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.Str(),
        required=False,
    )
    # TODO: img dictionary contains image metadata e.g., path, size, format, etc.
    img = marshmallow.fields.Dict(
        keys=marshmallow.fields.Str(),
        values=marshmallow.fields.Str(),
        required=False,
    )

    class Meta:
        ordered = True
        unknown = marshmallow.EXCLUDE
