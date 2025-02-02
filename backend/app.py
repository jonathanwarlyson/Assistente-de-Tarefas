from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime
from apscheduler.schedulers.background import BackgroundScheduler
from flask_socketio import SocketIO

#instancia do flask
app = Flask(__name__)
CORS(app) #comunicação com frontend
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///tasks.db'

#inicia o banco de dados
db = SQLAlchemy(app)

socketio = SocketIO(app, cors_allowed_origins="*", logger=True, engineio_logger=True)

#define o modelo
class Task(db.Model): 
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) #titulo da tarefa
    due_time = db.Column(db.DateTime, nullable=False) #prazo (data/hora)
    completed = db.Column(db.Boolean, default=False) #status

#cria as tabelas
with app.app_context():
    db.create_all()

@app.route('/tasks', methods=['POST'])
def add_task():
    data = request.json
    new_task = Task(
        title=data['title'],
        due_time=datetime.strptime(data['due_time'], '%Y-%m-%d %H:%M')
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"message": "Tarefa adicionada!"}), 201


@app.route('/tasks', methods=['GET'])
def get_tasks():
    tasks = Task.query.all() 
    tasks_json = [{
        "id": task.id,
        "title": task.title,
        "due_time": task.due_time.isoformat(),
        "completed": task.completed
    } for task in tasks]
    return jsonify(tasks_json)


@app.route('/tasks/<int:id>/complete', methods=['PUT'])
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({"message": "Tarefa concluída!"})
    else:
        return jsonify({"error": "Tarefa não encontrada"}), 404
    

@app.route('/notifications', methods=['GET'])
def get_notifications():
    with app.app_context():
        now = datetime.now()
        pending_tasks = Task.query.filter(
            Task.completed == False,
            Task.due_time <= now
        ).all()

        notifications = [
        {"message": f'Lembrete: "{task.title}" está pendente!'}
        for task in pending_tasks
        ]
    return jsonify(notifications)

@app.route('/tasks/clear', methods=['DELETE'])
def clear_tasks():
    try:
        num_deleted = db.session.query(Task).delete()
        db.session.commit()
        return jsonify({"message": f"{num_deleted} tarefas removidas!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    with app.app_context():
        socketio.run(app, host="0.0.0.0", port=5000, debug=True, allow_unsafe_werkzeug=True)
()