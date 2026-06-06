const STORAGE_KEY = "todo_app_tasks_v1";

const priorityMeta = {
    high: { label: "高", weight: 3 },
    normal: { label: "通常", weight: 2 },
    low: { label: "低", weight: 1 },
};

const state = {
    tasks: loadTasks(),
    filter: "all",
    query: "",
    sort: "createdDesc",
};

const elements = {
    form: document.querySelector("#taskForm"),
    taskId: document.querySelector("#taskId"),
    title: document.querySelector("#taskTitle"),
    note: document.querySelector("#taskNote"),
    due: document.querySelector("#taskDue"),
    priority: document.querySelector("#taskPriority"),
    submitButton: document.querySelector("#submitButton"),
    cancelEditButton: document.querySelector("#cancelEditButton"),
    taskList: document.querySelector("#taskList"),
    emptyState: document.querySelector("#emptyState"),
    template: document.querySelector("#taskTemplate"),
    search: document.querySelector("#searchInput"),
    sort: document.querySelector("#sortSelect"),
    filterTabs: document.querySelectorAll(".filter-tab"),
    totalCount: document.querySelector("#totalCount"),
    activeCount: document.querySelector("#activeCount"),
    doneCount: document.querySelector("#doneCount"),
    progressValue: document.querySelector("#progressValue"),
    progressRing: document.querySelector(".progress-ring"),
    clearDone: document.querySelector("#clearDoneButton"),
    reset: document.querySelector("#resetButton"),
};

elements.form.addEventListener("submit", saveTask);
elements.cancelEditButton.addEventListener("click", resetForm);
elements.search.addEventListener("input", (event) => {
    state.query = event.target.value.trim().toLowerCase();
    render();
});
elements.sort.addEventListener("change", (event) => {
    state.sort = event.target.value;
    render();
});
elements.clearDone.addEventListener("click", clearCompleted);
elements.reset.addEventListener("click", resetAll);

elements.filterTabs.forEach((tab) => {
    tab.addEventListener("click", () => {
        state.filter = tab.dataset.filter;
        elements.filterTabs.forEach((item) => item.classList.toggle("active", item === tab));
        render();
    });
});

render();

function saveTask(event) {
    event.preventDefault();

    const title = elements.title.value.trim();
    if (!title) {
        elements.title.focus();
        return;
    }

    const id = elements.taskId.value;
    const now = new Date().toISOString();
    const payload = {
        title,
        note: elements.note.value.trim(),
        dueDate: elements.due.value,
        priority: elements.priority.value,
        updatedAt: now,
    };

    if (id) {
        state.tasks = state.tasks.map((task) => (
            task.id === id ? { ...task, ...payload } : task
        ));
    } else {
        state.tasks.unshift({
            id: createId(),
            completed: false,
            createdAt: now,
            ...payload,
        });
    }

    persist();
    resetForm();
    render();
}

function toggleTask(id) {
    const now = new Date().toISOString();
    state.tasks = state.tasks.map((task) => (
        task.id === id ? { ...task, completed: !task.completed, updatedAt: now } : task
    ));
    persist();
    render();
}

function editTask(id) {
    const task = state.tasks.find((item) => item.id === id);
    if (!task) {
        return;
    }

    elements.taskId.value = task.id;
    elements.title.value = task.title;
    elements.note.value = task.note;
    elements.due.value = task.dueDate;
    elements.priority.value = task.priority;
    elements.submitButton.querySelector("span:last-child").textContent = "更新";
    elements.cancelEditButton.classList.remove("hidden");
    elements.title.focus();
}

function deleteTask(id) {
    const task = state.tasks.find((item) => item.id === id);
    if (!task || !confirm(`「${task.title}」を削除しますか？`)) {
        return;
    }

    state.tasks = state.tasks.filter((item) => item.id !== id);
    persist();
    render();
}

function clearCompleted() {
    if (!state.tasks.some((task) => task.completed)) {
        return;
    }

    if (!confirm("完了済みのタスクを削除しますか？")) {
        return;
    }

    state.tasks = state.tasks.filter((task) => !task.completed);
    persist();
    render();
}

function resetAll() {
    if (state.tasks.length === 0 || !confirm("すべてのタスクを削除しますか？")) {
        return;
    }

    state.tasks = [];
    persist();
    resetForm();
    render();
}

function resetForm() {
    elements.form.reset();
    elements.taskId.value = "";
    elements.priority.value = "normal";
    elements.submitButton.querySelector("span:last-child").textContent = "追加";
    elements.cancelEditButton.classList.add("hidden");
}

function render() {
    const tasks = getVisibleTasks();
    renderStats();
    renderTasks(tasks);
}

function renderStats() {
    const total = state.tasks.length;
    const done = state.tasks.filter((task) => task.completed).length;
    const active = total - done;
    const progress = total === 0 ? 0 : Math.round((done / total) * 100);

    elements.totalCount.textContent = total;
    elements.activeCount.textContent = active;
    elements.doneCount.textContent = done;
    elements.progressValue.textContent = `${progress}%`;
    elements.progressRing.style.background = `conic-gradient(var(--primary) ${progress * 3.6}deg, #dfe7e5 0deg)`;
}

function renderTasks(tasks) {
    elements.taskList.replaceChildren();
    elements.emptyState.classList.toggle("hidden", tasks.length > 0);

    const fragment = document.createDocumentFragment();
    tasks.forEach((task) => {
        const item = elements.template.content.firstElementChild.cloneNode(true);
        const isDueToday = isToday(task.dueDate);
        const isTaskOverdue = isOverdue(task);

        item.classList.toggle("done", task.completed);
        item.classList.toggle("overdue", isTaskOverdue);
        item.querySelector("h2").textContent = task.title;
        item.querySelector(".task-note").textContent = task.note;

        const badge = item.querySelector(".priority-badge");
        badge.textContent = priorityMeta[task.priority].label;
        badge.classList.add(`priority-${task.priority}`);

        const dueDate = item.querySelector(".due-date");
        dueDate.textContent = task.dueDate ? `期限 ${formatDate(task.dueDate)}` : "期限なし";
        dueDate.classList.toggle("today", isDueToday && !task.completed);
        dueDate.classList.toggle("overdue", isTaskOverdue);

        item.querySelector(".created-date").textContent = `作成 ${formatDateTime(task.createdAt)}`;
        item.querySelector(".check-button").addEventListener("click", () => toggleTask(task.id));
        item.querySelector(".edit-button").addEventListener("click", () => editTask(task.id));
        item.querySelector(".delete-button").addEventListener("click", () => deleteTask(task.id));

        fragment.appendChild(item);
    });

    elements.taskList.appendChild(fragment);
}

function getVisibleTasks() {
    return state.tasks
        .filter((task) => matchesFilter(task))
        .filter((task) => matchesQuery(task))
        .sort(compareTasks);
}

function matchesFilter(task) {
    if (state.filter === "active") {
        return !task.completed;
    }
    if (state.filter === "done") {
        return task.completed;
    }
    if (state.filter === "today") {
        return isToday(task.dueDate);
    }
    if (state.filter === "overdue") {
        return isOverdue(task);
    }
    return true;
}

function matchesQuery(task) {
    if (!state.query) {
        return true;
    }

    return `${task.title} ${task.note}`.toLowerCase().includes(state.query);
}

function compareTasks(a, b) {
    if (state.sort === "dueAsc") {
        return dueTime(a) - dueTime(b) || newestFirst(a, b);
    }
    if (state.sort === "priorityDesc") {
        return priorityMeta[b.priority].weight - priorityMeta[a.priority].weight || newestFirst(a, b);
    }
    return newestFirst(a, b);
}

function newestFirst(a, b) {
    return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
}

function dueTime(task) {
    return task.dueDate ? new Date(`${task.dueDate}T00:00:00`).getTime() : Number.MAX_SAFE_INTEGER;
}

function isToday(dateString) {
    if (!dateString) {
        return false;
    }

    const today = new Date();
    const localToday = [
        today.getFullYear(),
        String(today.getMonth() + 1).padStart(2, "0"),
        String(today.getDate()).padStart(2, "0"),
    ].join("-");

    return dateString === localToday;
}

function isOverdue(task) {
    if (!task.dueDate || task.completed) {
        return false;
    }

    const today = new Date();
    today.setHours(0, 0, 0, 0);
    return new Date(`${task.dueDate}T00:00:00`) < today;
}

function formatDate(dateString) {
    const date = new Date(`${dateString}T00:00:00`);
    return new Intl.DateTimeFormat("ja-JP", {
        month: "numeric",
        day: "numeric",
        weekday: "short",
    }).format(date);
}

function formatDateTime(dateString) {
    return new Intl.DateTimeFormat("ja-JP", {
        month: "numeric",
        day: "numeric",
        hour: "2-digit",
        minute: "2-digit",
    }).format(new Date(dateString));
}

function loadTasks() {
    try {
        const tasks = JSON.parse(localStorage.getItem(STORAGE_KEY));
        return Array.isArray(tasks) ? tasks : [];
    } catch {
        return [];
    }
}

function persist() {
    localStorage.setItem(STORAGE_KEY, JSON.stringify(state.tasks));
}

function createId() {
    if (crypto.randomUUID) {
        return crypto.randomUUID();
    }

    return `${Date.now()}-${Math.random().toString(16).slice(2)}`;
}
