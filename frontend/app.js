const socket = io('http://localhost:5000');

document.addEventListener('DOMContentLoaded', () => {
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');

    fetch('http://localhost:5000/tasks')
        .then(response => response.json())
        .then(tasks => renderTasks(tasks))
        .catch(error => console.error('Erro:', error));

    taskForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const title = document.getElementById('taskTitle').value;
        const dueTime = document.getElementById('taskDueTime').value;

        fetch('http://localhost:5000/tasks', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                title: title,
                due_time: dueTime.replace('T', ' ')
            })
        }).then(() => fetch('http://localhost:5000/tasks'))
        .then(response => response.json())
        .then(tasks => renderTasks(tasks));
    });

    function renderTasks(tasks) {
        taskList.innerHTML = tasks.map(task =>`
            <div class="task-item ${task.completed ? 'completed' : ''}">
                <div>
                    <h3>${task.title}</h3>
                    <p>Prazo: ${new Date(task.due_time).toLocaleString('pt-BR')}</p>
                </div>
                ${!task.completed ?
                    `<button onclick="completeTask(${task.id})">Concluir</button>` :
                    '<span>Concluída</span>'}
            </div>
        `).join('');
    }

    function checkNotifications() {
        fetch('http://localhost:5000/notifications')
        .then(response => response.json())
        .then(notifications => {
            notifications.forEach(notification => {
                showNotification(notification.message);
            });
        })
        .catch(error => console.error('Erro ao buscar notificações:', error));
    }

    function showNotification(message) {
        const container = document.getElementById('notificationContainer');
        const text = document.getElementById('notificationText');

        text.textContent = message;
        container.classList.add('show');

        setTimeout(() => {
            container.classList.remove('show');
        }, 5000);

        if (Notification.permission === 'granted') {
            new Notification(message);
        } else if (Notification.permission !== 'denied') {
            Notification.requestPermission();
        }
    }

setInterval(checkNotifications, 60000);
});

window.completeTask = (id) => {
    fetch(`http://localhost:5000/tasks/${id}/complete`, {
        method: 'PUT'
    }).then(() => fetch('http://localhost:5000/tasks'))
    .then(response => response.json())
    .then(tasks => renderTasks(tasks));
};

window.clearTasks = function() {
    if (!confirm("Tem certeza que deseja apagar todas as tarefas?")) return;

    fetch('http://localhost:5000/tasks/clear', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        document.getElementById('taskList').innerHTML = '';
    })
    .catch(error => console.error('Erro ao limpar tarefas:', error));
}

document.addEventListener('DOMContentLoaded', () => {
    checkNotifications();
    document.getElementById('clearTasksBtn').addEventListener('click', clearTasks);
});