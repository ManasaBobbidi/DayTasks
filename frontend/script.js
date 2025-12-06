const API = "https://daytasks.onrender.com/tasks";

window.onload = loadTasks;

// Load tasks
async function loadTasks() {
  const res = await fetch(API);
  const tasks = await res.json();

  const list = document.getElementById("task-list");
  list.innerHTML = "";

  tasks.forEach(task => {
    list.innerHTML += `
      <div class="task">
        <span><b>${task.title}</b></span>
        <span>Status: ${task.completed ? "✔ Completed" : "❌ Pending"}</span>
        <button onclick="markDone('${task.id}', ${task.completed})">
          ${task.completed ? "Undo" : "Done"}
        </button>
        <button onclick="deleteTask('${task.id}')">Delete</button>
      </div>
    `;
  });
}

// Add task
async function addTask() {
  const title = document.getElementById("title").value.trim();
  if (!title) return alert("Enter a task!");

  await fetch(API, {
    method: "POST",
    headers: {"Content-Type": "application/json"},
    body: JSON.stringify({ title })
  });

  document.getElementById("title").value = "";
  loadTasks();
}

// Mark Done (toggle completed)
async function markDone(id, currentStatus) {
  await fetch(`${API}/${id}`, {
    method: "PUT",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ completed: !currentStatus })
  });
  loadTasks();
}

// Delete task
async function deleteTask(id) {
  await fetch(`${API}/${id}`, {
    method: "DELETE"
  });
  loadTasks();
}
