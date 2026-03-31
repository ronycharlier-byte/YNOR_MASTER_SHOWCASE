const storageKey = "ynor_chat_history";
const briefKey = "ynor_brief_mode";
const chatStream = document.getElementById("chatStream");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const briefMode = document.getElementById("briefMode");
const confidenceBadge = document.getElementById("confidenceBadge");
let messages = JSON.parse(localStorage.getItem(storageKey) || "[]");
briefMode.checked = localStorage.getItem(briefKey) === "true";

function escapeHtml(value) {
    return String(value)
        .replaceAll("&", "&amp;")
        .replaceAll("<", "&lt;")
        .replaceAll(">", "&gt;")
        .replaceAll('"', "&quot;")
        .replaceAll("'", "&#39;");
}

function renderMessages() {
    chatStream.innerHTML = "";
    if (!messages.length) {
        chatStream.innerHTML = `
            <div class="bubble assistant">
                Your private intelligence workspace is ready.<br><br>
                Ask a question, and Ynor will combine corpus grounding with live web context.
            </div>
        `;
        return;
    }
    chatStream.innerHTML = messages.map(renderMessage).join("");
    chatStream.scrollTop = chatStream.scrollHeight;
}

function renderMessage(message) {
    const role = message.role === "user" ? "user" : "assistant";
    const sources = (message.sources || []).map((source, index) => `
        <a class="source-chip" href="${escapeHtml(source.url || "#")}" target="_blank" rel="noreferrer">
          <strong>[${index + 1}]</strong> ${escapeHtml(source.title || "Source")}
        </a>
    `).join("");
    const meta = message.confidence_label ? `
        <div class="assistant-meta">
          <span class="badge ${message.confidence_label.toLowerCase()}">${escapeHtml(message.confidence_score)} • ${escapeHtml(message.confidence_label)}</span>
        </div>
    ` : "";
    const sourceBlock = sources ? `<div class="sources">${sources}</div>` : "";
    return `
        <div class="bubble ${role}">
          ${escapeHtml(message.content)}
          ${meta}
          ${sourceBlock}
        </div>
    `;
}

function persist() {
    localStorage.setItem(storageKey, JSON.stringify(messages));
}

function setPrompt(text) {
    chatInput.value = text;
    chatInput.focus();
}

briefMode.addEventListener("change", () => {
    localStorage.setItem(briefKey, String(briefMode.checked));
});

chatInput.addEventListener("keydown", (event) => {
    if (event.key === "Enter" && !event.shiftKey) {
        event.preventDefault();
        sendMessage();
    }
});

async function sendMessage() {
    const text = chatInput.value.trim();
    if (!text) return;

    messages.push({ role: "user", content: text });
    messages.push({ role: "assistant", content: "Thinking across corpus and live web context..." });
    persist();
    renderMessages();
    chatInput.value = "";
    sendBtn.disabled = true;

    try {
        const response = await fetch("/api/assistant/chat", {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({
                messages: messages.filter((item) => item.content !== "Thinking across corpus and live web context..."),
                brief_mode: briefMode.checked,
            }),
        });
        const payload = await response.json();
        messages.pop();
        messages.push({
            role: "assistant",
            content: payload.answer || "No answer returned.",
            sources: payload.sources || [],
            confidence_score: payload.confidence_score,
            confidence_label: payload.confidence_label,
        });
        confidenceBadge.textContent = `${payload.confidence_score || "0.00"} • ${payload.confidence_label || "Low"}`;
        confidenceBadge.className = `badge ${(payload.confidence_label || "low").toLowerCase()}`;
    } catch (error) {
        messages.pop();
        messages.push({
            role: "assistant",
            content: `The assistant is temporarily unavailable. ${String(error)}`,
            sources: [],
            confidence_score: "0.00",
            confidence_label: "Low",
        });
    } finally {
        persist();
        renderMessages();
        sendBtn.disabled = false;
    }
}

window.setPrompt = setPrompt;
window.sendMessage = sendMessage;
renderMessages();
