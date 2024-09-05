from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from src.models.models import db
from src.routes.routes import bp

app = Flask(__name__)

# Configurations for the database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:@localhost:3306/sportify'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db.init_app(app)

# Initialize the migration
migrate = Migrate(app, db, directory='src/db/migrations')

# Register the blueprint
app.register_blueprint(bp)

# Run the app, listening on all IPs, on port 5000 in debug mode
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
