from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from flask_socketio import SocketIO
from models import db, Task
from routes import routes

<<<<<<< HEAD
=======
#instancia do flask
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b
def create_app():
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}})
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'
    
<<<<<<< HEAD
=======
    # Inicialize a instância do SQLAlchemy com a aplicação Flask
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b
    db.init_app(app)

    socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

<<<<<<< HEAD
=======
    # Registre blueprints aqui
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b
    app.register_blueprint(routes)

    with app.app_context():
        db.create_all()

    return app, socketio

app, socketio = create_app()

if __name__ == '__main__':
    with app.app_context():
        socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)