from flask import request, jsonify
from src.db import db
from src.models.models import Product
from src.helpers.http_helper import HttpHelper
from src.validators.product_validator import ProductValidator, ProductUpdateValidator
from marshmallow import ValidationError


def create_product():
    """
    Create a new product in the system.

    This function validates the product input and saves the product in the database.

    Returns:
        JSON response with success or error message.
    """

    schema = ProductValidator()

    try:
        # Validate the incoming JSON data
        product_data = schema.load(request.json)

        # Create a new product instance
        product = Product(
            name=product_data["name"],
            description=product_data["description"],
            price=product_data["price"],
            brand_id=product_data["brand_id"],
            category_id=product_data["category_id"],
            sport_id=product_data["sport_id"],
            gender_id=product_data["gender_id"],
            country_id=product_data["country_id"],
            composition=product_data.get("composition"),
            discount_price=product_data.get("discount_price"),
            image_url=product_data.get("image_url", ""),
        )

        # Add and commit the new product to the database
        db.session.add(product)
        db.session.commit()

        return HttpHelper.response(
            HttpHelper.retCreated, {"message": "Product created successfully"}
        )

    except ValidationError as err:
        return HttpHelper.response(HttpHelper.retUnprocessableContent, err.messages)

    except Exception as e:
        db.session.rollback()
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})


def get_products():
    """
    Retrieve all products in the system.

    This function fetches all products from the database and returns them as a JSON response.

    Returns:
        JSON response with a list of products or an error message.
    """

    try:
        # Fetch all products
        products = Product.query.all()

        # Serialize the products
        product_list = [
            {
                "id": product.id,
                "name": product.name,
                "description": product.description,
                "price": product.price,
                "discount_price": product.discount_price,
                "image_url": product.image_url,
                "brand_id": product.brand_id,
                "category_id": product.category_id,
                "sport_id": product.sport_id,
                "gender_id": product.gender_id,
                "country_id": product.country_id,
                "composition": product.composition,
            }
            for product in products
        ]

        return HttpHelper.response(HttpHelper.retOK, product_list)

    except Exception as e:
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})


def get_product_by_id(product_id):
    """
    Retrieve a single product by ID.

    This function fetches a product from the database by its ID and returns it as a JSON response.

    Args:
        product_id: The ID of the product to retrieve.

    Returns:
        JSON response with the product data or an error message
    """

    try:
        # Fetch the product by ID
        product = Product.query.get(product_id)

        if not product:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "Product not found"}
            )

        # Serialize the product
        product_data = {
            "id": product.id,
            "name": product.name,
            "description": product.description,
            "price": product.price,
            "discount_price": product.discount_price,
            "image_url": product.image_url,
            "brand_id": product.brand_id,
            "category_id": product.category_id,
            "sport_id": product.sport_id,
            "gender_id": product.gender_id,
            "country_id": product.country_id,
            "composition": product.composition,
        }

        return HttpHelper.response(HttpHelper.retOK, product_data)

    except Exception as e:
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})


def update_product(product_id):
    """
    Update an existing product by ID.

    This function validates the incoming JSON data and updates the product in the database.

    Args:
        product_id: The ID of the product to update.

    Returns:
        JSON response with success or error message.
    """

    schema = ProductUpdateValidator()

    try:
        # Validate the incoming JSON data
        product_data = schema.load(request.json)

        # Fetch the product by ID
        product = Product.query.get(product_id)

        if not product:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "Product not found"}
            )

        # We search the fields that are present in the request and update them
        for key, value in product_data.items():
            if value is not None:
                setattr(product, key, value)

        # Commit the changes to the database
        db.session.commit()

        return HttpHelper.response(
            HttpHelper.retOK, {"message": "Product updated successfully"}
        )

    except ValidationError as err:
        return HttpHelper.response(HttpHelper.retUnprocessableContent, err.messages)

    except Exception as e:
        db.session.rollback()
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})


def delete_product(product_id):
    """
    Delete an existing product by ID.

    This function deletes a product from the database by its ID.

    Args:
        product_id: The ID of the product to delete.

    Returns:
        JSON response with success or error message.
    """

    try:
        # Fetch the product by ID
        product = Product.query.get(product_id)

        if not product:
            return HttpHelper.response(
                HttpHelper.retNotFound, {"message": "Product not found"}
            )

        # Delete the product from the database
        db.session.delete(product)
        db.session.commit()

        return HttpHelper.response(
            HttpHelper.retOK, {"message": "Product deleted successfully"}
        )

    except Exception as e:
        db.session.rollback()
        return HttpHelper.response(HttpHelper.retErrorServer, {"error": str(e)})
