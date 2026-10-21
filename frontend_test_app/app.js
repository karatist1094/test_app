// Адрес бэкенда (порт 8080 открыт в docker-compose)
const API = "http://localhost:8080";

const errorBox = document.getElementById("error");

function showError(message) {
  errorBox.textContent = message;
  errorBox.style.display = "block";
}

function clearError() {
  errorBox.style.display = "none";
}

// Общая функция запросов: бросает ошибку, если бэк ответил не успехом
async function request(path, options = {}) {
  let response;
  try {
    response = await fetch(API + path, {
      headers: { "Content-Type": "application/json" },
      ...options,
    });
  } catch (e) {
    throw new Error("Не удалось связаться с бэкендом (" + API + "). Он запущен?");
  }
  if (!response.ok) {
    throw new Error("Ошибка " + response.status + " при запросе " + path);
  }
  // 204 No Content (удаление) — тела нет
  return response.status === 204 ? null : response.json();
}

// Обёртка: выполняет действие и обновляет списки, ошибки показывает вверху
async function run(action) {
  try {
    clearError();
    await action();
    await loadAll();
  } catch (e) {
    showError(e.message);
  }
}

// ---------- Рисование списков ----------
function renderEmpty(list, text) {
  const li = document.createElement("li");
  li.className = "empty";
  li.textContent = text;
  list.appendChild(li);
}

function makeIconButton(symbol, label, extraClass, onClick) {
  const btn = document.createElement("button");
  btn.type = "button";
  btn.textContent = symbol;
  btn.title = label;
  btn.setAttribute("aria-label", label);
  btn.className = "icon " + extraClass;
  btn.addEventListener("click", onClick);
  return btn;
}

function renderProgress(tasks) {
  const done = tasks.filter((t) => t.completed).length;
  const percent = tasks.length ? Math.round((done / tasks.length) * 100) : 0;
  document.getElementById("task-count").textContent = tasks.length;
  document.getElementById("progress-text").textContent =
    "Выполнено " + done + " из " + tasks.length + " (" + percent + "%)";
  document.getElementById("progress-fill").style.width = percent + "%";
}

function renderTasks(tasks) {
  const list = document.getElementById("tasks");
  list.innerHTML = "";
  renderProgress(tasks);
  if (tasks.length === 0) return renderEmpty(list, "Задач пока нет — добавь первую");

  tasks.forEach((task) => {
    const li = document.createElement("li");
    if (task.completed) li.classList.add("done");

    const checkbox = document.createElement("input");
    checkbox.type = "checkbox";
    checkbox.checked = task.completed;
    checkbox.addEventListener("change", () =>
      run(() => request("/tasks/" + task.id, {
        method: "PATCH",
        body: JSON.stringify({ completed: checkbox.checked }),
      }))
    );

    const title = document.createElement("span");
    title.className = "title";
    title.textContent = task.title; // textContent — безопасно от вставки HTML

    const actions = document.createElement("div");
    actions.className = "actions";

    const edit = makeIconButton("✎", "Изменить", "", () => {
      const newTitle = prompt("Новое название задачи:", task.title);
      if (newTitle && newTitle.trim() && newTitle !== task.title) {
        run(() => request("/tasks/" + task.id, {
          method: "PATCH",
          body: JSON.stringify({ title: newTitle.trim() }),
        }));
      }
    });

    const del = makeIconButton("✕", "Удалить", "danger", () =>
      run(() => request("/tasks/" + task.id, { method: "DELETE" }))
    );

    actions.append(edit, del);
    li.append(checkbox, title, actions);
    list.appendChild(li);
  });
}

function renderCategories(categories) {
  const list = document.getElementById("categories");
  list.innerHTML = "";
  document.getElementById("category-count").textContent = categories.length;
  if (categories.length === 0) return renderEmpty(list, "Категорий пока нет");

  categories.forEach((category) => {
    const li = document.createElement("li");

    const dot = document.createElement("span");
    dot.className = "category-dot";

    const name = document.createElement("span");
    name.className = "title";
    name.textContent = category.name;

    const actions = document.createElement("div");
    actions.className = "actions";

    const edit = makeIconButton("✎", "Изменить", "", () => {
      const newName = prompt("Новое название категории:", category.name);
      if (newName && newName.trim() && newName !== category.name) {
        run(() => request("/categories/" + category.id, {
          method: "PATCH",
          body: JSON.stringify({ name: newName.trim() }),
        }));
      }
    });

    const del = makeIconButton("✕", "Удалить", "danger", () =>
      run(() => request("/categories/" + category.id, { method: "DELETE" }))
    );

    actions.append(edit, del);
    li.append(dot, name, actions);
    list.appendChild(li);
  });
}

// ---------- Загрузка данных ----------
async function loadAll() {
  const [tasks, categories] = await Promise.all([
    request("/tasks"),
    request("/categories"),
  ]);
  renderTasks(tasks);
  renderCategories(categories);
}

// ---------- Формы добавления ----------
document.getElementById("task-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.getElementById("task-title");
  const title = input.value.trim();
  if (!title) return;
  run(async () => {
    await request("/tasks", { method: "POST", body: JSON.stringify({ title }) });
    input.value = "";
  });
});

document.getElementById("category-form").addEventListener("submit", (event) => {
  event.preventDefault();
  const input = document.getElementById("category-name");
  const name = input.value.trim();
  if (!name) return;
  run(async () => {
    await request("/categories", { method: "POST", body: JSON.stringify({ name }) });
    input.value = "";
  });
});

// Первая загрузка
run(async () => {});