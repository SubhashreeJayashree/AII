const form = document.getElementById("chatForm");
const chatWindow = document.getElementById("chatWindow");
const msgInput = document.getElementById("msg");
let history = [];
function append(role, text) {
  const el = document.createElement("div");
  el.className = role === "user" ? "text-end mb-2" : "text-start mb-2";
  el.innerHTML = `<div class="d-inline-block p-2 rounded" style="background:${role==="user"?"#0d6efd":"#e9ecef"}; color:${role==="user"?"white":"black"}">${text}</div>`;
  chatWindow.appendChild(el); chatWindow.scrollTop = chatWindow.scrollHeight;
}
form.addEventListener("submit", async (e) => {
  e.preventDefault();
  const text = msgInput.value.trim(); if (!text) return;
  append("user", text); history.push({ role: "user", content: text }); msgInput.value = "";
  try {
    const res = await fetch("/api/chat", { method: "POST", headers: { "Content-Type": "application/json" }, body: JSON.stringify({ message: text, history }) });
    const data = await res.json();
    if (data.error) append("assistant", "Error: " + data.error); else { append("assistant", data.reply); history.push({ role: "assistant", content: data.reply }); }
  } catch (err) { append("assistant", "Network error: " + err.message); }
});
