// SimpleLang Interpreter - Easy but Powerful!

class SimpleLangInterpreter {
    constructor() {
        this.variables = {};
        this.arrays = {};
        this.functions = {};
        this.state = {
            in_if: false,
            if_cond_true: false,
            in_else: false,
            in_loop: false,
            loop_cond: null,
            loop_body: [],
            in_function: false,
            function_name: null,
            function_body: []
        };
        this.loadData(); // Load stored data
    }

    // Load data from localStorage
    loadData() {
        try {
            const stored = localStorage.getItem('simplelang_data');
            if (stored) {
                const data = JSON.parse(stored);
                this.variables = data.variables || {};
                this.arrays = data.arrays || {};
                this.functions = data.functions || {};
            }
        } catch (e) {
            console.error('Error loading data:', e);
        }
    }

    // Save data to localStorage
    saveData() {
        try {
            const data = {
                variables: this.variables,
                arrays: this.arrays,
                functions: this.functions
            };
            localStorage.setItem('simplelang_data', JSON.stringify(data));
        } catch (e) {
            console.error('Error saving data:', e);
        }
    }

    reset() {
        // Don't reset stored data, just clear runtime state
        this.state = {
            in_if: false,
            if_cond_true: false,
            in_else: false,
            in_loop: false,
            loop_cond: null,
            loop_body: [],
            in_function: false,
            function_name: null,
            function_body: []
        };
    }

    // Get value - handles numbers, text, variables, arrays
    getValue(expr) {
        expr = expr.trim();
        
        // Array access: name[index]
        const arrayMatch = expr.match(/^(\w+)\[(\d+)\]$/);
        if (arrayMatch) {
            const [, name, index] = arrayMatch;
            if (this.arrays[name] && this.arrays[name][parseInt(index)]) {
                return this.arrays[name][parseInt(index)];
            }
            return null;
        }
        
        // If it's a number
        if (/^-?\d+(\.\d+)?$/.test(expr)) {
            return parseFloat(expr);
        }
        
        // If it's text (in quotes)
        if ((expr.startsWith('"') && expr.endsWith('"')) || 
            (expr.startsWith("'") && expr.endsWith("'"))) {
            return expr.slice(1, -1);
        }
        
        // If it's a variable
        if (this.variables.hasOwnProperty(expr)) {
            return this.variables[expr];
        }
        
        // Try math expression
        try {
            let mathExpr = expr;
            // Replace variables
            for (let varName in this.variables) {
                const regex = new RegExp(`\\b${varName}\\b`, 'g');
                mathExpr = mathExpr.replace(regex, this.variables[varName]);
            }
            // Evaluate if it's pure math
            if (/^[\d+\-*/().\s]+$/.test(mathExpr)) {
                return eval(mathExpr);
            }
        } catch (e) {
            // Not a math expression
        }
        
        return expr;
    }

    // Evaluate condition
    evalCondition(cond) {
        cond = cond.trim();
        
        // Replace variables
        for (let varName in this.variables) {
            const regex = new RegExp(`\\b${varName}\\b`, 'g');
            cond = cond.replace(regex, this.variables[varName]);
        }
        
        // Simple comparisons
        if (cond.includes('>=')) {
            const [a, b] = cond.split('>=').map(x => parseFloat(x.trim()));
            return a >= b;
        }
        if (cond.includes('<=')) {
            const [a, b] = cond.split('<=').map(x => parseFloat(x.trim()));
            return a <= b;
        }
        if (cond.includes('==')) {
            const [a, b] = cond.split('==').map(x => x.trim());
            return this.getValue(a) == this.getValue(b);
        }
        if (cond.includes('!=')) {
            const [a, b] = cond.split('!=').map(x => x.trim());
            return this.getValue(a) != this.getValue(b);
        }
        if (cond.includes('>')) {
            const [a, b] = cond.split('>').map(x => parseFloat(x.trim()));
            return a > b;
        }
        if (cond.includes('<')) {
            const [a, b] = cond.split('<').map(x => parseFloat(x.trim()));
            return a < b;
        }
        
        return Boolean(this.getValue(cond));
    }

    // Process one line
    runLine(line, outputCallback) {
        line = line.trim();
        
        // Skip empty lines and comments
        if (!line || line.startsWith('#')) {
            return;
        }

        const state = this.state;

        // FUNCTION DEFINITION
        if (line.startsWith('func ')) {
            const rest = line.substring(5).trim();
            const match = rest.match(/^(\w+)\s*\(([^)]*)\)$/);
            if (match) {
                state.in_function = true;
                state.function_name = match[1];
                state.function_body = [];
                return;
            }
        }

        // END FUNCTION
        if (line === 'endfunc') {
            if (state.in_function) {
                this.functions[state.function_name] = {
                    body: state.function_body,
                    params: []
                };
                state.in_function = false;
                state.function_name = null;
                state.function_body = [];
            }
            return;
        }

        // If recording function body
        if (state.in_function) {
            state.function_body.push(line);
            return;
        }

        // CALL FUNCTION
        if (line.includes('(') && line.includes(')')) {
            const match = line.match(/^(\w+)\s*\(([^)]*)\)$/);
            if (match && this.functions[match[1]]) {
                const func = this.functions[match[1]];
                // Execute function body
                for (let bline of func.body) {
                    this.runLine(bline, outputCallback);
                }
                return;
            }
        }

        // IF STATEMENT
        if (line.startsWith('if ')) {
            const cond = line.substring(3).trim();
            const condVal = this.evalCondition(cond);
            state.in_if = true;
            state.if_cond_true = condVal;
            state.in_else = false;
            return;
        }

        // ELSE
        if (line === 'else') {
            if (state.in_if) {
                state.in_else = true;
            }
            return;
        }

        // ENDIF
        if (line === 'endif') {
            state.in_if = false;
            state.in_else = false;
            return;
        }

        // LOOP
        if (line.startsWith('loop ')) {
            const cond = line.substring(5).trim();
            state.in_loop = true;
            state.loop_cond = cond;
            state.loop_body = [];
            return;
        }

        // ENDLOOP
        if (line === 'endloop') {
            if (state.in_loop && state.loop_cond) {
                // Check condition first
                if (this.evalCondition(state.loop_cond)) {
                    // Execute loop body
                    const bodyCopy = [...state.loop_body];
                    for (let bline of bodyCopy) {
                        this.runLine(bline, outputCallback);
                    }
                    // Re-evaluate condition and loop again if true
                    if (this.evalCondition(state.loop_cond)) {
                        // Will continue looping on next endloop
                        return;
                    } else {
                        // Exit loop
                        state.in_loop = false;
                        state.loop_cond = null;
                        state.loop_body = [];
                    }
                } else {
                    // Exit loop
                    state.in_loop = false;
                    state.loop_cond = null;
                    state.loop_body = [];
                }
            }
            return;
        }

        // If recording loop body
        if (state.in_loop) {
            state.loop_body.push(line);
            return;
        }

        // If inside if/else, only execute if condition matches
        if (state.in_if) {
            const execute = (state.if_cond_true && !state.in_else) || 
                          ((!state.if_cond_true) && state.in_else);
            if (!execute) {
                return;
            }
        }

        // SAY - Display
        if (line.startsWith('say ')) {
            const text = line.substring(4).trim();
            const value = this.getValue(text);
            outputCallback(String(value), 'green');
            return;
        }

        // MAKE - Create variable
        if (line.startsWith('make ')) {
            const rest = line.substring(5).trim();
            const parts = rest.split(/\s+/);
            
            if (parts.length < 2) {
                outputCallback('Error: Use "make name value"', 'red');
                return;
            }
            
            const name = parts[0];
            const valueExpr = parts.slice(1).join(' ');
            const value = this.getValue(valueExpr);
            
            this.variables[name] = value;
            this.saveData(); // Auto-save
            return;
        }

        // ARRAY - Create array
        if (line.startsWith('array ')) {
            const rest = line.substring(6).trim();
            const match = rest.match(/^(\w+)\s+\[(.*)\]$/);
            if (match) {
                const name = match[1];
                const items = match[2].split(',').map(item => this.getValue(item.trim()));
                this.arrays[name] = items;
                this.saveData();
                return;
            }
            outputCallback('Error: Use "array name [item1, item2, ...]"', 'red');
            return;
        }

        // ADD - Add to array
        if (line.startsWith('add ')) {
            const rest = line.substring(4).trim();
            const match = rest.match(/^(\w+)\s+(.+)$/);
            if (match) {
                const [, name, value] = match;
                if (!this.arrays[name]) {
                    this.arrays[name] = [];
                }
                this.arrays[name].push(this.getValue(value.trim()));
                this.saveData();
                return;
            }
            outputCallback('Error: Use "add arrayname value"', 'red');
            return;
        }

        // GET - Get from array
        if (line.startsWith('get ')) {
            const rest = line.substring(4).trim();
            const match = rest.match(/^(\w+)\s+(\d+)\s+(\w+)$/);
            if (match) {
                const [, arrName, index, varName] = match;
                if (this.arrays[arrName] && this.arrays[arrName][parseInt(index)]) {
                    this.variables[varName] = this.arrays[arrName][parseInt(index)];
                    this.saveData();
                    return;
                }
            }
            outputCallback('Error: Use "get arrayname index varname"', 'red');
            return;
        }

        // STORE - Store data permanently
        if (line.startsWith('store ')) {
            const rest = line.substring(6).trim();
            const match = rest.match(/^(\w+)\s+"([^"]+)"$/);
            if (match) {
                const [, key, value] = match;
                try {
                    let stored = {};
                    const existing = localStorage.getItem('simplelang_storage');
                    if (existing) {
                        stored = JSON.parse(existing);
                    }
                    stored[key] = value;
                    localStorage.setItem('simplelang_storage', JSON.stringify(stored));
                    outputCallback(`Stored: ${key} = ${value}`, 'cyan');
                    return;
                } catch (e) {
                    outputCallback('Error storing data', 'red');
                    return;
                }
            }
            outputCallback('Error: Use "store key "value""', 'red');
            return;
        }

        // VIEW - View stored data
        if (line === 'view') {
            try {
                const stored = localStorage.getItem('simplelang_storage');
                if (stored) {
                    const data = JSON.parse(stored);
                    outputCallback('--- Stored Data ---', 'yellow');
                    for (let key in data) {
                        outputCallback(`${key}: ${data[key]}`, 'white');
                    }
                } else {
                    outputCallback('No stored data found', 'yellow');
                }
                return;
            } catch (e) {
                outputCallback('Error viewing data', 'red');
                return;
            }
        }

        // VIEWALL - View all variables, arrays, functions
        if (line === 'viewall') {
            outputCallback('--- All Data ---', 'yellow');
            outputCallback('Variables:', 'cyan');
            for (let key in this.variables) {
                outputCallback(`  ${key} = ${this.variables[key]}`, 'white');
            }
            outputCallback('Arrays:', 'cyan');
            for (let key in this.arrays) {
                outputCallback(`  ${key} = [${this.arrays[key].join(', ')}]`, 'white');
            }
            outputCallback('Functions:', 'cyan');
            for (let key in this.functions) {
                outputCallback(`  ${key}()`, 'white');
            }
            return;
        }

        // ASK - Get input
        if (line.startsWith('ask ')) {
            const rest = line.substring(4).trim();
            const match = rest.match(/^"([^"]+)"\s+(\w+)$/);
            if (!match) {
                outputCallback('Error: Use "ask "question" name"', 'red');
                return;
            }
            const [, question, varName] = match;
            const answer = prompt(question);
            this.variables[varName] = answer || '';
            this.saveData();
            outputCallback(`Got: ${answer || ''}`, 'cyan');
            return;
        }

        // Unknown command
        outputCallback(`Error: Unknown command. Type "help" for commands`, 'red');
    }

    // Run multiple lines
    runCode(code, outputCallback) {
        this.reset();
        const lines = code.split('\n');
        for (let line of lines) {
            this.runLine(line, outputCallback);
        }
    }

    // Get all data for viewing
    getAllData() {
        return {
            variables: this.variables,
            arrays: this.arrays,
            functions: this.functions,
            stored: (() => {
                try {
                    const stored = localStorage.getItem('simplelang_storage');
                    return stored ? JSON.parse(stored) : {};
                } catch {
                    return {};
                }
            })()
        };
    }
}

// Export
if (typeof module !== 'undefined' && module.exports) {
    module.exports = SimpleLangInterpreter;
}
