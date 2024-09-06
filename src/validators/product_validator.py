from marshmallow import Schema, fields, validate


class ProductValidator(Schema):
    """
    This class is a schema validator for the product creation endpoint.
    It validates the incoming JSON data for creating a new product.
    """

    name = fields.Str(
        required=True,
        validate=validate.Length(min=1),
        error_messages={"required": "Name is required."},
    )

    description = fields.Str(
        required=True,
        error_messages={"required": "Description is required."},
    )

    price = fields.Float(
        required=True,
        error_messages={"required": "Price is required."},
    )

    brand_id = fields.Int(
        required=True,
        error_messages={"required": "Brand ID is required."},
    )

    category_id = fields.Int(
        required=True,
        error_messages={"required": "Category ID is required."},
    )

    sport_id = fields.Int(
        required=True,
        error_messages={"required": "Sport ID is required."},
    )

    gender_id = fields.Int(
        required=True,
        error_messages={"required": "Gender ID is required."},
    )

    country_id = fields.Int(
        required=True,
        error_messages={"required": "Country ID is required."},
    )

    discount_price = fields.Float(
        required=False,
        allow_none=True,
    )

    composition = fields.Str(
        required=False,
        allow_none=True,
    )

    image_url = fields.Str(
        required=False,
        allow_none=True,
    )


class ProductUpdateValidator(Schema):
    """
    This class is a schema validator for the product update endpoint.
    It validates the incoming JSON data for updating an existing product.
    """

    name = fields.Str(
        required=False,
    )

    description = fields.Str(
        required=False,
    )

    price = fields.Float(
        required=False,
    )

    brand_id = fields.Int(
        required=False,
    )

    category_id = fields.Int(
        required=False,
    )

    sport_id = fields.Int(
        required=False,
    )

    gender_id = fields.Int(
        required=False,
    )

    country_id = fields.Int(
        required=False,
    )

    discount_price = fields.Float(
        required=False,
        allow_none=True,
    )

    composition = fields.Str(
        required=False,
        allow_none=True,
    )

    image_url = fields.Str(
        required=False,
        allow_none=True,
    )
