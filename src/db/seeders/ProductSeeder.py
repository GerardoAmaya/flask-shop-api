import json
from src.models.models import Product, Brand, Category, Sport, Gender, Country
from src.db import db

def seed_products():
    with open('src/db/seeders/json_data/products.json') as f:
        data = json.load(f)

    for product_data in data['products']:
        brand = Brand.query.get(product_data['brand_id'])
        category = Category.query.get(product_data['category_id'])
        sport = Sport.query.get(product_data['sport_id'])
        gender = Gender.query.get(product_data['gender_id'])
        country = Country.query.get(product_data['country_id'])

        product = Product(
            name=product_data['name'],
            description=product_data['description'],
            price=product_data['price'],
            discount_price=product_data['discount_price'],
            image_url=product_data['image_url'],
            brand=brand,
            category=category,
            sport=sport,
            gender=gender,
            country=country,
            composition=product_data['composition']
        )
        db.session.add(product)

    db.session.commit()
    print("Productos insertados correctamente.")
