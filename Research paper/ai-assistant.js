// AI Assistant for FlowLang

class AIAssistant {
    constructor() {
        this.conversationHistory = [];
    }

    // Simulate AI responses (in a real app, this would call an AI API)
    async processMessage(userMessage, codeContext = '') {
        return new Promise((resolve) => {
            setTimeout(() => {
                const message = userMessage.toLowerCase();
                
                // Spelling correction
                if (message.includes('spell') || message.includes('correct') || message.includes('fix spelling')) {
                    resolve(this.correctSpelling(userMessage, codeContext));
                    return;
                }

                // Code correction
                if (message.includes('fix') || message.includes('error') || message.includes('bug') || message.includes('wrong')) {
                    resolve(this.correctCode(codeContext));
                    return;
                }

                // Build/create features
                if (message.includes('build') || message.includes('create') || message.includes('make') || message.includes('generate')) {
                    resolve(this.buildFeature(userMessage, codeContext));
                    return;
                }

                // General help
                if (message.includes('help') || message.includes('how') || message.includes('what')) {
                    resolve(this.provideHelp(userMessage));
                    return;
                }

                // Default response
                resolve(this.defaultResponse(userMessage, codeContext));
            }, 300); // Small delay to simulate AI processing
        });
    }

    correctSpelling(text, code) {
        // Simple spelling correction for SimpleLang (only 3 commands!)
        const corrections = {
            'sy': 'say',
            'sya': 'say',
            'mak': 'make',
            'maek': 'make',
            'aks': 'ask',
            'as': 'ask'
        };

        let corrected = text;
        for (let [wrong, right] of Object.entries(corrections)) {
            const regex = new RegExp(`\\b${wrong}\\b`, 'gi');
            corrected = corrected.replace(regex, right);
        }

        if (code) {
            let correctedCode = code;
            for (let [wrong, right] of Object.entries(corrections)) {
                const regex = new RegExp(`\\b${wrong}\\b`, 'gi');
                correctedCode = correctedCode.replace(regex, right);
            }
            return {
                message: `I found and corrected some spelling mistakes:\n\n${corrected}\n\nHere's your corrected code:\n\`\`\`\n${correctedCode}\n\`\`\``,
                code: correctedCode
            };
        }

        return {
            message: `I corrected the spelling: "${corrected}"`,
            code: null
        };
    }

    correctCode(code) {
        if (!code || code.trim() === '') {
            return {
                message: 'Please provide the code you want me to fix.',
                code: null
            };
        }

        // Common error patterns for SimpleLang (only 3 commands!)
        const fixes = [
            {
                pattern: /sy\s+|sya\s+/gi,
                replacement: 'say ',
                description: 'Fixed "sy/sya" → "say"'
            },
            {
                pattern: /mak\s+|maek\s+/gi,
                replacement: 'make ',
                description: 'Fixed "mak/maek" → "make"'
            },
            {
                pattern: /aks\s+|as\s+/gi,
                replacement: 'ask ',
                description: 'Fixed "aks/as" → "ask"'
            },
            {
                pattern: /say\s+([^"]+?)(?=\n|$)/g,
                replacement: (match, p1) => {
                    if (!p1.trim().startsWith('"') && !p1.trim().match(/^\d/)) {
                        return `say "${p1.trim()}"`;
                    }
                    return match;
                },
                description: 'Added quotes to say statements'
            }
        ];

        let correctedCode = code;
        const appliedFixes = [];

        for (let fix of fixes) {
            if (fix.pattern.test(correctedCode)) {
                correctedCode = correctedCode.replace(fix.pattern, fix.replacement);
                appliedFixes.push(fix.description);
            }
        }

        if (appliedFixes.length > 0) {
            return {
                message: `I found and fixed ${appliedFixes.length} issue(s):\n${appliedFixes.map(f => `• ${f}`).join('\n')}\n\nCorrected code:\n\`\`\`\n${correctedCode}\n\`\`\``,
                code: correctedCode
            };
        }

        return {
            message: 'I reviewed your code and it looks correct! If you\'re experiencing an error, please share the error message.',
            code: null
        };
    }

    buildFeature(request, codeContext) {
        const examples = {
            'calculator': `say "Calculator"
make a 10
make b 5
make sum a + b
make diff a - b
make prod a * b
say "Sum: "
say sum
say "Difference: "
say diff
say "Product: "
say prod`,

            'greeting': `say "Welcome!"
ask "What is your name?" name
say "Hello "
say name
store username name
say "Your name is stored!"`,

            'array': `say "Array Example"
array fruits ["apple", "banana", "orange"]
say fruits[0]
say fruits[1]
add fruits "grape"
say "Added grape!"`,

            'loop': `say "Loop Example"
make i 1
loop i <= 5
    say i
    make i i + 1
endloop
say "Done!"`,

            'storage': `say "Data Storage"
make name "John"
make age 25
store username name
store userage age
say "Data stored!"
view`,

            'function': `say "Function Example"
func greet()
    say "Hello!"
    say "Welcome!"
endfunc

greet()
say "Function called!"`
        };

        for (let [keyword, code] of Object.entries(examples)) {
            if (request.toLowerCase().includes(keyword)) {
                return {
                    message: `I've created a ${keyword} program for you:\n\n\`\`\`\n${code}\n\`\`\``,
                    code: code
                };
            }
        }

        // Generic builder
        return {
            message: `I can help you build various programs! Try asking for:\n• Calculator\n• Array example\n• Loop example\n• Data storage\n• Function example\n• Greeting program\n\nOr describe what you want to build, and I'll create it for you!`,
            code: null
        };
    }

    provideHelp(query) {
        const helpTopics = {
            'syntax': `SimpleLang Commands:
BASIC:
• say "text" - Display text
• make name value - Create variable
• ask "question" name - Get input

ARRAYS:
• array name [item1, item2] - Create array
• add name value - Add to array
• get name index var - Get from array

LOOPS & CONDITIONS:
• if condition ... endif
• loop condition ... endloop

FUNCTIONS:
• func name() ... endfunc
• name() - Call function

STORAGE:
• store key "value" - Store permanently
• view - View stored data
• viewall - View all data`,

            'variables': `Variables in SimpleLang:
• Use "make": make name "John"
• Use "say": say name
• All data is automatically saved!
• Use "viewall" to see all variables`,

            'storage': `Data Storage:
• store key "value" - Store permanently
• view - View stored data
• All variables/arrays auto-save
• Click "View Data" button to see everything`,

            'commands': `SimpleLang - All Commands:
1. SAY - Display
   say "Hello"
   say 10

2. MAKE - Create variable
   make x 10

3. ASK - Get input
   ask "Name?" name

4. ARRAY - Create array
   array items [1, 2, 3]

5. LOOP - Repeat
   loop i < 10 ... endloop

6. STORE - Save data
   store key "value"

7. VIEW - View data
   view
   viewall`
        };

        for (let [topic, help] of Object.entries(helpTopics)) {
            if (query.toLowerCase().includes(topic)) {
                return {
                    message: help,
                    code: null
                };
            }
        }

        return {
            message: `I'm here to help! SimpleLang features:\n• say, make, ask - Basic commands\n• Arrays - Store lists of data\n• Loops & Conditions - Control flow\n• Functions - Reusable code\n• Data Storage - Save permanently\n• view/viewall - View all your data\n\nAsk me to build something or fix your code!`,
            code: null
        };
    }

    defaultResponse(message, code) {
        return {
            message: `I understand you want: "${message}". I can help you:\n• Fix spelling mistakes\n• Correct code errors\n• Build new features\n• Answer questions about SimpleLang\n\nSimpleLang features: variables, arrays, loops, functions, and data storage!\n\nTry: "build a calculator" or "fix my code"!`,
            code: null
        };
    }
}

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
    module.exports = AIAssistant;
}
