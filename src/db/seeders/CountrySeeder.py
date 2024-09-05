import json
from src.models.models import Country
from src.db import db

def seed_countries():
    with open('src/db/seeders/json_data/countries.json') as f:
        data = json.load(f)

    for country_data in data['countries']:
        country = Country(name=country_data['name'])
        db.session.add(country)

    db.session.commit()
    print("Países insertados correctamente.")
