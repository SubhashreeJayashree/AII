from __future__ import annotations
import http.server
import socketserver
import json
import io
import sys
import os
from typing import Any, Tuple, Optional, List, Dict, cast

PORT = 8555
AINO_API_KEY = os.getenv("AINO_API_KEY", "")

# --- AION CORE ENGINE (RESTORED & UPGRADED) ---

class Lexer:
    def __init__(self, code: str):
        self.code = code
        self.tokens: List[str] = []
    
    def tokenize(self) -> List[str]:
        tokens: List[str] = []
        current: List[str] = []
        in_quotes = False
        
        code_str = str(self.code)
        for i in range(len(code_str)):
            char = code_str[i]
            if char == '"':
                if in_quotes:
                    current.append(char)
                    tokens.append("".join(current))
                    current = []
                    in_quotes = False
                else:
                    if current:
                        tokens.append("".join(current))
                        current = []
                    in_quotes = True
                    current.append(char)
            elif in_quotes:
                current.append(char)
            elif char.isspace():
                if current:
                    tokens.append("".join(current))
                    current = []
            elif char in "{}();=+-*/<>(),":
                if current:
                    tokens.append("".join(current))
                    current = []
                tokens.append(char)
            else:
                current.append(char)
        if current:
            tokens.append("".join(current))
        self.tokens = tokens
        return self.tokens

class Parser:
    def __init__(self, tokens: List[str]):
        self.tokens = tokens
    def parse(self) -> Dict[str, Any]:
        return {"AST": self.tokens}

class Interpreter:
    def __init__(self, ast: Dict[str, Any]):
        self.ast = ast
        self.variables: Dict[str, Any] = {}
        self.functions: Dict[str, Tuple[List[str], List[str]]] = {}
    
    def eval_expression(self, expr_tokens: List[str], local_vars: Optional[Dict[str, Any]] = None) -> Any:
        def aion_call(name: str, *args: Any) -> Any:
            if name in self.functions:
                return self.call_function(name, list(args))
            return None
        ctx = {**self.variables, **(local_vars or {})}
        for f_name in self.functions: ctx[f_name] = lambda *a, n=f_name: aion_call(n, *a)
        expr = " ".join([str(t) for t in expr_tokens])
        if len(expr_tokens) == 1 and str(expr_tokens[0]).startswith('"') and str(expr_tokens[0]).endswith('"'):
            return str(expr_tokens[0]).strip('"')
        try: return eval(expr, {"__builtins__": {}}, ctx)
        except Exception: return None

    def call_function(self, name: str, args: List[Any]) -> Any:
        params, body = self.functions[name]
        return self.run_block(body, dict(zip(params, args)))

    def run_block(self, b_body: List[str], b_vars: Dict[str, Any]) -> Any:
        pc_idx: int = 0
        while pc_idx < len(b_body):
            curr_tok = str(b_body[pc_idx])
            if (pc_idx + 1) < len(b_body) and str(b_body[pc_idx + 1]) == "=":
                l_expr_tks: List[str] = []
                j_l: int = pc_idx + 2
                while j_l < len(b_body) and str(b_body[j_l]) != ";":
                    l_expr_tks.append(str(b_body[j_l]))
                    j_l = j_l + 1
                b_vars[curr_tok] = self.eval_expression(l_expr_tks, b_vars)
                pc_idx = j_l + 1
            elif curr_tok == "return":
                r_expr_tks: List[str] = []
                j_r: int = pc_idx + 1
                while j_r < len(b_body) and str(b_body[j_r]) != ";":
                    r_expr_tks.append(str(b_body[j_r]))
                    j_r = j_r + 1
                return self.eval_expression(r_expr_tks, b_vars)
            elif curr_tok == "if":
                i_expr_tks: List[str] = []
                j_i: int = pc_idx + 2
                while j_i < len(b_body) and str(b_body[j_i]) != ")":
                    i_expr_tks.append(str(b_body[j_i]))
                    j_i = j_i + 1
                condition_res = self.eval_expression(i_expr_tks, b_vars)
                j_b: int = j_i + 2
                i_block: List[str] = []
                i_depth: int = 1
                while j_b < len(b_body) and i_depth > 0:
                    char_tok = str(b_body[j_b])
                    if char_tok == "{": i_depth = i_depth + 1
                    elif char_tok == "}": i_depth = i_depth - 1
                    if i_depth > 0: i_block.append(char_tok)
                    j_b = j_b + 1
                if condition_res:
                    i_ret = self.run_block(i_block, b_vars)
                    if i_ret is not None: return i_ret
                    pc_idx = j_b
                elif j_b < len(b_body) and str(b_body[j_b]) == "else":
                    j_e: int = j_b + 2
                    e_block_list: List[str] = []
                    e_depth_count: int = 1
                    while j_e < len(b_body) and e_depth_count > 0:
                        char_e = str(b_body[j_e])
                        if char_e == "{": e_depth_count = e_depth_count + 1
                        elif char_e == "}": e_depth_count = e_depth_count - 1
                        if e_depth_count > 0: e_block_list.append(char_e)
                        j_e = j_e + 1
                    e_ret = self.run_block(e_block_list, b_vars)
                    if e_ret is not None: return e_ret
                    pc_idx = j_e
                else: pc_idx = j_b
                continue
            else: pc_idx = pc_idx + 1
        return None

    def run(self):
        r_tks: List[str] = cast(List[str], [str(t) for t in self.ast.get("AST", [])])
        r_pc: int = 0
        while r_pc < len(r_tks):
            r_tok: str = str(r_tks[r_pc])
            if r_tok == "func":
                f_name: str = str(r_tks[r_pc + 1])
                f_params: List[str] = []
                f_j_p: int = r_pc + 3
                while f_j_p < len(r_tks) and str(r_tks[f_j_p]) != ")":
                    if str(r_tks[f_j_p]) != ",": f_params.append(str(r_tks[f_j_p]))
                    f_j_p = f_j_p + 1
                f_j_b: int = f_j_p + 2
                f_body: List[str] = []
                f_depth: int = 1
                while f_j_b < len(r_tks) and f_depth > 0:
                    f_char = str(r_tks[f_j_b])
                    if f_char == "{": f_depth = f_depth + 1
                    elif f_char == "}": f_depth = f_depth - 1
                    if f_depth > 0: f_body.append(f_char)
                    f_j_b = f_j_b + 1
                self.functions[f_name] = (f_params, f_body)
                r_pc = f_j_b
            elif r_tok in self.functions:
                f_args: List[Any] = []
                f_j_a: int = r_pc + 2
                while f_j_a < len(r_tks) and str(r_tks[f_j_a]) != ")":
                    if str(r_tks[f_j_a]) != ",": f_args.append(self.eval_expression([str(r_tks[f_j_a])]))
                    f_j_a = f_j_a + 1
                self.call_function(r_tok, f_args)
                r_pc = f_j_a + 1
            elif (r_pc + 1) < len(r_tks) and str(r_tks[r_pc + 1]) == "=":
                a_tks: List[str] = []
                j_a: int = r_pc + 2
                while j_a < len(r_tks) and str(r_tks[j_a]) != ";":
                    a_tks.append(str(r_tks[j_a]))
                    j_a = j_a + 1
                self.variables[r_tok] = self.eval_expression(a_tks)
                r_pc = j_a + 1
            elif r_tok == "task":
                task_val = self.eval_expression([str(r_tks[r_pc + 2])])
                print(f"AI Agent says: {task_val}")
                r_pc = r_pc + 3
            else: r_pc = r_pc + 1

class AINOBrain:
    @staticmethod
    def get_response(prompt: str, code: str) -> str:
        prompt_clean = prompt.lower()
        def box(title: str, content: str, is_code: bool = False) -> str:
            style = "border:1px solid #ff0844; padding:12px; margin:10px 0; border-radius:10px; background:rgba(255,8,68,0.05); position:relative; overflow: hidden;"
            header = f"<div style='color:#ff0844; font-weight:bold; margin-bottom:5px; font-size:12px; text-transform:uppercase; letter-spacing:1px;'>{title}</div>"
            if is_code:
                return f"<div style='{style}'>{header}<pre style='color:#38ef7d; margin:0; font-family:monospace; font-size:13px; overflow-x:auto;'>{content}</pre><button onclick='copyToClipboard(this.parentElement.querySelector(\"pre\").innerText, this)' style='position:absolute; top:8px; right:8px; background:rgba(255,8,68,0.2); color:#fff; border:1px solid #ff0844; border-radius:4px; cursor:pointer; font-size:10px; padding:3px 8px;'>Copy</button></div>"
            return f"<div style='{style}'>{header}<div style='color:#eee; font-size:14px; line-height:1.5;'>{content}</div></div>"

        # NEW: Context Awareness (Answering questions about the current Program)
        if any(w in prompt_clean for w in ["this code", "my program", "explain", "what does", "how does"]):
            analysis = "Looking at your current script... "
            if not code or len(code.strip()) < 5:
                analysis += "I don't see much code yet! Try adding an <code>agent</code> or a <code>task()</code> call so I can analyze your architecture."
            else:
                words: List[str] = code.split()
                agents: List[str] = []
                for i in range(1, len(words)):
                    if words[i-1] == "agent" and words[i].isidentifier():
                        agents.append(words[i])
                tasks = code.count("task(")
                funcs = code.count("func ")
                
                analysis += f"I see you've architected a system with {tasks} task calls"
                if agents: analysis += f" and defined agents like <b>{', '.join(agents)}</b>"
                if funcs: analysis += f". You've also implemented {funcs} custom logic blocks (funcs)"
                analysis += ". Your code flows naturally through the AION engine."
            
            hint = "<b>Hint:</b> You can ask me to 'optimize this' or 'add an agent to my code' for specific suggestions."
            return f"🎨 <b>AINO Code Analysis:</b><br>{box('Neural Program Review', analysis)}{box('Program Hint', hint)}"

        # AI LOGIC: Map many subjects to AION programs with HINTS
        if any(w in prompt_clean for w in ["hi", "hello", "hey", "start"]):
            resp = "Greetings! I've engineered a initialization sequence for your review."
            hint = "<b>Hint:</b> This program uses <code>task()</code> to log system status. Note that variables are declared normally."
            prog = "system_id = \"AION-NX-1\";\ntask(\"Initializing \" + system_id);\ntask(\"All systems functional.\");"
            return f"{resp}<br>{box('AION: Starter Code', prog, True)}{box('Program Hint', hint)}"
        
        if any(w in prompt_clean for w in ["agent", "task", "ai", "subject"]):
            resp = "AION is built for high-level agent orchestration. Here is a multi-agent template."
            hint = "<b>Hint:</b> You can define unique <code>agent</code> blocks to organize tasks. Each agent can perform separate AI task calls."
            prog = "agent Security {\n  task(\"Monitoring firewall streams\");\n}\n\nagent Database {\n  task(\"Optimizing query shards\");\n}\n\ntask(\"Agent swarm active.\");"
            return f"{resp}<br>{box('AION: Agent Logic', prog, True)}{box('Program Hint', hint)}"
        
        if any(w in prompt_clean for w in ["func", "function", "return"]):
            resp = "Modular logic is handled via <code>func</code> blocks in AION."
            hint = "<b>Hint:</b> Functions can take parameters and use <code>return</code> to send data back to the caller."
            prog = "func process(x, y) {\n  val = (x * y) + 10;\n  return val;\n}\n\nresult = process(5, 5);\ntask(\"Processed result: \");\ntask(result);"
            return f"{resp}<br>{box('AION: Functions', prog, True)}{box('Program Hint', hint)}"
        
        if any(w in prompt_clean for w in ["loop", "repeat", "recursive", "while"]):
            resp = "Loops are currently implemented via recursion for maximum safety."
            hint = "<b>Hint:</b> A function calling itself with a decrementing value (<code>n - 1</code>) creates a reliable loop."
            prog = "func loop(n) {\n  task(\"Iteration count: \");\n  task(n);\n  if (n > 1) {\n    return loop(n - 1);\n  }\n  return 0;\n}\n\nloop(3);"
            return f"{resp}<br>{box('AION: Recursion Loop', prog, True)}{box('Program Hint', hint)}"

        if any(w in prompt_clean for w in ["math", "calculation", "arithmetic"]):
            resp = "AION supports native mathematical precedence (BEDMAS)."
            hint = "<b>Hint:</b> You can wrap complex expressions in parentheses to control the order of execution."
            prog = "calc = 100 + (50 * 3) / 2;\ntask(\"Calculation result: \");\ntask(calc);"
            return f"{resp}<br>{box('AION: Math Suite', prog, True)}{box('Program Hint', hint)}"
        
        if any(w in prompt_clean for w in ["logic", "if", "else", "condition"]):
            resp = "Decision-making in AION uses standard boolean logic."
            hint = "<b>Hint:</b> Use <code>if/else</code> blocks to branch your code based on variable values."
            prog = "status = 1;\nif (status == 1) {\n  task(\"System Green\");\n} else {\n  task(\"System Red\");\n}"
            return f"{resp}<br>{box('AION: Logic Gates', prog, True)}{box('Program Hint', hint)}"

        # Final Fallback for ALL other questions
        resp = f"I've synthesized a custom AION architecture for your query: '{prompt}'."
        hint = "<b>Hint:</b> This is a generic AION template that you can customize to fit your specific subject requirements."
        prog = "subject = \"Custom Module\";\ntask(\"Loading \" + subject);\n\nfunc start() {\n  task(\"Executing custom logic sequence\");\n}\n\nstart();"
        return f"{resp}<br>{box('Generated AION Script', prog, True)}{box('Program Hint', hint)}"

# --- BACKEND SERVER ROUTING ---

class AIONHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        # Force index.html for the root path to provide the classic experience
        if self.path == '/' or self.path == '/ide.html':
            self.path = '/index.html'
        return super().do_GET()

    def do_POST(self):
        if self.path == '/execute':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            
            old_stdout = sys.stdout
            sys.stdout = captured_output = io.StringIO()
            
            try:
                data = json.loads(post_data)
                code = data.get('code', '')
                
                # Execute User's Custom AION script logic
                lexer = Lexer(code)
                tokens = lexer.tokenize()
                parser = Parser(tokens)
                ast = parser.parse()
                interpreter = Interpreter(ast)
                interpreter.run()

                sys.stdout = old_stdout
                output = captured_output.getvalue()

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'output': output}).encode())

            except Exception as e:
                sys.stdout = old_stdout
                self.send_response(400)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'error': str(e)}).encode())
                
        elif self.path == '/ask_ai':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length).decode('utf-8')
            data = json.loads(post_data)
            prompt = data.get('prompt', '')
            code = data.get('code', '')
            
            # Use AINOBrain for dynamic agent responses
            response = AINOBrain.get_response(prompt, code)

            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'response': response}).encode())
        else:
            self.send_response(404)
            self.end_headers()

Handler = AIONHandler

class AIONServer(socketserver.TCPServer):
    allow_reuse_address = True

with AIONServer(("", PORT), Handler) as httpd:
    print(f"AION Unified Backend Engine Live at http://localhost:{PORT}")
    httpd.serve_forever()
