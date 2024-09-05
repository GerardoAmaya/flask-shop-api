import json
from src.models.models import Brand
from src.db import db

def seed_brands():
    with open('src/db/seeders/json_data/brands.json') as f:
        data = json.load(f)

    for brand_data in data['brands']:
        brand = Brand(name=brand_data['name'], description=brand_data['description'])
        db.session.add(brand)

    db.session.commit()
    print("Marcas insertadas correctamente.")
