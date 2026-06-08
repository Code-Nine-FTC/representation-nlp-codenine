const messagesEl = document.getElementById("messages");
const composerEl = document.getElementById("composer");
const inputEl = document.getElementById("input");
const sendBtn = document.getElementById("sendBtn");
const newChatBtn = document.getElementById("newChatBtn");
const errorTextEl = document.getElementById("errorText");
const statusDotEl = document.getElementById("statusDot");
const statusTextEl = document.getElementById("statusText");
const exampleChips = document.querySelectorAll("[data-query]");

function setStatus(kind, text) {
  statusDotEl.classList.remove("status--busy", "status--ok", "status--err");
  if (kind) statusDotEl.classList.add(`status--${kind}`);
  statusTextEl.textContent = text || "Pronto";
}

function escapeHtml(s) {
  return String(s)
    .replaceAll("&", "&amp;")
    .replaceAll("<", "&lt;")
    .replaceAll(">", "&gt;")
    .replaceAll('"', "&quot;")
    .replaceAll("'", "&#039;");
}

function scrollToBottom() {
  messagesEl.scrollTop = messagesEl.scrollHeight;
}

function buildSqlBlock(sql) {
  const code = document.createElement("div");
  code.className = "code";
  code.innerHTML = `
    <div class="code__head">
      <span>SQL escolhido</span>
      <span>read-only</span>
    </div>
    <pre><code>${escapeHtml(sql)}</code></pre>
  `;
  return code;
}

function buildJsonDetails(result) {
  const details = document.createElement("details");
  details.className = "code";
  details.innerHTML = `
    <summary class="code__head">
      <span>JSON bruto</span>
      <span>clique para expandir</span>
    </summary>
    <pre><code>${escapeHtml(JSON.stringify(result, null, 2))}</code></pre>
  `;
  return details;
}

function buildCountBlock(data) {
  const wrap = document.createElement("div");
  wrap.className = "count";

  const isObj = data !== null && typeof data === "object";
  const total = isObj && "total" in data ? data.total : data;
  const rows  = isObj && Array.isArray(data.rows) ? data.rows : [];

  const header = document.createElement("div");
  header.className = "count__header";
  header.innerHTML = `
    <div class="count__num">${escapeHtml(String(total))}</div>
    <div class="count__label">resultado da contagem</div>
  `;
  wrap.appendChild(header);

  if (rows.length > 0) {
    const summary = document.createElement("div");
    summary.className = "results__summary";
    summary.textContent = `${rows.length} foto(s)`;
    wrap.appendChild(summary);

    const grid = document.createElement("div");
    grid.className = "grid grid--compact";
    rows.forEach((row) => grid.appendChild(buildPersonCard(row)));
    wrap.appendChild(grid);
  }

  return wrap;
}

function buildPersonCard(row) {
  const card = document.createElement("article");
  card.className = "card";
  const img = row.caminho_imagem || "";
  const nome = row.nome || "—";
  const etnia = row.etnia || "—";
  const cabelo = row.cor_cabelo || "—";
  const label = row.label_etaria || "—";
  const idadeTag = row.idade != null ? ` · ${row.idade} anos` : "";
  card.innerHTML = `
    <div class="card__media">
      <img src="${escapeHtml(img)}" alt="${escapeHtml(nome)}" loading="lazy"
           onerror="this.style.opacity='0.35'"/>
    </div>
    <div class="card__body">
      <div class="card__name">${escapeHtml(nome)}</div>
      <div class="card__meta">
        <span class="tag">etnia: ${escapeHtml(etnia)}</span>
        <span class="tag">cabelo: ${escapeHtml(cabelo)}</span>
        <span class="tag">${escapeHtml(label)}${escapeHtml(idadeTag)}</span>
      </div>
    </div>
  `;
  return card;
}

function buildRowsGrid(rows) {
  const wrap = document.createElement("div");
  wrap.className = "results";
  if (!rows || rows.length === 0) {
    wrap.innerHTML = `<div class="results__empty">Nenhum resultado encontrado.</div>`;
    return wrap;
  }
  const grid = document.createElement("div");
  grid.className = "grid";
  rows.forEach((row) => grid.appendChild(buildPersonCard(row)));
  const summary = document.createElement("div");
  summary.className = "results__summary";
  summary.textContent = `${rows.length} resultado(s)`;
  wrap.appendChild(summary);
  wrap.appendChild(grid);
  return wrap;
}

function addMessage({ role, text, meta, sql, kind, result }) {
  const wrapper = document.createElement("div");
  wrapper.className = `msg msg--${role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg__avatar";
  avatar.textContent = role === "user" ? "U" : "A";

  const bubble = document.createElement("div");
  bubble.className = "bubble";

  if (text) {
    const t = document.createElement("div");
    t.className = "bubble__text";
    t.textContent = text;
    bubble.appendChild(t);
  }

  if (meta) {
    const m = document.createElement("div");
    m.className = "bubble__meta";
    m.textContent = meta;
    bubble.appendChild(m);
  }

  if (sql) bubble.appendChild(buildSqlBlock(sql));

  if (kind === "count" && result !== undefined && result !== null) {
    bubble.appendChild(buildCountBlock(result));
  } else if (kind === "rows" && Array.isArray(result)) {
    bubble.appendChild(buildRowsGrid(result));
  }

  if (result !== undefined && result !== null) {
    bubble.appendChild(buildJsonDetails(result));
  }

  wrapper.appendChild(avatar);
  wrapper.appendChild(bubble);
  messagesEl.appendChild(wrapper);
  scrollToBottom();
}

function setError(msg) {
  errorTextEl.textContent = msg || "";
  if (msg) setStatus("err", "Erro");
}

function resetChat() {
  messagesEl.innerHTML = "";
  setError("");
  setStatus(null, "Pronto");
  addMessage({
    role: "bot",
    text:
      "Oi! Eu sou a interface da busca semântica do PC7.\n\nPergunte algo sobre as pessoas cadastradas (por etnia, cor de cabelo ou faixa etária) e eu retorno a SQL escolhida + as fotos correspondentes.",
  });
  inputEl.focus();
}

async function sendQuery(query) {
  setError("");
  setStatus("busy", "Pensando…");
  sendBtn.disabled = true;

  try {
    const res = await fetch("/search", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ query }),
    });

    const data = await res.json().catch(() => ({}));
    if (!res.ok) {
      throw new Error(data?.error || `Erro HTTP ${res.status}`);
    }

    if (data.query_interpretada === null) {
      addMessage({
        role: "bot",
        text: data.mensagem || "Não entendi a pergunta.",
        meta: `Score máximo: ${data.score}`,
      });
    } else {
      addMessage({
        role: "bot",
        text: "Aqui está o que eu encontrei:",
        meta: `Intent #${data.query_interpretada} · score ${data.score} · tipo ${data.kind}`,
        sql: data.sql,
        kind: data.kind,
        result: data.resultado,
      });
    }

    setStatus("ok", "Pronto");
  } catch (e) {
    setError(e?.message || "Falha ao chamar /search");
  } finally {
    sendBtn.disabled = false;
    setStatus(sendBtn.disabled ? "busy" : null, sendBtn.disabled ? "Pensando…" : "Pronto");
  }
}

function autoGrow() {
  inputEl.style.height = "auto";
  inputEl.style.height = Math.min(inputEl.scrollHeight, 160) + "px";
}

composerEl.addEventListener("submit", async (ev) => {
  ev.preventDefault();
  const query = (inputEl.value || "").trim();
  if (!query) return;

  addMessage({ role: "user", text: query });
  inputEl.value = "";
  autoGrow();
  await sendQuery(query);
});

inputEl.addEventListener("input", autoGrow);
inputEl.addEventListener("keydown", (ev) => {
  if (ev.key === "Enter" && !ev.shiftKey) {
    ev.preventDefault();
    composerEl.requestSubmit();
  }
});

if (newChatBtn) {
  newChatBtn.addEventListener("click", resetChat);
}

exampleChips.forEach((chip) => {
  chip.addEventListener("click", () => {
    const query = chip.getAttribute("data-query") || "";
    inputEl.value = query;
    autoGrow();
    inputEl.focus();
    inputEl.setSelectionRange(query.length, query.length);
  });
});

resetChat();
