const API = "https://daytasks.onrender.com";

// Load tasks on page load
window.onload = loadTasks;

async function loadTasks() {
  const res = await fetch(API);
  const tasks = await res.json();

  const list = document.getElementById("task-list");
  list.innerHTML = "";

  tasks.forEach(task => {
    list.innerHTML += `
      <div class="task">
        <span><b>${task.title}</b> – ${task.description}</span>
        <span>Status: ${task.completed ? "Completed" : "Pending"}</span>
        <button onclick="markDone('${task._id || task.id}')">Done</button>
        <button onclick="deleteTask('${task._id || task.id}')">Delete</button>
      </div>
    `;
  });
}

async function addTask() {
  const title = document.getElementById("title").value;
  const description = document.getElementById("description").value;

  await fetch(API, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title, description, completed: false })
  });

  document.getElementById("title").value = "";
  document.getElementById("description").value = "";
  loadTasks();
}

async function markDone(id) {
  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ completed: true })
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${API}/${id}`, {
    method: "DELETE"
  });
  loadTasks();
}
