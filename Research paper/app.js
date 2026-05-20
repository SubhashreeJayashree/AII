// Main Application Logic

let interpreter = new SimpleLangInterpreter();
let aiAssistant = new AIAssistant();
let aiModeEnabled = false;

// Initialize on page load
document.addEventListener('DOMContentLoaded', function() {
    initializeApp();
});

function initializeApp() {
    // Setup AI mode toggle
    const aiToggle = document.getElementById('aiModeToggle');
    const aiStatus = document.getElementById('aiStatus');
    const aiPanel = document.getElementById('aiPanel');

    aiToggle.addEventListener('change', function() {
        aiModeEnabled = this.checked;
        aiStatus.textContent = `AI Mode: ${aiModeEnabled ? 'ON' : 'OFF'}`;
        if (aiModeEnabled) {
            aiPanel.classList.remove('hidden');
            addAIMessage('assistant', 'Hello! I\'m your AI assistant. I can help you:\n• Fix spelling mistakes\n• Correct code errors\n• Build new features\n• Answer questions\n\nHow can I help you today?');
        } else {
            aiPanel.classList.add('hidden');
        }
    });

    // Setup shell input
    const shellInput = document.getElementById('shellInput');
    shellInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            executeShellCommand(this.value);
            this.value = '';
        }
    });

    // Setup AI input
    const aiInput = document.getElementById('aiInput');
    aiInput.addEventListener('keypress', function(e) {
        if (e.key === 'Enter') {
            sendAIMessage();
        }
    });

    // Welcome message
    addShellOutput('Welcome to SimpleLang!', 'cyan');
    addShellOutput('Easy but powerful - with data storage!', 'yellow');
    addShellOutput('Type "help" to see all commands.', 'yellow');
}

function addShellOutput(text, color = 'white') {
    const shellOutput = document.getElementById('shellOutput');
    const line = document.createElement('div');
    line.className = 'shell-line';
    line.innerHTML = `<span class="color-${color}">${escapeHtml(text)}</span>`;
    shellOutput.appendChild(line);
    shellOutput.scrollTop = shellOutput.scrollHeight;
}

function addShellPrompt(command) {
    const shellOutput = document.getElementById('shellOutput');
    const line = document.createElement('div');
    line.className = 'shell-line';
    line.innerHTML = `<span class="shell-prompt">flowlang&gt;</span> <span class="color-white">${escapeHtml(command)}</span>`;
    shellOutput.appendChild(line);
    shellOutput.scrollTop = shellOutput.scrollHeight;
}

function executeShellCommand(command) {
    if (!command.trim()) return;

    addShellPrompt(command);

    if (command.toLowerCase() === 'help') {
        addShellOutput('SimpleLang - All Commands:', 'cyan');
        addShellOutput('', 'white');
        addShellOutput('BASIC:', 'yellow');
        addShellOutput('  say "text" - Display text/numbers', 'white');
        addShellOutput('  make name value - Create variable', 'white');
        addShellOutput('  ask "question" name - Get input', 'white');
        addShellOutput('', 'white');
        addShellOutput('ARRAYS:', 'yellow');
        addShellOutput('  array name [item1, item2] - Create array', 'white');
        addShellOutput('  add name value - Add to array', 'white');
        addShellOutput('  get name index varname - Get from array', 'white');
        addShellOutput('', 'white');
        addShellOutput('LOOPS & CONDITIONS:', 'yellow');
        addShellOutput('  if condition ... endif - Conditional', 'white');
        addShellOutput('  loop condition ... endloop - Loop', 'white');
        addShellOutput('', 'white');
        addShellOutput('FUNCTIONS:', 'yellow');
        addShellOutput('  func name() ... endfunc - Define function', 'white');
        addShellOutput('  name() - Call function', 'white');
        addShellOutput('', 'white');
        addShellOutput('DATA STORAGE:', 'yellow');
        addShellOutput('  store key "value" - Store permanently', 'white');
        addShellOutput('  view - View stored data', 'white');
        addShellOutput('  viewall - View all variables/arrays', 'white');
        return;
    }

    if (command.toLowerCase() === 'clear') {
        clearShell();
        return;
    }

    if (command.toLowerCase() === 'view' || command.toLowerCase() === 'viewall') {
        if (command.toLowerCase() === 'viewall') {
            viewStoredData();
        } else {
            // Just view permanent storage
            try {
                const stored = localStorage.getItem('simplelang_storage');
                if (stored) {
                    const data = JSON.parse(stored);
                    addShellOutput('--- Stored Data ---', 'yellow');
                    for (let key in data) {
                        addShellOutput(`${key}: ${data[key]}`, 'white');
                    }
                } else {
                    addShellOutput('No stored data found', 'yellow');
                }
            } catch (e) {
                addShellOutput('Error viewing data', 'red');
            }
        }
        return;
    }

    interpreter.runLine(command, function(text, color) {
        addShellOutput(text, color || 'green');
    });
}

function runCode() {
    const codeEditor = document.getElementById('codeEditor');
    const code = codeEditor.value;
    
    if (!code.trim()) {
        addShellOutput('No code to run!', 'red');
        return;
    }

    addShellOutput('--- Running Code ---', 'yellow');
    
    interpreter.reset();
    const lines = code.split('\n');
    for (let line of lines) {
        interpreter.runLine(line, function(text, color) {
            addShellOutput(text, color || 'green');
        });
    }
    
    addShellOutput('--- Code Execution Complete ---', 'yellow');
}

function clearEditor() {
    document.getElementById('codeEditor').value = '';
}

function clearShell() {
    document.getElementById('shellOutput').innerHTML = '';
    addShellOutput('Shell cleared. Welcome back!', 'cyan');
}

function loadExample() {
    const example = `say "Welcome to SimpleLang!"
say "Easy but powerful!"

# Variables
make name "Alice"
make age 25
say name
say age

# Math
make total 10 + 20
say total

# Arrays
array fruits ["apple", "banana", "orange"]
say "Fruits:"
say fruits[0]
say fruits[1]

# Add to array
add fruits "grape"
say "Added grape!"

# Store data permanently
store username "Alice"
store email "alice@example.com"

# View stored data
view

# Loop
make count 1
loop count <= 5
    say count
    make count count + 1
endloop

# Conditional
make score 85
if score >= 80
    say "Great score!"
else
    say "Try harder!"
endif

say "Done!"`;
    
    document.getElementById('codeEditor').value = example;
}

function viewStoredData() {
    const data = interpreter.getAllData();
    
    addShellOutput('=== STORED DATA ===', 'yellow');
    
    // Variables
    addShellOutput('Variables:', 'cyan');
    if (Object.keys(data.variables).length > 0) {
        for (let key in data.variables) {
            addShellOutput(`  ${key} = ${data.variables[key]}`, 'white');
        }
    } else {
        addShellOutput('  (none)', 'white');
    }
    
    // Arrays
    addShellOutput('Arrays:', 'cyan');
    if (Object.keys(data.arrays).length > 0) {
        for (let key in data.arrays) {
            addShellOutput(`  ${key} = [${data.arrays[key].join(', ')}]`, 'white');
        }
    } else {
        addShellOutput('  (none)', 'white');
    }
    
    // Functions
    addShellOutput('Functions:', 'cyan');
    if (Object.keys(data.functions).length > 0) {
        for (let key in data.functions) {
            addShellOutput(`  ${key}()`, 'white');
        }
    } else {
        addShellOutput('  (none)', 'white');
    }
    
    // Permanent storage
    addShellOutput('Permanent Storage:', 'cyan');
    if (Object.keys(data.stored).length > 0) {
        for (let key in data.stored) {
            addShellOutput(`  ${key} = ${data.stored[key]}`, 'white');
        }
    } else {
        addShellOutput('  (none)', 'white');
    }
    
    addShellOutput('==================', 'yellow');
}

function sendAIMessage() {
    const aiInput = document.getElementById('aiInput');
    const message = aiInput.value.trim();
    
    if (!message) return;

    // Add user message
    addAIMessage('user', message);

    // Get current code context
    const codeContext = document.getElementById('codeEditor').value;

    // Process with AI
    aiAssistant.processMessage(message, codeContext).then(response => {
        addAIMessage('assistant', response.message);
        
        // If AI provided corrected code, update editor
        if (response.code) {
            document.getElementById('codeEditor').value = response.code;
            addAIMessage('assistant', '✅ Code has been updated in the editor!');
        }
    });

    aiInput.value = '';
}

function addAIMessage(type, text) {
    const aiChat = document.getElementById('aiChat');
    const messageDiv = document.createElement('div');
    messageDiv.className = `ai-message ${type}`;
    
    // Format code blocks
    let formattedText = escapeHtml(text);
    formattedText = formattedText.replace(/```([\s\S]*?)```/g, '<pre><code>$1</code></pre>');
    formattedText = formattedText.replace(/\n/g, '<br>');
    
    messageDiv.innerHTML = formattedText;
    aiChat.appendChild(messageDiv);
    aiChat.scrollTop = aiChat.scrollHeight;
}

function downloadPDF() {
    // Open the markdown guide in a new window for printing/saving as PDF
    const guideWindow = window.open('', '_blank');
    guideWindow.document.write(`
        <!DOCTYPE html>
        <html>
        <head>
            <title>FlowLang - Beginner's Guide</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    max-width: 800px;
                    margin: 40px auto;
                    padding: 20px;
                    line-height: 1.6;
                }
                h1 { color: #667eea; }
                h2 { color: #764ba2; margin-top: 30px; }
                code {
                    background: #f4f4f4;
                    padding: 2px 6px;
                    border-radius: 3px;
                    font-family: 'Courier New', monospace;
                }
                pre {
                    background: #1e1e1e;
                    color: #d4d4d4;
                    padding: 15px;
                    border-radius: 5px;
                    overflow-x: auto;
                }
                @media print {
                    body { margin: 0; }
                    @page { margin: 2cm; }
                }
            </style>
        </head>
        <body>
            <h1>SimpleLang - Complete Guide</h1>
            <p><strong>Welcome to SimpleLang!</strong> The simplest programming language - only 3 commands!</p>
            
            <h2>Only 3 Commands!</h2>
            <h3>1. SAY - Display Text or Numbers</h3>
            <pre><code>say "Hello World"
say 42
say myname</code></pre>
            
            <h3>2. MAKE - Create Variables</h3>
            <pre><code>make name "Alice"
make age 25
make total 10 + 20</code></pre>
            
            <h3>3. ASK - Get User Input</h3>
            <pre><code>ask "What is your name?" name
say name</code></pre>
            
            <h2>Examples</h2>
            <h3>Simple Program</h3>
            <pre><code>say "Hello!"
make x 10
say x</code></pre>
            
            <h3>Greeting Program</h3>
            <pre><code>say "Welcome!"
ask "What is your name?" name
say "Hello "
say name</code></pre>
            
            <h3>Math Example</h3>
            <pre><code>make a 10
make b 5
make sum a + b
say sum</code></pre>
            
            <h2>AI Assistant Features</h2>
            <p>The AI Assistant can:</p>
            <ul>
                <li>Fix spelling mistakes</li>
                <li>Correct code errors</li>
                <li>Build programs for you</li>
                <li>Answer questions</li>
            </ul>
            
            <h2>Tips</h2>
            <ul>
                <li>Use quotes for text: <code>"Hello"</code></li>
                <li>No quotes for numbers: <code>10</code></li>
                <li>That's it! Only 3 commands!</li>
            </ul>
            
            <p style="margin-top: 40px; text-align: center; color: #667eea;">
                <strong>Happy Coding with SimpleLang! 🌟</strong>
            </p>
            <p style="text-align: center; color: #666;">
                Only 3 commands: say, make, ask - That's all you need!
            </p>
        </body>
        </html>
    `);
    guideWindow.document.close();
    
    // Show message
    addShellOutput('PDF guide opened in new window! Use browser Print (Ctrl+P) to save as PDF.', 'green');
}

function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}
