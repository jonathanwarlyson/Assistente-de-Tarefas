from flask_sqlalchemy import SQLAlchemy
<<<<<<< HEAD
from sqlalchemy import Enum
=======
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b

db = SQLAlchemy()

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)

<<<<<<< HEAD
class Priority(db.Model):
    __tablename__ = 'priorities'

    id = db.Column(db.Integer, primary_key=True)
    level = db.Column(Enum('Baixa', 'Média', 'Alta', name="priority-levels"), nullable=False)
    tasks = db.relationship('Task', back_populates='priority')

    def __repr__(self):
        return f'<Priority {self.level}>'

class Task(db.Model): 
    __tablename__ = 'tasks'

=======
class Task(db.Model): 
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False) #titulo da tarefa
    due_time = db.Column(db.DateTime, nullable=False) #prazo (data/hora)
    completed = db.Column(db.Boolean, default=False) #status
    category_id = db.Column(db.Integer, db.ForeignKey('category.id'), nullable=True)
<<<<<<< HEAD
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
    priority_id = db.Column(db.Integer, db.ForeignKey('priorities.id'), nullable=True)
    priority = db.relationship('Priority', back_populates='tasks')
=======
    category = db.relationship('Category', backref=db.backref('tasks', lazy=True))
>>>>>>> 0b90993ae2fc6feeda62495586b191e9498d960b
