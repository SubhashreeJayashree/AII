const runBtn = document.getElementById("runBtn");
const clearBtn = document.getElementById("clearBtn");
const saveBtn = document.getElementById("saveBtn");
const saveOutputBtn = document.getElementById("saveOutputBtn");
const saveGuideBtn = document.getElementById("saveGuideBtn");
const saveAllBtn = document.getElementById("saveAllBtn");
const output = document.getElementById("output");
const shellInput = document.getElementById("shellInput");
const shellRun = document.getElementById("shellRun");

runBtn.addEventListener("click", () => {
  const code = document.getElementById("code").value;
  output.textContent += "\\nOK: " + code;
});

clearBtn.addEventListener("click", () => { output.textContent = ""; });

shellRun.addEventListener("click", () => {
  const line = shellInput.value.trim();
  if (!line) return;
  output.textContent += "\\nOK: " + line;
  shellInput.value = "";
});

saveBtn.addEventListener("click", () => {
  const code = document.getElementById("code").value;
  const blob = new Blob([code], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "my_code.aino"; a.click();
  URL.revokeObjectURL(url);
});

saveOutputBtn.addEventListener("click", () => {
  const logs = output.textContent;
  const blob = new Blob([logs], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "shell_output.txt"; a.click();
  URL.revokeObjectURL(url);
});

saveGuideBtn.addEventListener("click", () => {
  const guide = document.getElementById("guide").innerText;
  const blob = new Blob([guide], { type: "application/pdf" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "AinoNova_LearningGuide.pdf"; a.click();
  URL.revokeObjectURL(url);
});

saveAllBtn.addEventListener("click", () => {
  const code = document.getElementById("code").value;
  const logs = output.textContent;
  const guide = document.getElementById("guide").innerText;
  const all = "=== Code ===\\n" + code + "\\n\\n=== Output ===\\n" + logs + "\\n\\n=== Guide ===\\n" + guide;
  const blob = new Blob([all], { type: "text/plain" });
  const url = URL.createObjectURL(blob);
  const a = document.createElement("a");
  a.href = url; a.download = "aino_nova_bundle.txt"; a.click();
  URL.revokeObjectURL(url);
});
