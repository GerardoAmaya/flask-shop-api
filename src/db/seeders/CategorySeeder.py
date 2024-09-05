import json
from src.models.models import Category
from src.db import db

def seed_categories():
    with open('src/db/seeders/json_data/categories.json') as f:
        data = json.load(f)

    for category_data in data['categories']:
        category = Category(name=category_data['name'], description=category_data['description'])
        db.session.add(category)

    db.session.commit()
    print("Categorías insertadas correctamente.")
