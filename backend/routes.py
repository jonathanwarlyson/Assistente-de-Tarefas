from flask import Blueprint, request, jsonify
from models import db, Task, Category, Priority
from datetime import datetime
from flask_cors import CORS

routes = Blueprint('routes', __name__)
CORS(routes)

@routes.route('/categories', methods=['POST'])
def add_category():
    data = request.json
    if not data.get("name"):
        return jsonify({"error": "Nome da categoria obrigatório"}), 400
    
    category = Category(name=data["name"])
    db.session.add(category)
    db.session.commit()
    return jsonify({"message": "Categoria criada!", "id": category.id}), 201

@routes.route('/categories', methods=['GET'])
def get_categories():
    categories = Category.query.all()
    return jsonify([{"id": c.id, "name": c.name} for c in categories])

@routes.route('/priorities', methods=['POST'])
def get_priorities():
    priorities = Priority.query.all()
    return jsonify([{"id": c.id, "name": c.name}
    for c in priorities])

@routes.route('/categories/clear', methods=['DELETE'])
def clear_categories():
    clean_categories = []
    categories = Category.query.all()
    for category in categories:
        if not category.tasks:
            clean_categories.append(category.name)
            db.session.delete(category)
            db.session.commit()
            return jsonify({"message": f"Categorias sem tarefas removidas!"}), 200

@routes.route('/tasks', methods=['POST'])
def add_task():
    data = request.get_json()
    title = data.get('title')
    due_time = data.get('due_time')
    category_id = data.get('category_id')
    priority_level = data.get('priority_id')

    if priority_level not in ['Baixa', 'Média', 'Alta']:
        return jsonify({"error": "Prioridade inválida"}), 400

    priority = Priority.query.filter_by(id=priority_level).first()
    if not priority:
        priority = Priority(level=priority_level)
        db.session.add(priority)
        db.session.commit()

    try:
        new_task = Task(
            title=title,
            due_time=datetime.strptime(data['due_time'], '%Y-%m-%d %H:%M'),
            category_id=category_id,
            priority_id=priority.id
        )
        db.session.add(new_task)
        db.session.commit()
        return jsonify({"message": "Tarefa adicionada!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@routes.route('/tasks', methods=['GET'])
def get_tasks():
        tasks = Task.query.all() 
        tasks_data = []
        
        for task in tasks:
            task_info = {
                "id": task.id,
                "title": task.title,
                "due_time": task.due_time.isoformat(),
                "completed": task.completed,
                "category": task.category.name if task.category else None,
                "priority": task.priority.level if task.priority else "Sem prioridade"
            }   
            tasks_data.append(task_info)

        return jsonify(tasks_data)


@routes.route('/tasks/<int:id>/complete', methods=['PUT'])
def complete_task(id):
    task = Task.query.get(id)
    if task:
        task.completed = True
        db.session.commit()
        return jsonify({"message": "Tarefa concluída!"})
    return jsonify({"error": "Tarefa não encontrada"}), 404
    

@routes.route('/notifications', methods=['GET'])
def get_notifications():
    try:
        now = datetime.now()
        print("Data e hora atuais:", now)
        pending_tasks = Task.query.filter(
            Task.completed == False,
            Task.due_time <= now
        ).all()
        print("Tarefas pendentes:", pending_tasks)

        notifications = [
            {"message": f'Lembrete: "{task.title}" está pendente!'}
            for task in pending_tasks
        ]
        return jsonify(notifications)
    except Exception as e:
        print(f"Erro ao buscar notificações: {e}")
        return jsonify({"error": "Erro interno ao buscar notificações."}), 500

@routes.route('/tasks/clear', methods=['DELETE'])
def clear_tasks():
    try:
        num_deleted = db.session.query(Task).delete()
        db.session.commit()
        return jsonify({"message": f"{num_deleted} tarefas removidas!"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), 500