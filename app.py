from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from config import Config
from flask_migrate import Migrate

app = Flask(__name__)
app.config.from_object(Config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from routes import *  # Import routes_app after creating Flask app instance

app.register_blueprint(routes_app)

if __name__ == '__main__':
    app.run(debug=True)