const API = "https://daytasks.onrender.com/tasks";

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
        <span><b>${task.title}</b></span>
        <span>Status: ${task.completed ? "Completed" : "Pending"}</span>
        <button onclick="markDone('${task.id}')">Done</button>
        <button onclick="deleteTask('${task.id}')">Delete</button>
      </div>
    `;
  });
}

async function addTask() {
  const title = document.getElementById("title").value;

  await fetch(API, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title })
  });

  document.getElementById("title").value = "";
  loadTasks();
}

async function markDone(id) {
  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: {"Content-Type": "application/json"},
  });
  loadTasks();
}

async function deleteTask(id) {
  await fetch(`${API}/${id}`, {
    method: "DELETE"
  });
  loadTasks();
}
