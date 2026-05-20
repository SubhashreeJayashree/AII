async function sendTask() {
    let task = document.getElementById("taskInput").value;
    if (task.trim() === "") return;

    // If welcome is visible, collapse it into compact session list before sending
    try { collapseWelcomeToList(); } catch (e) { console.warn('collapseWelcomeToList failed', e); }

    addMessage(task, "user");
    document.getElementById("taskInput").value = "";

    // include selected mode (if any) and options (language, emotion, storyCount)
    const modeEl = document.getElementById('modeSelect');
    const mode = modeEl ? modeEl.value : 'default';
    const language = (document.getElementById('languageSelect') || {}).value || 'any';
    const emotion = (document.getElementById('emotionSelect') || {}).value || 'default';
    const storyCountVal = document.getElementById('storyCount');
    const storyCount = storyCountVal ? Math.max(1, Math.min(5, parseInt(storyCountVal.value || '1'))) : 1;
    const storyLength = (document.getElementById('storyLength') || {}).value || 'medium';
    const useAI = !!(document.getElementById('useAI') && document.getElementById('useAI').checked);
    const quick = !!(document.getElementById('quickToggle') && document.getElementById('quickToggle').checked);
    const subject = (document.getElementById('subjectSelect') || {}).value || '';

    // (debug logging removed) do not show internal debug strings in chat output

    let response = await fetch("http://127.0.0.1:5000/process", {
        method: "POST",
        headers: {"Content-Type": "application/json"},
        body: JSON.stringify({"task": task, "mode": mode, "options": {language: language, emotion: emotion, story_count: storyCount, story_length: storyLength, use_llm: useAI, quick: quick, subject: subject}})
    });

    let data = await response.json();
if (data.translation.speech) {
    addMessage(data.translation.speech, "bot");
}
    if (data.status === "unsafe") {
        addMessage("❌ " + data.message, "bot");
        speak("This task is unsafe. I cannot perform it.");
        showRobot("error");
        return;
    }

    // FIXED: backend returns data.translation NOT data.commands
    let steps = data.translation.steps;
addMessage("✅ Task is safe.\n\nRobot Commands:\n" + JSON.stringify(steps, null, 2), "bot");
document.getElementById("output").innerText = data.translation.speech;

    addMessage("✅ Task is safe.\n\nRobot Commands:\n" + JSON.stringify(steps, null, 2), "bot");

    // If translator returned an 'output' (code, story, explanation, math result), show it
    if (data.translation.output) {
        // Stories list
        if (Array.isArray(data.translation.output.stories)) {
            data.translation.output.stories.forEach((s, i) => {
                addMessage(`Story ${i + 1} (${s.lang}):\n${s.text}\n`, 'bot');
            });
        }

        // Songs list: show title and links with open buttons
        if (Array.isArray(data.translation.output.songs)) {
            data.translation.output.songs.forEach((song, idx) => {
                // Build a custom message element so we can attach buttons
                let chatBox = document.getElementById('chatBox');
                let div = document.createElement('div');
                div.className = 'chat-message bot-msg';

                let title = document.createElement('div');
                title.style.fontWeight = '600';
                title.innerText = `Suggestion ${idx + 1}: ${song.title}`;

                let links = document.createElement('div');
                links.style.marginTop = '6px';

                let ytBtn = document.createElement('button');
                ytBtn.innerText = 'Open YouTube';
                ytBtn.style.marginRight = '8px';
                ytBtn.onclick = () => { window.open(song.youtube, '_blank', 'noopener'); };

                let spBtn = document.createElement('button');
                spBtn.innerText = 'Open Spotify';
                spBtn.onclick = () => { window.open(song.spotify, '_blank', 'noopener'); };

                links.appendChild(ytBtn);
                links.appendChild(spBtn);

                div.appendChild(title);
                div.appendChild(links);

                chatBox.appendChild(div);
                chatBox.scrollTop = chatBox.scrollHeight;
            });
        }
        console.log('Sending subject:', subject);
console.log('Received translation:', data.translation);

        // Generic output keys (code, explanation, result)
        if (data.translation.output.code) {
            addMessage('Code:\n' + data.translation.output.code, 'bot');
        }
        if (data.translation.output.explanation) {
            addMessage('Explanation:\n' + data.translation.output.explanation, 'bot');
        }
        if (data.translation.output.result) {
            addMessage('Result:\n' + data.translation.output.result, 'bot');
        }
        // If there are other simple string outputs, display them
        if (typeof data.translation.output === 'string') {
            addMessage('Output:\n' + data.translation.output, 'bot');
        }
        // Motivational output (speaker)
        if (data.translation.output.motivation) {
                const speaker = data.translation.output.speaker || 'Motivational Speaker';
                addMessage(`${speaker}:\n${data.translation.output.motivation}`, 'bot');
                // style the last message as motivational
                try {
                    const chatBox = document.getElementById('chatBox');
                    if (chatBox && chatBox.lastChild) chatBox.lastChild.classList.add('motivational-msg');
                } catch (err) { /* ignore */ }
        }
    }

    // Determine an appropriate TTS language: prefer backend-provided speech_lang, fall back to selected language
    const backendSpeechLang = (data.translation.output && data.translation.output.speech_lang) ? data.translation.output.speech_lang : null;
    const ttsLang = backendSpeechLang || (language === 'ta' ? 'ta-IN' : (language === 'es' ? 'es-ES' : (language === 'fr' ? 'fr-FR' : 'en-US')));
    speak(data.translation.speech || "Task is safe. Executing robot steps.", ttsLang);

    simulateRobot(steps);
}

function addMessage(msg, type) {
    let chatBox = document.getElementById("chatBox");
    let div = document.createElement("div");
    div.className = "chat-message " + (type === "user" ? "user-msg" : "bot-msg");

    // Assign a random rainbow class for bot messages so output is colorful
    if (type !== 'user') {
        const rainbowIndex = Math.floor(Math.random() * 6) + 1; // 1..6
        div.classList.add(`rainbow-${rainbowIndex}`);
    }

    // Escape HTML to avoid injection
    function escapeHtml(unsafe) {
        return unsafe
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/\"/g, "&quot;")
            .replace(/'/g, "&#039;");
    }

    // Turn URLs into clickable links
    function linkify(text) {
        const urlRegex = /(https?:\/\/[\w\-._~:/?#[\]@!$&'()*+,;=%]+)/g;
        return text.replace(urlRegex, function(url) {
            return `<a href="${url}" target="_blank" rel="noopener noreferrer">${url}</a>`;
        });
    }

    if (type === 'user') {
        div.innerText = msg;
    } else {
        // For bot messages, show clickable links but escape other content
        const escaped = escapeHtml(String(msg));
        div.innerHTML = linkify(escaped);
    }

    chatBox.appendChild(div);
    chatBox.scrollTop = chatBox.scrollHeight;
    // Flash overlay disabled for now so background remains persistent
    // if (type !== 'user') flashScreen();
}

// Create a full-screen colored overlay for a brief time
function flashScreen() {
    // Disabled: keep background persistent and avoid transient full-screen flashes
    return;
}

// Text-to-speech
function speak(text, lang) {
    try {
        if (!('speechSynthesis' in window) || typeof SpeechSynthesisUtterance === 'undefined') {
            console.warn('TTS not supported in this browser.');
            addMessage('⚠️ Text-to-speech not supported in this browser.', 'bot');
            return;
        }

        if (!text || text.trim() === '') {
            console.warn('No text provided to speak.');
            return;
        }

        let utter = new SpeechSynthesisUtterance(text);
        if (lang) {
            try { utter.lang = lang; } catch(e) { /* ignore */ }
        }
        utter.rate = 1;
        utter.pitch = 1;
        window.speechSynthesis.speak(utter);
    } catch (err) {
        console.error('TTS error:', err);
        addMessage('⚠️ Text-to-speech error: ' + err.message, 'bot');
    }
}

// Render a full-width welcome panel inside the chat box
function renderWelcomeBox() {
    const chatBox = document.querySelector('.chat-box');
    if (!chatBox) return;

    const container = document.createElement('div');
    container.className = 'bot-msg welcome-full';

    const title = document.createElement('div');
    title.className = 'welcome-title';
    title.innerText = 'Hi — how can I help you?';

    const sub = document.createElement('div');
    sub.className = 'welcome-sub';
    sub.innerText = 'Choose a mode or tell me what you need';

    const options = document.createElement('div');
    options.className = 'welcome-options';

    const modes = ['Storyteller','Teacher','Emotional','Motivational','Quick Chat'];
    modes.forEach(m => {
        const btn = document.createElement('button');
        btn.className = 'opt-btn';
        btn.innerText = m;
        btn.onclick = () => {
            const modeSelect = document.getElementById('modeSelect');
            if (modeSelect) modeSelect.value = m.toLowerCase();
            // focus prompt area
            const prompt = document.getElementById('taskInput');
            if (prompt) prompt.focus();
        };
        options.appendChild(btn);
    });

    const langRow = document.createElement('div');
    langRow.className = 'welcome-langrow';
    const langSelect = document.getElementById('languageSelect');
    if (langSelect) {
        const cp = langSelect.cloneNode(true);
        cp.id = 'welcomeLang';
        langRow.appendChild(cp);
    }

    const startRow = document.createElement('div');
    startRow.className = 'welcome-startrow';
    const startBtn = document.createElement('button');
    startBtn.className = 'start-btn';
    startBtn.innerText = 'Start';
    startBtn.onclick = () => {
        // collapse into compact session summary instead of removing entirely
        collapseWelcomeToList();
        const prompt = document.getElementById('taskInput');
        if (prompt) prompt.focus();
    };
    startRow.appendChild(startBtn);

    container.appendChild(title);
    container.appendChild(sub);
    container.appendChild(options);
    container.appendChild(langRow);
    container.appendChild(startRow);

    // insert at top of chat box
    chatBox.insertBefore(container, chatBox.firstChild);
}

// Replace the full welcome box with a compact session list (Mode / Language / Subject)
function collapseWelcomeToList() {
    const chatBox = document.querySelector('.chat-box');
    if (!chatBox) return;
    const welcome = chatBox.querySelector('.welcome-full');
    if (!welcome) return;

    // If already compacted, do nothing
    if (welcome.classList.contains('welcome-compact')) return;

    const mode = (document.getElementById('modeSelect') || {}).value || 'default';
    const language = (document.getElementById('languageSelect') || {}).value || 'any';
    const subject = (document.getElementById('subjectSelect') || {}).value || '';

    // Build compact content
    welcome.innerHTML = '';
    welcome.classList.add('welcome-compact');

    const label = document.createElement('div');
    label.className = 'session-label';
    label.innerText = 'Session:';

    const list = document.createElement('ul');
    list.className = 'session-list';

    const mli = document.createElement('li'); mli.innerText = `Mode: ${mode}`; list.appendChild(mli);
    const lli = document.createElement('li'); lli.innerText = `Language: ${language}`; list.appendChild(lli);
    if (subject) {
        const sli = document.createElement('li'); sli.innerText = `Subject: ${subject}`; list.appendChild(sli);
    }

    // Add a small dismiss button to re-open the full welcome if needed
    const reopen = document.createElement('button');
    reopen.className = 'opt-btn';
    reopen.style.padding = '6px 10px';
    reopen.style.fontSize = '13px';
    reopen.innerText = 'Edit';
    reopen.onclick = () => {
        // remove compact flag and re-render full welcome
        welcome.classList.remove('welcome-compact');
        welcome.parentNode.removeChild(welcome);
        renderWelcomeBox();
        // restore selected values
        const modeSelect = document.getElementById('modeSelect'); if (modeSelect) modeSelect.value = mode;
        const langSelect = document.getElementById('languageSelect'); if (langSelect) langSelect.value = language;
        const subj = document.getElementById('subjectSelect'); if (subj) subj.value = subject;
    };

    welcome.appendChild(label);
    welcome.appendChild(list);
    welcome.appendChild(reopen);
}

function speakText() {
    let input = document.getElementById("taskInput");
    let text = input ? input.value : '';

    if (!text || text.trim() === '') {
        // If there's no input text, try to speak the last bot message as helpful fallback
        let chatBox = document.getElementById('chatBox');
        if (chatBox && chatBox.lastChild) {
            let last = chatBox.lastChild.innerText || '';
            if (last) {
                speak(last);
                return;
            }
        }

        addMessage('⚠️ Nothing to speak. Type a task or click Send first.', 'bot');
        return;
    }

    speak(text);
}

// --- Speech-to-text (microphone) support ---
let recognition = null;
let isRecording = false;

function initSpeechRecognition() {
    if (recognition !== null) return;

    const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
    if (!SpeechRecognition) {
        // Disable button if not supported
        const btn = document.getElementById('recordButton');
        if (btn) {
            btn.disabled = true;
            btn.title = 'Speech recognition not supported in this browser.';
        }
        addMessage('⚠️ Speech-to-text not supported in this browser.', 'bot');
        return;
    }

    recognition = new SpeechRecognition();
    recognition.continuous = false;
    recognition.interimResults = true;
    recognition.lang = 'en-US';

    recognition.onstart = () => {
        isRecording = true;
        const btn = document.getElementById('recordButton');
        if (btn) btn.innerText = '⏺️ Recording...';
        addMessage('🎤 Listening...', 'bot');
    };

    recognition.onerror = (event) => {
        console.error('Speech recognition error', event);
        addMessage('⚠️ Speech recognition error: ' + (event.error || 'unknown'), 'bot');
    };

    let interimTranscript = '';
    recognition.onresult = (event) => {
        interimTranscript = '';
        let finalTranscript = '';
        for (let i = event.resultIndex; i < event.results.length; ++i) {
            const res = event.results[i];
            if (res.isFinal) finalTranscript += res[0].transcript;
            else interimTranscript += res[0].transcript;
        }

        // show interim as a hint in the input field
        const input = document.getElementById('taskInput');
        if (input) {
            if (finalTranscript) input.value = finalTranscript;
            else input.value = interimTranscript;
        }
    };

    recognition.onend = () => {
        isRecording = false;
        const btn = document.getElementById('recordButton');
        if (btn) btn.innerText = '🎤 Record';

        // If there's text in the input after recording, submit it automatically
        const input = document.getElementById('taskInput');
        const text = input ? input.value : '';
        if (text && text.trim() !== '') {
            addMessage('🎤 Detected: ' + text, 'user');
            // Auto-submit the recognized text so voice commands behave like text commands
            sendTask();
        } else {
            addMessage('⚠️ No speech detected.', 'bot');
        }
    };
}

function toggleRecording() {
    initSpeechRecognition();
    if (!recognition) return;

    try {
        if (isRecording) {
            recognition.stop();
        } else {
            // Clear previous input only if empty to avoid overwriting typed text
            const input = document.getElementById('taskInput');
            if (input && (!input.value || input.value.trim() === '')) input.value = '';
            recognition.start();
        }
    } catch (err) {
        console.error('toggleRecording error', err);
        addMessage('⚠️ Could not start/stop recording: ' + err.message, 'bot');
    }
}

// Wire the record button when the script loads
document.addEventListener('DOMContentLoaded', () => {
    const btn = document.getElementById('recordButton');
    if (btn) btn.addEventListener('click', toggleRecording);
});

// Apply theme based on emotion select
function applyThemeFromEmotion() {
    const sel = document.getElementById('emotionSelect');
    if (!sel) return;
    const val = sel.value || 'default';
    document.body.classList.remove('theme-happy', 'theme-sad', 'theme-angry');
    if (val === 'happy') document.body.classList.add('theme-happy');
    else if (val === 'sad') document.body.classList.add('theme-sad');
    else if (val === 'angry') document.body.classList.add('theme-angry');
}

// Attach emotion change handler and apply on load
document.addEventListener('DOMContentLoaded', () => {
    const sel = document.getElementById('emotionSelect');
    if (sel) {
        sel.addEventListener('change', applyThemeFromEmotion);
    }
    applyThemeFromEmotion();
    // Render welcome box at load
    try { renderWelcomeBox(); } catch (e) { console.warn('renderWelcomeBox failed', e); }
});

// Render a large welcome box with options inside the chat area
function renderWelcomeBox() {
    const chatBox = document.getElementById('chatBox');
    if (!chatBox) return;

    // Avoid duplicating
    if (document.querySelector('.welcome-full')) return;

    const div = document.createElement('div');
    div.className = 'chat-message bot-msg welcome-full';

    const title = document.createElement('div');
    title.className = 'welcome-title';
    title.innerText = 'Hi — how can I help you?';

    const subtitle = document.createElement('div');
    subtitle.className = 'welcome-sub';
    subtitle.innerText = 'Choose an option below to get started';

    const opts = document.createElement('div');
    opts.className = 'welcome-options';

    const modes = [
        {v: 'default', t: 'Robot'},
        {v: 'teacher', t: 'Teacher'},
        {v: 'storyteller', t: 'Storyteller'},
        {v: 'emotional', t: 'Emotional'},
        {v: 'motivational', t: 'Motivational'}
    ];

    modes.forEach(m => {
        const b = document.createElement('button');
        b.className = 'opt-btn';
        b.innerText = m.t;
        b.onclick = () => {
            const sel = document.getElementById('modeSelect');
            if (sel) sel.value = m.v;
            // remove welcome box once a choice is made
            const w = document.querySelector('.welcome-full');
            if (w) w.remove();
            // focus input so user can type
            const input = document.getElementById('taskInput');
            if (input) input.focus();
        };
        opts.appendChild(b);
    });

    // Language quick picker inside welcome
    const langRow = document.createElement('div');
    langRow.className = 'welcome-langrow';
    langRow.innerHTML = `<label style="font-weight:600;margin-right:8px">Language:</label>`;
    const langSel = document.createElement('select');
    const subject = (document.getElementById('subjectSelect') || {}).value || '';
    langSel.innerHTML = document.getElementById('languageSelect').innerHTML;
    langSel.onchange = () => {
        const mainLang = document.getElementById('languageSelect');
        if (mainLang) mainLang.value = langSel.value;
    };
    langRow.appendChild(langSel);

    // Start / Ask button
    const startRow = document.createElement('div');
    startRow.className = 'welcome-startrow';
    const startBtn = document.createElement('button');
    startBtn.className = 'start-btn';
    startBtn.innerText = 'Start';
    startBtn.onclick = () => {
        // sync language select
        const mainLang = document.getElementById('languageSelect');
        if (mainLang) mainLang.value = langSel.value;
        // remove welcome and focus input
        const w = document.querySelector('.welcome-full');
        if (w) w.remove();
        const input = document.getElementById('taskInput');
        if (input) input.focus();
    };
    startRow.appendChild(startBtn);

    div.appendChild(title);
    div.appendChild(subtitle);
    div.appendChild(opts);
    div.appendChild(langRow);
    div.appendChild(startRow);

    // insert at top
    if (chatBox.firstChild) chatBox.insertBefore(div, chatBox.firstChild);
    else chatBox.appendChild(div);
    chatBox.scrollTop = 0;
}

// Show welcome when page loads
document.addEventListener('DOMContentLoaded', () => {
    renderWelcomeBox();
});

// Robot animation
function simulateRobot(steps) {
    let index = 0;

    function nextStep() {
        if (index >= steps.length) {
            showRobot("idle");
            document.getElementById("robotAction").innerText = "Task Complete!";
            speak("Task completed.");
            return;
        }

        let step = steps[index];
        document.getElementById("robotAction").innerText = "Performing: " + step;
        showRobot("work");

        index++;
        setTimeout(nextStep, 2000);
    }

    nextStep();
}

function showRobot(mode) {
    let img = document.getElementById("robotImage");

    const area = document.querySelector('.robot-area');
    const statusEl = document.getElementById('robotStatus');

    // clear state classes
    if (area) {
        area.classList.remove('idle', 'work', 'error');
    }

    if (mode === "idle") {
        img.src = "assests/images/robot_idle.png";
        if (area) area.classList.add('idle');
        if (statusEl) statusEl.innerText = 'Status: idle';
    } else if (mode === "work") {
        img.src = "assests/images/robot_working.gif";
        if (area) area.classList.add('work');
        if (statusEl) statusEl.innerText = 'Status: working';
    } else {
        img.src = "assests/images/robot_error.png";
        if (area) area.classList.add('error');
        if (statusEl) statusEl.innerText = 'Status: error';
    }
}
