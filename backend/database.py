from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from models import db

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    db.init_app(app)
    return app

app = create_app()

def create_tables():
    with app.app_context():
        db.create_all()

if __name__ == "__main__":
    create_tables()