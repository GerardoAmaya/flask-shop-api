# src/db/seeders/RoleSeeder.py
import json
from src.models.models import Role
from src.db import db

def seed_roles():
    with open("src/db/seeders/json_data/roles.json") as f:
        data = json.load(f)

    for role_data in data["roles"]:
        role = Role(name=role_data["name"])
        db.session.add(role)

    db.session.commit()
    print("Roles insertados correctamente.")
