// TaskFlow 프론트엔드 로직 (Vanilla JS, jQuery 금지)

const API_BASE = "/api/tasks";

// 상태 → 화면 구성 정보 매핑
const statusMeta = {
  todo: { column: "colTodo", count: "countTodo", label: "대기" },
  doing: { column: "colDoing", count: "countDoing", label: "진행중" },
  done: { column: "colDone", count: "countDone", label: "완료" },
};

// 우선순위 → 배지 스타일/라벨 매핑
const priorityMeta = {
  low: { label: "낮음", badge: "bg-slate-200 text-slate-600" },
  medium: { label: "보통", badge: "bg-sky-200 text-sky-700" },
  high: { label: "높음", badge: "bg-rose-200 text-rose-700" },
};

// 상태 변경 버튼에 사용할 다음 상태 흐름
const nextStatus = { todo: "doing", doing: "done", done: "todo" };
const nextLabel = { todo: "시작", doing: "완료", done: "되돌리기" };

// 서버에서 업무 목록을 받아 화면을 다시 그린다.
async function loadTasks() {
  const res = await fetch(API_BASE);
  if (!res.ok) {
    alert("업무 목록을 불러오지 못했습니다.");
    return;
  }
  const tasks = await res.json();
  renderTasks(tasks);
}

// 전체 보드를 다시 렌더링한다.
function renderTasks(tasks) {
  // 각 컬럼 비우기
  Object.values(statusMeta).forEach((meta) => {
    document.getElementById(meta.column).innerHTML = "";
  });

  const counts = { todo: 0, doing: 0, done: 0 };

  tasks.forEach((task) => {
    const meta = statusMeta[task.status];
    if (!meta) return;
    counts[task.status] += 1;
    document.getElementById(meta.column).appendChild(createCard(task));
  });

  // 카운트 갱신
  Object.entries(statusMeta).forEach(([status, meta]) => {
    document.getElementById(meta.count).textContent = counts[status];
  });
}

// 업무 카드 DOM 을 생성한다.
function createCard(task) {
  const card = document.createElement("div");
  card.className =
    "bg-white rounded-lg shadow-sm border border-slate-200 p-3 flex flex-col gap-2";

  const pMeta = priorityMeta[task.priority] || priorityMeta.medium;

  // 제목 + 우선순위 배지
  const top = document.createElement("div");
  top.className = "flex items-start justify-between gap-2";

  const title = document.createElement("p");
  title.className = "font-medium text-slate-800 break-words";
  title.textContent = task.title;
  if (task.status === "done") {
    title.classList.add("line-through", "text-slate-400");
  }

  const badge = document.createElement("span");
  badge.className = `shrink-0 text-xs rounded-full px-2 py-0.5 ${pMeta.badge}`;
  badge.textContent = pMeta.label;

  top.append(title, badge);
  card.appendChild(top);

  // 설명(있을 때만)
  if (task.description) {
    const desc = document.createElement("p");
    desc.className = "text-sm text-slate-500 break-words";
    desc.textContent = task.description;
    card.appendChild(desc);
  }

  // 액션 버튼: 상태 변경 / 삭제
  const actions = document.createElement("div");
  actions.className = "flex items-center justify-between mt-1";

  const moveBtn = document.createElement("button");
  moveBtn.className =
    "text-xs font-medium text-indigo-600 hover:text-indigo-800 transition-colors";
  moveBtn.textContent = `→ ${nextLabel[task.status]}`;
  moveBtn.addEventListener("click", () => changeStatus(task.id, nextStatus[task.status]));

  const delBtn = document.createElement("button");
  delBtn.className = "text-xs text-rose-500 hover:text-rose-700 transition-colors";
  delBtn.textContent = "삭제";
  delBtn.addEventListener("click", () => deleteTask(task.id));

  actions.append(moveBtn, delBtn);
  card.appendChild(actions);

  return card;
}

// 업무 추가
async function addTask(title, priority) {
  const res = await fetch(API_BASE, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ title, priority }),
  });
  if (!res.ok) {
    alert("업무 추가에 실패했습니다.");
    return;
  }
  await loadTasks();
}

// 상태 변경
async function changeStatus(id, status) {
  const res = await fetch(`${API_BASE}/${id}/status`, {
    method: "PATCH",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ status }),
  });
  if (!res.ok) {
    alert("상태 변경에 실패했습니다.");
    return;
  }
  await loadTasks();
}

// 업무 삭제
async function deleteTask(id) {
  if (!confirm("이 업무를 삭제할까요?")) return;
  const res = await fetch(`${API_BASE}/${id}`, { method: "DELETE" });
  if (!res.ok) {
    alert("삭제에 실패했습니다.");
    return;
  }
  await loadTasks();
}

// 폼 제출 핸들러 등록
document.getElementById("taskForm").addEventListener("submit", (event) => {
  event.preventDefault();
  const titleInput = document.getElementById("titleInput");
  const priorityInput = document.getElementById("priorityInput");
  const title = titleInput.value.trim();
  if (!title) return;
  addTask(title, priorityInput.value);
  titleInput.value = "";
  priorityInput.value = "medium";
  titleInput.focus();
});

// 최초 로딩
loadTasks();
