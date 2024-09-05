import json
from src.models.models import Gender
from src.db import db

def seed_genders():
    with open('src/db/seeders/json_data/genders.json') as f:
        data = json.load(f)

    for gender_data in data['genders']:
        gender = Gender(name=gender_data['name'])
        db.session.add(gender)

    db.session.commit()
    print("Géneros insertados correctamente.")
