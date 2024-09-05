import json
from src.models.models import Sport
from src.db import db

def seed_sports():
    with open('src/db/seeders/json_data/sports.json') as f:
        data = json.load(f)

    for sport_data in data['sports']:
        sport = Sport(name=sport_data['name'])
        db.session.add(sport)

    db.session.commit()
    print("Deportes insertados correctamente.")
