from src.db.seeders.BrandSeeder import seed_brands
from src.db.seeders.CategorySeeder import seed_categories
from src.db.seeders.SportSeeder import seed_sports
from src.db.seeders.GenderSeeder import seed_genders
from src.db.seeders.CountrySeeder import seed_countries
from src.db.seeders.ProductSeeder import seed_products
from src.db.seeders.RoleSeeder import seed_roles
from src.db.seeders.RoleSeeder import seed_roles
from run import app


def run_all_seeders():
    print("Iniciando seeders...")

    with app.app_context():
        seed_brands()
        seed_categories()
        seed_sports()
        seed_genders()
        seed_countries()
        seed_products()
        seed_roles()

    print("Todos los seeders han sido ejecutados correctamente.")
