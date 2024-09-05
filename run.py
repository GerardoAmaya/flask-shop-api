from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from extensions import db, ma, mail
from src.routes.routes import bp, user_bp
from flask_mail import Mail
from config import Config

app = Flask(__name__)

# Load the configurations(env) from the Config class
app.config.from_object(Config)

# Initialize the extensions
db.init_app(app)
ma.init_app(app)
mail.init_app(app)


migrate = Migrate(app, db, directory="src/db/migrations")

# Register the blueprints
app.register_blueprint(bp)
app.register_blueprint(user_bp, url_prefix="/user")

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
