import re
import sys

# Simple colors (works in many terminals)
RESET = "\033[0m"
GREEN = "\033[92m"
CYAN = "\033[96m"
YELLOW = "\033[93m"
RED = "\033[91m"

variables = {}


def color(text, c):
    return c + text + RESET


def eval_expr(expr):
    """Very simple expression evaluator that substitutes variables and uses Python eval safely."""

    def repl_var(m):
        name = m.group(0)
        if name in variables:
            return str(variables[name])
        return name

    # Very simple: variables are [a-zA-Z_][a-zA-Z0-9_]*
    expr_sub = re.sub(r"[a-zA-Z_][a-zA-Z0-9_]*", repl_var, expr)
    try:
        # No builtins for safety
        return eval(expr_sub, {"__builtins__": {}})
    except Exception as e:
        print(color(f"[error] cannot evaluate: {expr_sub} ({e})", RED))
        return None


def run_line(line, state):
    line = line.strip()
    if not line or line.startswith("#"):
        return state

    # state for blocks
    in_if = state.get("in_if", False)
    if_cond_true = state.get("if_cond_true", False)
    in_else = state.get("in_else", False)
    in_while = state.get("in_while", False)
    while_cond = state.get("while_cond", None)
    while_body = state.get("while_body", [])

    # Block handling
    if line.startswith("if "):
        cond_expr = line[3:].strip()
        cond_val = bool(eval_expr(cond_expr))
        state["in_if"] = True
        state["if_cond_true"] = cond_val
        state["in_else"] = False
        return state

    if line == "else":
        if not in_if:
            print(color("[error] 'else' without 'if'", RED))
        else:
            state["in_else"] = True
        return state

    if line == "end":
        # End of if / while
        if in_while and while_cond is not None:
            # Re-evaluate while condition
            if bool(eval_expr(while_cond)):
                # Re-run while body
                for bline in while_body:
                    run_line(bline, state)
                return state
            else:
                # Exit while
                state["in_while"] = False
                state["while_cond"] = None
                state["while_body"] = []
                return state
        else:
            # End if
            state["in_if"] = False
            state["in_else"] = False
            return state

    if line.startswith("while "):
        cond_expr = line[6:].strip()
        state["in_while"] = True
        state["while_cond"] = cond_expr
        state["while_body"] = []
        return state

    # If we are recording while body
    if in_while and not line.startswith("end"):
        state["while_body"].append(line)
        return state

    # If inside if/else, only execute if condition matches
    if in_if:
        execute = (if_cond_true and not in_else) or ((not if_cond_true) and in_else)
        if not execute:
            return state

    # Commands
    if line.startswith("show "):
        expr = line[5:].strip()
        val = eval_expr(expr)
        if val is not None:
            print(color(str(val), GREEN))
        return state

    if line.startswith("let "):
        # let name = expr
        rest = line[4:]
        if "=" not in rest:
            print(color("[error] invalid let syntax", RED))
            return state
        name, expr = rest.split("=", 1)
        name = name.strip()
        expr = expr.strip()
        val = eval_expr(expr)
        variables[name] = val
        return state

    if line.startswith("ask "):
        # ask "Question" -> var
        m = re.match(r'ask\s+"(.*)"\s*->\s*([a-zA-Z_][a-zA-Z0-9_]*)', line)
        if not m:
            print(color("[error] invalid ask syntax", RED))
            return state
        question, name = m.groups()
        try:
            answer = input(color(question + " ", CYAN))
        except EOFError:
            answer = ""
        variables[name] = answer
        return state

    print(color(f"[error] unknown command: {line}", RED))
    return state


def run_shell():
    print(color("EasyLang Shell (type 'exit' to quit)", YELLOW))
    state = {}
    while True:
        try:
            line = input(color("easylang> ", CYAN))
        except (EOFError, KeyboardInterrupt):
            print()
            break
        if line.strip().lower() == "exit":
            break
        state = run_line(line, state)


def run_script(path):
    state = {}
    with open(path, "r", encoding="utf-8") as f:
        for line in f:
            state = run_line(line, state)


if __name__ == "__main__":
    if len(sys.argv) == 2:
        run_script(sys.argv[1])
    else:
        run_shell()

