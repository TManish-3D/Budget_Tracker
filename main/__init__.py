from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'yourhoood'


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
    'DATABASE_URL',
    'postgresql://budget_user:%40Thalaboy98@localhost:5432/budget_tracker'
)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# (Render/Heroku quirk) normalize postgres:// -> postgresql://
db_url = app.config['SQLALCHEMY_DATABASE_URI']
if db_url and db_url.startswith("postgres://"):
    app.config['SQLALCHEMY_DATABASE_URI'] = db_url.replace("postgres://", "postgresql://", 1)


db = SQLAlchemy(app)

migrate = Migrate(app, db)
bcrypt=Bcrypt(app)
login_manager=LoginManager(app)
login_manager.login_view = 'login' 

# import routes so they are registered
from main import routes
from main import models
