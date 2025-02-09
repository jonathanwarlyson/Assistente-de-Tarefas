from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_socketio import SocketIO
from models import db, Task
from routes import routes

def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    
    db.init_app(app)

    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()

    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    with app.app_context():
        socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)