from flask_sqlalchemy import SQLAlchemy
from flask import Flask
app = Flask(__name__)
app = Flask(__name__, template_folder='../templates')
app.config.from_object('config')
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:postgres@localhost:5432/band_db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'C2HWGVoMGfNTBsrYQg8EcMrdTimkZfAb'
db = SQLAlchemy(app)
