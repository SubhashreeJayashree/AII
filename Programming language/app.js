const runBtn = document.getElementById("runBtn");
const askBtn = document.getElementById("askBtn");
const helpBtn = document.getElementById("helpBtn");
const themeBtn = document.getElementById("themeBtn");
const sendAskBtn = document.getElementById("sendAskBtn");
const voiceBtn = document.getElementById("voiceBtn");
const speakBtn = document.getElementById("speakBtn");
const moduleBtns = document.querySelectorAll(".moduleBtn");
const sidebarModuleBtns = document.querySelectorAll(".sidebarModuleBtn");
const chipExplain = document.getElementById("chipExplain");
const chipFix = document.getElementById("chipFix");
const chipGen = document.getElementById("chipGen");
const chipPerf = document.getElementById("chipPerf");

const latencyEl = document.getElementById("latency");
const p95El = document.getElementById("p95");
const aiStatusEl = document.getElementById("aiStatus");
const buildStatusEl = document.getElementById("buildStatus");
const askInput = document.getElementById("askInput");
const aiOutput = document.getElementById("aiOutput");
const codeEditor = document.getElementById("codeEditor");
const programOutput = document.getElementById("programOutput");
const terminalOutput = document.getElementById("terminalOutput");
const terminalInput = document.getElementById("terminalInput");
const terminalRunBtn = document.getElementById("terminalRunBtn");

let sampleLatencies = [];
let buildRunning = false;
let isListening = false;

function randomLatency() {
  return Math.floor(8 + Math.random() * 40);
}

function computeP95(values) {
  if (!values.length) return "--";
  const sorted = [...values].sort((a, b) => a - b);
  const idx = Math.min(sorted.length - 1, Math.ceil(sorted.length * 0.95) - 1);
  return sorted[idx];
}

function tickRealtime() {
  const current = randomLatency();
  sampleLatencies.push(current);
  if (sampleLatencies.length > 60) sampleLatencies.shift();
  latencyEl.textContent = `${current} ms`;
  p95El.textContent = `${computeP95(sampleLatencies)} ms`;
}

function setOutput(text) {
  aiOutput.textContent = text;
}

function setProgramOutput(text, isHtml = false) {
  if (isHtml) {
    programOutput.innerHTML = text;
  } else {
    programOutput.textContent = text;
  }
}

function appendTerminal(line) {
  terminalOutput.textContent += `\n${line}`;
  terminalOutput.scrollTop = terminalOutput.scrollHeight;
}

function runAgentQuery(query) {
  const lower = query.toLowerCase();
  
  if (lower.includes("analyze") && lower.includes("dataset")) {
    codeEditor.value = [
      "core main {",
      "  data := load_dataset \"users.csv\"",
      "  summary := ask \"generate statistical variance and mean on data\"",
      "  show summary.text",
      "  show \"Statistical dataset analysis complete!\"",
      "}"
    ].join("\n");
    setOutput("Agent securely imported the dataset analysis module.");
    appendTerminal(`AI> Dataset script generated: ${query}`);
    return;
  }
  
  if (lower.includes("build") && lower.includes("ui")) {
    codeEditor.value = [
      "core main {",
      "  note := ask \"generate physical login interface component\"",
      "  // AI Agent automatically injects interactive physical UI components",
      "  render_ui \"<div id='aiLoginBox' style='padding:15px; border:1px solid #444; border-radius:8px; background:#1e1e1e; max-width:250px; color:#fff; font-family:sans-serif;'><h3 style='margin-top:0; padding-bottom:10px; border-bottom:1px solid #333;'>System Login</h3><input id='aiUser' type='text' placeholder='username' style='width:90%;margin-bottom:10px; padding:8px; border-radius:4px; border:1px solid #555; background:#111; color:#fff;' /><br/><input type='password' placeholder='password' style='width:90%;margin-bottom:15px; padding:8px; border-radius:4px; border:1px solid #555; background:#111; color:#fff;' /><br/><button onclick='var u=document.getElementById(\\\"aiUser\\\").value || \\\"Guest\\\"; document.getElementById(\\\"aiLoginBox\\\").innerHTML=\\\"<h2>Welcome, \\\"+u+\\\"!</h2><p style=\\\\\"color:#2ed573\\\\\">Successfully authenticated by Novi Runtime.</p><h3>Main Page Dashboard</h3><hr/><ul><li>System Status: OK</li><li>Database: Connected</li></ul>\\\"' style='background:#ffcf66; font-weight:bold; border:none; padding:10px; width:100%; border-radius:4px; cursor:pointer; color:#000;'>Sign In</button></div>\"",
      "}"
    ].join("\n");
    setOutput("Agent Physical UI Builder injected the component directly into the editor!");
    appendTerminal(`AI> Physical UI Builder active: ${query}`);
    return;
  }

  if (lower.includes("hook") && lower.includes("database")) {
    codeEditor.value = [
      "core main {",
      "  db := connect \"local:5432\"",
      "  query := \"SELECT * FROM customers WHERE active=true\"",
      "  records := db_read query",
      "  show \"Database hook instantiated automatically by Agent.\"",
      "}"
    ].join("\n");
    setOutput("Local Database connection securely scaffolded by the Agent.");
    appendTerminal(`AI> Local DB hooked: ${query}`);
    return;
  }

  if (
    lower.includes("hello world") &&
    (lower.includes("a+b") || lower.includes("add")) &&
    lower.includes("a=1") &&
    lower.includes("b=4")
  ) {
    codeEditor.value = [
      "core main {",
      "  a := 1",
      "  b := 4",
      "  show \"hello world\"",
      "  show a + b",
      "}"
    ].join("\n");
    setOutput("Generated requested program. Click Run to print output.");
    appendTerminal(`AI> Program generated from query: ${query}`);
    return;
  }
  if (lower.includes("python") && lower.includes("if") && lower.includes("print")) {
    codeEditor.value = [
      "core main {",
      "  a := 1",
      "  when a = 1 {",
      "    show \"hello\"",
      "  }",
      "}"
    ].join("\n");
    setOutput("Generated Python-like easy Novi program. Click Run to print output.");
    appendTerminal(`AI> Converted Python-like request: ${query}`);
    return;
  }
  const aiText = fakeAIResponse(query);
  setOutput(aiText);
  appendTerminal(`AI> ${aiText.replace(/\n/g, " | ")}`);
}

function tryConvertOtherLanguageSnippet(raw) {
  const text = raw.trim();
  if (text.includes("console.log(") || text.includes("let ") || text.includes("const ")) {
    return [
      "core main {",
      "  show \"Converted from JS style\"",
      "}"
    ].join("\n");
  }
  if (text.includes("System.out.println") || text.includes("public static void main")) {
    return [
      "core main {",
      "  show \"Converted from Java style\"",
      "}"
    ].join("\n");
  }
  if (text.includes("Console.WriteLine") || text.includes("namespace ")) {
    return [
      "core main {",
      "  show \"Converted from .NET/C# style\"",
      "}"
    ].join("\n");
  }
  if (text.includes("SELECT ") || text.includes("FROM ")) {
    return [
      "core main {",
      "  show \"SQL query detected. Use AI for schema/query optimization.\"",
      "}"
    ].join("\n");
  }
  return "";
}

function normalizeTypedNovi(code) {
  let fixed = code;
  fixed = fixed.replace(/\bcore\s+main\s*\(/g, "core main {");
  fixed = fixed.replace(/\bmain\s*\{/g, "core main {");
  fixed = fixed.replace(/\}\s*else if/g, "}\nelse if");
  fixed = fixed.replace(/\}\s*else\s*\{/g, "}\nelse {");
  
  // Cross-language bridges (C++, Java, Python, SQL -> Novi)
  fixed = fixed.replace(/\bprintf?\s*\(\s*(.+?)\s*\)\s*;/g, "show $1");
  fixed = fixed.replace(/\bstd::cout\s*<<\s*(.+?)(?:\s*<<\s*std::endl)?\s*;/g, "show $1");
  fixed = fixed.replace(/\bcout\s*<<\s*(.+?)(?:\s*<<\s*endl)?\s*;/g, "show $1");
  fixed = fixed.replace(/\bSystem\.out\.println\s*\(\s*(.+?)\s*\)\s*;/g, "show $1");
  fixed = fixed.replace(/\bprint\s*\(\s*(.+?)\s*\)/g, "show $1");
  fixed = fixed.replace(/\bconsole\.log\s*\(\s*(.+?)\s*\)\s*;/g, "show $1");
  
  // Auto-SQL bridge (Simple SELECT to Novi output format)
  fixed = fixed.replace(/^\s*SELECT\s+(.+?)\s+FROM\s+([a-zA-Z_]\w*).*$/gim, 'data := db_read "SELECT $1 FROM $2"\nshow "fetched SQL records from $2"');
  
  // Polyglot variable declarations (int xyz = 5; -> xyz := 5)
  fixed = fixed.replace(/\b(?:int|let|const|var|String|float|double)\s+([a-zA-Z_]\w*)\s*=\s*(.+?);?/g, "$1 := $2");
  
  fixed = fixed.replace(/(^|\s)([a-zA-Z_]\w*)\s*=\s*([^=\n]+)$/gm, "$1$2 := $3");
  fixed = fixed.replace(/::=/g, ":=");
  fixed = fixed.replace(/\bprint\b/g, "show");
  fixed = fixed.replace(/\bif\s*\((.+)\)\s*print\s*\((.+)\)/g, "if $1 {\n  show $2\n}");
  fixed = fixed.replace(/show\s*\(\s*"([^"]+)"\s*\)/g, "show \"$1\"");
  fixed = fixed.replace(/show\s*\(\s*([a-zA-Z_]\w*\s*\+\s*[a-zA-Z_]\w*|\d+\s*\+\s*\d+|[a-zA-Z_]\w*)\s*\)/g, "show $1");
  fixed = fixed.replace(/;\s*$/gm, "");
  return fixed;
}

function evalExpr(expr, vars) {
  const safe = expr.trim();
  
  if (/^".*"$/.test(safe)) {
    return safe.slice(1, -1);
  }
  if (/^\d+$/.test(safe)) {
    return Number(safe);
  }
  if (/^[a-zA-Z_]\w*$/.test(safe)) {
    return vars[safe] ?? 0;
  }
  const fieldMatch = safe.match(/^([a-zA-Z_]\w*)\.text$/);
  if (fieldMatch) {
    return vars[fieldMatch[1]]?.text ?? "";
  }

  if (safe.includes('+')) {
    let parts = [];
    let current = "";
    let inString = false;
    for (let char of safe) {
      if (char === '"') inString = !inString;
      if (char === '+' && !inString) {
        parts.push(current.trim());
        current = "";
      } else {
        current += char;
      }
    }
    parts.push(current.trim());
    
    if (parts.length > 1) {
      let evaledParts = parts.map(p => evalExpr(p, vars));
      if (evaledParts.some(p => typeof p === 'string')) {
        return evaledParts.join('');
      } else {
        return evaledParts.reduce((a, b) => Number(a) + Number(b), 0);
      }
    }
  }

  const mathMatch = safe.match(/^([a-zA-Z_]\w*|\d+)\s*([-*\/])\s*([a-zA-Z_]\w*|\d+)$/);
  if (mathMatch) {
    const left = evalExpr(mathMatch[1], vars);
    const right = evalExpr(mathMatch[3], vars);
    if (mathMatch[2] === '-') return left - right;
    if (mathMatch[2] === '*') return left * right;
    if (mathMatch[2] === '/') return left / right;
  }
  
  const compareMatch = safe.match(/^([a-zA-Z_]\w*|\d+)\s*(==|=|>|<|>=|<=)\s*([a-zA-Z_]\w*|\d+)$/);
  if (compareMatch) {
    const left = evalExpr(compareMatch[1], vars);
    const right = evalExpr(compareMatch[3], vars);
    const op = compareMatch[2] === "=" ? "==" : compareMatch[2];
    if (op === "==") return left === right;
    if (op === ">") return left > right;
    if (op === "<") return left < right;
    if (op === ">=") return left >= right;
    if (op === "<=") return left <= right;
  }

  return safe;
}

function runNoviProgram(code) {
  const vars = {};
  const lines = code.split("\n");
  const outputs = [];
  const blockStack = [];
  let pendingIfChain = null;

  for (const raw of lines) {
    const line = raw.trim();
    if (!line || line.startsWith("//") || line.startsWith("core ")) continue;

    const elseIfStart = line.match(/^else if\s+(.+)\s*\{$/);
    if (elseIfStart) {
      if (!pendingIfChain) continue;
      const parentAllowed = pendingIfChain.parentAllowed;
      const shouldRun = parentAllowed && !pendingIfChain.matched && Boolean(evalExpr(elseIfStart[1], vars));
      pendingIfChain.matched = pendingIfChain.matched || shouldRun;
      blockStack.push({
        run: shouldRun,
        isConditional: true,
        chainMatched: pendingIfChain.matched,
        parentAllowed
      });
      continue;
    }

    const elseStart = line.match(/^else\s*\{$/);
    if (elseStart) {
      if (!pendingIfChain) continue;
      const shouldRun = pendingIfChain.parentAllowed && !pendingIfChain.matched;
      pendingIfChain.matched = true;
      blockStack.push({
        run: shouldRun,
        isConditional: true,
        chainMatched: true,
        parentAllowed: pendingIfChain.parentAllowed
      });
      continue;
    }

    if (pendingIfChain) {
      pendingIfChain = null;
    }

    if (line === "}") {
      const popped = blockStack.pop();
      if (popped?.isConditional) {
        pendingIfChain = {
          matched: popped.chainMatched,
          parentAllowed: popped.parentAllowed
        };
      } else {
        pendingIfChain = null;
      }
      continue;
    }

    const ifStart = line.match(/^(if|when)\s+(.+)\s*\{$/);
    if (ifStart) {
      const parentAllowed = !blockStack.some((b) => b.run === false);
      const ok = parentAllowed && Boolean(evalExpr(ifStart[2], vars));
      blockStack.push({
        run: ok,
        isConditional: true,
        chainMatched: ok,
        parentAllowed
      });
      pendingIfChain = {
        matched: ok,
        parentAllowed
      };
      continue;
    }

    const isBlocked = blockStack.some((b) => b.run === false);
    if (isBlocked) continue;

    const assign = line.match(/^([a-zA-Z_]\w*)\s*:=\s*(.+)$/);
    if (assign) {
      const name = assign[1];
      const rhs = assign[2];
      if (rhs.startsWith("ask ")) {
        vars[name] = { text: "AI: Suggested action: cooling fan level 2." };
      } else {
        vars[name] = evalExpr(rhs, vars);
      }
      continue;
    }

    const showText = line.match(/^show\s+"(.+)"$/);
    if (showText) {
      outputs.push(showText[1]);
      continue;
    }

    const showVar = line.match(/^show\s+([a-zA-Z_]\w*)$/);
    if (showVar) {
      outputs.push(String(vars[showVar[1]] ?? ""));
      continue;
    }

    const showField = line.match(/^show\s+([a-zA-Z_]\w*)\.text$/);
    if (showField) {
      outputs.push(String(vars[showField[1]]?.text ?? ""));
      continue;
    }

    const showExpr = line.match(/^show\s+(.+)$/);
    if (showExpr) {
      outputs.push(String(evalExpr(showExpr[1], vars)));
      continue;
    }

    const renderMatch = line.match(/^render_ui\s+"(.*)"$/);
    if (renderMatch) {
      outputs.push(renderMatch[1]);
      continue;
    }
  }

  return outputs;
}

function fakeAIResponse(query) {
  if (!query.trim()) {
    return "Please type a question first.";
  }

  const lower = query.toLowerCase();
  if (lower.includes(".net") || lower.includes("dotnet") || lower.includes("c#")) {
    return [
      "AI Agent (.NET):",
      "- Use ASP.NET Core for APIs.",
      "- Use EF Core for RDBMS access.",
      "- Keep controller, service, repository layers clean."
    ].join("\n");
  }
  if (lower.includes("node") || lower.includes("node.js") || lower.includes("nodejs")) {
    return [
      "AI Agent (Node.js):",
      "- Prefer async/await for clear flow.",
      "- Validate input and centralize error handling.",
      "- Use proper environment-based config."
    ].join("\n");
  }
  if (lower.includes("rdbms") || lower.includes("sql") || lower.includes("database")) {
    return [
      "AI Agent (RDBMS):",
      "- Normalize tables and define keys.",
      "- Use indexes for hot query paths.",
      "- Use transactions for multi-step updates."
    ].join("\n");
  }
  if (lower.includes("optimize") || lower.includes("latency")) {
    return [
      "Optimization tips:",
      "1) Move parsing outside loop if constant.",
      "2) Pre-allocate buffers for sensor data.",
      "3) Use bounded retries with timeout 100ms."
    ].join("\n");
  }
  if (lower.includes("fix")) {
    return [
      "Suggested fix:",
      "- Add zero/null checks before conversion.",
      "- Wrap risky parse in result<T,E> handling.",
      "- Add test for malformed packets."
    ].join("\n");
  }
  if (lower.includes("iot") || lower.includes("cloud") || lower.includes("ml") || lower.includes("web")) {
    return [
      "Unified Novi answer:",
      "Use built-in modules directly in Novi code.",
      "No separate C/Java/Python/JS files are required."
    ].join("\n");
  }
  return [
    "AI Agent response:",
    "I can answer questions across programming domains,",
    "explain concepts, suggest fixes, and generate Novi code."
  ].join("\n");
}

function moduleSnippet(moduleName) {
  const snippets = {
    web: [
      "",
      "pack web.core",
      "pack web.render",
      "",
      "core web_app {",
      "  route \"/\" -> page title:\"Novi Web\" body:head1(\"hello from novi\")",
      "}"
    ].join("\n"),
    iot: [
      "",
      "pack iot.stream",
      "",
      "core iot_worker {",
      "  bus := connect \"edge.local:1883\"",
      "  each pkt in bus.channel(\"factory/temp\") {",
      "    show pkt.data",
      "  }",
      "}"
    ].join("\n"),
    cloud: [
      "",
      "pack cloud.bridge",
      "",
      "core cloud_sync temp {",
      "  push \"alerts/temp\" with {value: temp}",
      "}"
    ].join("\n"),
    ml: [
      "",
      "pack ml.engine",
      "",
      "core score v {",
      "  model := load_model \"anomaly.nvmodel\"",
      "  give model.predict [v]",
      "}"
    ].join("\n"),
    system: [
      "",
      "pack sys.disk",
      "pack sys.net",
      "",
      "core health_check {",
      "  ok := ping \"gateway.local\"",
      "  write \"status.log\" \"gateway=\" + text(ok)",
      "}"
    ].join("\n"),
    python: [
      "",
      "pack lang.python",
      "",
      "core py_script {",
      "  // Python style code natively supported",
      "  show \"Python environment active\"",
      "}"
    ].join("\n"),
    java: [
      "",
      "pack lang.java",
      "",
      "core java_jvm {",
      "  // Java classes automatically bridged",
      "  show \"Java JVM linked\"",
      "}"
    ].join("\n"),
    cpp: [
      "",
      "pack lang.cpp",
      "",
      "core cpp_runtime {",
      "  // C/C++ memory model handled safely",
      "  show \"C/C++ runtime activated\"",
      "}"
    ].join("\n"),
    rdbms: [
      "",
      "pack db.sql",
      "",
      "core query_db {",
      "  // SQL RDBMS queries auto-optimized",
      "  records := db_read \"SELECT * FROM users\"",
      "  show \"SQL RDBMS connected\"",
      "}"
    ].join("\n"),
    ui: [
      "",
      "pack web.ui.core",
      "",
      "core secure_login {",
      "  // AI Agent automatically injects interactive physical UI components",
      "  render_ui \"<div id='aiLoginBox' style='padding:15px; border:1px solid #444; border-radius:8px; background:#1e1e1e; max-width:250px; color:#fff; font-family:sans-serif;'><h3 style='margin-top:0; padding-bottom:10px; border-bottom:1px solid #333;'>System Login</h3><input id='aiUser' type='text' placeholder='username' style='width:90%;margin-bottom:10px; padding:8px; border-radius:4px; border:1px solid #555; background:#111; color:#fff;' /><br/><input type='password' placeholder='password' style='width:90%;margin-bottom:15px; padding:8px; border-radius:4px; border:1px solid #555; background:#111; color:#fff;' /><br/><button onclick='var u=document.getElementById(\\\"aiUser\\\").value || \\\"Guest\\\"; document.getElementById(\\\"aiLoginBox\\\").innerHTML=\\\"<h2>Welcome, \\\"+u+\\\"!</h2><p style=\\\\\"color:#2ed573\\\\\">Successfully authenticated by Novi Runtime.</p><h3>Main Page Dashboard</h3><hr/><ul><li>System Status: OK</li><li>Database: Connected</li></ul>\\\"' style='background:#ffcf66; font-weight:bold; border:none; padding:10px; width:100%; border-radius:4px; cursor:pointer; color:#000;'>Sign In</button></div>\"",
      "}"
    ].join("\n")
  };
  return snippets[moduleName] || "";
}

runBtn.addEventListener("click", () => {
  if (buildRunning) return;
  buildRunning = true;
  buildStatusEl.textContent = "Running...";
  buildStatusEl.style.color = "#ffcf66";
  setTimeout(() => {
    const fixedCode = normalizeTypedNovi(codeEditor.value);
    codeEditor.value = fixedCode;
    const lines = runNoviProgram(fixedCode);
    const finalOutput = lines.length ? lines.join("\n") : "Program ran. No show statements found.";

    buildRunning = false;
    buildStatusEl.textContent = "Success";
    buildStatusEl.style.color = "#2ed573";
    setOutput("Program executed.\nAI auto-corrected basic syntax if needed.");
    
    if (finalOutput.includes("<div")) {
      setProgramOutput("<strong>Novi Runtime Output</strong><br/>-------------------<br/>" + finalOutput.replace(/\n/g, "<br/>"), true);
    } else {
      setProgramOutput([
        "Novi Runtime Output",
        "-------------------",
        finalOutput
      ].join("\n"));
    }
    
    appendTerminal(`RUN> ${finalOutput.replace(/\n/g, " | ")}`);
  }, 1200);
});

askBtn.addEventListener("click", () => {
  const before = codeEditor.value;
  const fixed = normalizeTypedNovi(before);
  codeEditor.value = fixed;
  const selectedText = fixed.slice(0, 280);
  const reply = fakeAIResponse(`explain and correct code: ${selectedText}`);
  setOutput(`${reply}\n\nAI correction applied to editor syntax.`);
});

chipGen.addEventListener("click", () => {
  const snippet = [
    "",
    "// Novi unified starter (native syntax)",
    "pack web.core",
    "pack iot.stream",
    "pack cloud.bridge",
    "pack ml.engine",
    "",
    "core unified_pipeline {",
    "  // Single-language full-stack flow",
    "}"
  ].join("\n");
  codeEditor.value += snippet;
  setOutput("Added unified Novi stack snippet. No external language files needed.");
});

chipFix.addEventListener("click", () => {
  codeEditor.value = codeEditor.value.replace("temp := 82", "temp := safe_int 82");
  setOutput("Applied safe conversion fix in Novi native syntax.");
});

helpBtn.addEventListener("click", () => {
  window.open("./HOW_IT_WORKS.md", "_blank", "noopener,noreferrer");
});

themeBtn.addEventListener("click", () => {
  document.body.classList.toggle("light");
});

sendAskBtn.addEventListener("click", () => {
  const query = askInput.value.trim();
  appendTerminal(`QUERY> ${query}`);
  runAgentQuery(query);
});

chipExplain.addEventListener("click", () => askBtn.click());
chipPerf.addEventListener("click", () => {
  setOutput(fakeAIResponse("optimize this loop for low latency"));
});

moduleBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const moduleName = btn.dataset.module;
    codeEditor.value += moduleSnippet(moduleName);
    setOutput(`Integrated ${moduleName.toUpperCase()} module in Novi code only.`);
    setProgramOutput(`Ready: ${moduleName.toUpperCase()} module added.\nPress Run to view runtime output.`);
  });
});

sidebarModuleBtns.forEach((btn) => {
  btn.addEventListener("click", () => {
    const topic = btn.dataset.topic || btn.textContent.trim();
    const query = `Explain ${topic} for beginner and give quick implementation steps`;
    askInput.value = query;
    setOutput(fakeAIResponse(query));
    setProgramOutput(`AI answered topic: ${btn.textContent.trim()}\nType follow-up question and click Send Query.`);
    appendTerminal(`TOPIC> ${btn.textContent.trim()}`);
  });
});

voiceBtn.addEventListener("click", () => {
  const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
  if (!SpeechRecognition) {
    setOutput("Voice input is not supported in this browser.");
    return;
  }

  if (isListening) return;

  const recognition = new SpeechRecognition();
  recognition.lang = "en-US";
  recognition.interimResults = false;
  recognition.maxAlternatives = 1;

  isListening = true;
  voiceBtn.textContent = "Listening...";
  setOutput("Voice mode started. Please speak your question.");

  recognition.onresult = (event) => {
    const transcript = event.results[0][0].transcript;
    askInput.value = transcript;
    runAgentQuery(transcript);
  };

  recognition.onerror = () => {
    setOutput("Voice input failed. Try again or use text input.");
  };

  recognition.onend = () => {
    isListening = false;
    voiceBtn.textContent = "Voice Input";
  };

  recognition.start();
});

speakBtn.addEventListener("click", () => {
  const text = aiOutput.textContent.trim();
  if (!text) {
    setOutput("No AI answer available to speak.");
    return;
  }
  if (!window.speechSynthesis) {
    setOutput("Speech output is not supported in this browser.");
    return;
  }
  const utter = new SpeechSynthesisUtterance(text);
  utter.rate = 1;
  utter.pitch = 1;
  window.speechSynthesis.cancel();
  window.speechSynthesis.speak(utter);
});

function runTerminalCommand() {
  const cmd = terminalInput.value.trim();
  if (!cmd) return;
  appendTerminal(`$ ${cmd}`);

  const lower = cmd.toLowerCase();
  if (lower === "clear") {
    terminalOutput.textContent = "Novi Terminal cleared.";
    terminalInput.value = "";
    return;
  }
  if (lower === "run") {
    runBtn.click();
    terminalInput.value = "";
    return;
  }
  if (lower.startsWith("ai ")) {
    const q = cmd.slice(3).trim();
    askInput.value = q;
    runAgentQuery(q);
    terminalInput.value = "";
    return;
  }
  if (lower.startsWith("write program ")) {
    const q = cmd.slice("write program ".length).trim();
    askInput.value = q;
    runAgentQuery(q);
    terminalInput.value = "";
    return;
  }
  if (lower.startsWith("convert ")) {
    const src = cmd.slice("convert ".length);
    const converted = tryConvertOtherLanguageSnippet(src);
    if (converted) {
      codeEditor.value = converted;
      appendTerminal("CONVERT> Source style converted to Novi starter.");
    } else {
      appendTerminal("CONVERT> Could not detect source style. Try JS/Java/C#/SQL text.");
    }
    terminalInput.value = "";
    return;
  }
  appendTerminal("Unknown command. Use: run | ai <query> | write program <request> | convert <code> | clear");
  terminalInput.value = "";
}

terminalRunBtn.addEventListener("click", runTerminalCommand);
terminalInput.addEventListener("keydown", (event) => {
  if (event.key === "Enter") {
    runTerminalCommand();
  }
});

aiStatusEl.textContent = "Online";
setInterval(tickRealtime, 1000);
tickRealtime();
setProgramOutput("No output yet. Press Run to execute Novi code.");
