from marshmallow import Schema, fields, validate


class BrandValidator(Schema):
    """
    This class is a schema validator for the brand creation endpoint.
    It validates the incoming JSON data for creating a new brand.
    """

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Brand name is required."},
    )

    description = fields.Str(
        required=False,
        allow_none=True,
    )
