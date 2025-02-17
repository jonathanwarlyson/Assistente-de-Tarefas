const socket = io('http://localhost:5000');

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

    if (container && text) {
        text.textContent = message;
        container.classList.add('show');
        
        setTimeout(() => {
            container.classList.remove('show');
        }, 5000);
    }

    if (Notification.permission === 'granted') {
        new Notification(message);
    } else if (Notification.permission !== 'denied') {
        Notification.requestPermission();
    }
}

function renderTasks(tasks) {
    const priorityOrder = { "Alta": 3, "Média": 2, "Baixa": 1};
    const taskList = document.getElementById('taskList');

    if (!taskList || !Array.isArray(tasks)) {
        console.error("Tasks não é um array:", tasks);
        return;
    }

    tasks.sort((a, b) => (priorityOrder[b.priority] || 0) - (priorityOrder[a.priority] || 0));

    taskList.innerHTML = tasks.map(task => `
        <div class="task-item ${task.completed ? 'completed' : ''}">
            <div>
                <h3>${task.title}</h3>
                <p>Prazo: ${new Date(task.due_time).toLocaleString('pt-BR')}</p>
                <p>Categoria: ${task.category || 'Sem categoria'}</p>
                <p>Prioridade: ${task.priority || 'Sem prioridade'}</p>
            </div>
            ${!task.completed ?
                `<button onclick="completeTask(${task.id})">Concluir</button>` :
                '<span>Concluída</span>'
            }
        </div>
    `).join('');
}

window.completeTask = (id) => {
    fetch(`http://localhost:5000/tasks/${id}/complete`, {
        method: 'PUT'
    })
    .then(response => response.json())
    .then(tasks => renderTasks(tasks))
    .catch(error => console.error('Erro ao completar tarefa:', error));
}; 

window.clearTasks = function() {
    if (!confirm("Tem certeza que deseja apagar todas as tarefas?")) return;

    fetch('http://localhost:5000/tasks/clear', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        alert(data.message);
        const taskList = document.getElementById('taskList');
        if (taskList) taskList.innerHTML = '';
    })
    .catch(error => console.error('Erro ao limpar tarefas:', error));
}

window.clearCategories = function() {
    if(!confirm("Tem certeza que deseja apagar todas categorias?")) return;

    fetch('http://localhost:5000/categories/clear', {
        method: 'DELETE'
    })
    .then(response => response.json())
    .then(data => {
        if (data.error) {
            alert(data.error);
        } else {
            alert(data.message);
            loadCategories();
        }
    })
    .catch (error => console.error('Erro ao limpar tarefas: ', error));
}

document.addEventListener('DOMContentLoaded', () => {
    checkNotifications();
    setInterval(checkNotifications, 60000);
    
    const taskForm = document.getElementById('taskForm');
    const taskList = document.getElementById('taskList');
    const clearTasksBtn = document.getElementById('clearTasksBtn');
    const taskCategory = document.getElementById('taskCategory');
    const priorityId = document.getElementById('taskPriority').value;
    const newCategoryInput = document.getElementById('newCategoryInput');
    const addCategoryBtn = document.getElementById('addCategoryBtn');
    const clearCategoriesBtn = document.getElementById('clearCategoriesBtn');

    function loadPriorities() {
        fetch('http://localhost:5000/priorities')
        .then(response => response.json())
        .then(priorities => {
            const taskPriority = document.getElementById('taskPriority');
            taskPriority.innerHTML = `<option value="">Selecione uma prioridade</option>`;

            priorities.forEach(priority => {
                const option = document.createElement('option');
                option.value = priority.id;
                option.textContent = priority.name;
                taskPriority.appendChild(option);
            });
        })
        .catch(error => console.error("Erro ao carregar prioridades:", error));
    }

    function loadCategories() {
        fetch('http://localhost:5000/categories')
            .then(response => response.json())
            .then(categories => {
                taskCategory.innerHTML = `<option value="">Selecione uma categoria</option>
                <option value="new">+ Criar nova categoria</option>`;

                categories.forEach(category => {
                    const option = document.createElement('option');
                    option.value = category.id;
                    option.textContent = category.name;
                    taskCategory.appendChild(option);
                });
            });
        console.log("Carregando categorias após criação...")
    }

    taskCategory.addEventListener('change', () => {
        if (taskCategory.value === "new") {
            newCategoryInput.style.display = "block";
            addCategoryBtn.style.display = "block";
            newCategoryInput.focus();
        } else {
            newCategoryInput.style.display = "none";
            addCategoryBtn.style.display = "none";
        }
    });

    addCategoryBtn.addEventListener('click', () => {
        const newCategoryName = newCategoryInput.value.trim();
        if (newCategoryName === "") {
            alert("Digite um nome para a categoria.");
            return;
        }

        fetch('http://localhost:5000/categories', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ name: newCategoryName })
        })
        .then(response => response.json())
        .then(data => {
            if (data.id) {
                loadCategories();
                taskCategory.value = data.id;
                newCategoryInput.style.display = "none";
                addCategoryBtn.style.display = "none";
                newCategoryInput.value = "";
            } else {
                alert("Erro ao adicionar categoria.");
            }
        });
    });

    fetch('http://localhost:5000/categories')
        .then(response => response.json())
        .then(categories => {
            categories.forEach(category => {
                const option = document.createElement('option');
                option.value = category.id;
                option.textContent = category.name;
                taskCategory.appendChild(option);
            });
        });


    if (taskForm) {
        taskForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const title = document.getElementById('taskTitle')?.value;
            const dueTime = document.getElementById('taskDueTime')?.value;
            const priorityId = document.getElementById('taskPriority').value || null;
            const categoryId = taskCategory.value || null; 

            if (!title || !dueTime) {
                console.error('Título ou prazo inválidos');
                return;
            }

            fetch('http://localhost:5000/tasks', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({
                    title: title,
                    due_time: dueTime.replace('T', ' '),
                    category_id: categoryId,
                    priority_id: priorityId
                })
            })
            .then(response => response.json())
            .then(data => {
                if (data.error) {
                    console.error("Erro ao criar tarefa:", data.error);
                    alert("Erro: " + data.error);
                } else if (Array.isArray(data)) {
                    renderTasks(data);
                } else {
                console.error("Resposta inesperada:", data);
                }
            }) 
            .catch(error => console.error('Erro ao adicionar tarefa:', error));
        });
    }

    if (clearTasksBtn) {
        clearTasksBtn.addEventListener('click', clearTasks);
    }

    if(clearCategoriesBtn) {
        clearCategoriesBtn.addEventListener('click', clearCategories);
    }
    
    if (taskList) {
        fetch('http://localhost:5000/tasks')
            .then(response => response.json())
            .then(tasks => renderTasks(tasks))
            .catch(error => console.error('Erro:', error));
    }
});