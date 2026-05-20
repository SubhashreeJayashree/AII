# HOW IT WORKS - New Language Guide

## 1. Introduction
This language is designed to be simple, beginner‑friendly, and AI‑assisted.
It supports both voice input and a text box, so you can either speak or type your commands and questions.
Programs run inside a lightweight interpreter, and results are printed directly to the Program Output panel.

## 2. Philosophy
- **Easy syntax:** minimal keywords, human‑readable style.
- **AI assistance:** ask questions inline with `ask`.
- **Universal modules:** Web, IoT, Cloud, ML, System APIs.
- **Output clarity:** every `show` statement prints evaluated results.
- **Accessibility:** both voice and text inputs are supported.

## 3. Syntax Rules
- **Program entry:**
```text
core main { ... }
```
- **Variable assignment:**
```text
x := 10
```
- **Condition:**
```text
if x > 5 { show "big" } else { show "small" }
```
- **Output:**
```text
show "hello world"
```
- **AI query:**
```text
note := ask "your question"
show note.text
```
- **Loop:**
```text
repeat 3 { show "hi" }
```
- **Function:**
```text
func add(a,b) { show a+b }
```

## 4. Execution Model
1. **Lexer** → breaks code into tokens.
2. **Parser** → checks grammar and builds a tree.
3. **Executor** → runs statements in order.
4. **Output Handler** → evaluates and prints results from `show`.
5. **AI Engine** → processes `ask` queries and returns text.
6. **Voice/Text Input Layer** → converts spoken or typed commands into code or queries.

## 5. Voice Input & Text Box
**Voice Input:**
- Speak commands like: “Write a hello world program”.
- The IDE converts speech into Novi code automatically.
- Example: Saying “add a and b where a=1 b=4” → generates:
```text
core main {
  a := 1
  b := 4
  show a + b
}
```

**Text Box:**
- Type code or questions directly.
- Example: Typing `write a program for hello world` → generates starter code.

Both inputs connect to the same AI engine, so whether you speak or type, the system responds consistently.

## 6. Example Programs

**Hello World + Addition**
```text
core main {
  a := 1
  b := 4
  show "hello world"
  show a + b
}
```
*Expected Output*
```text
hello world
5
```

**IoT Example with AI**
```text
core main {
  temp := 95
  note := ask "suggest cooling action"
  show note.text
}
```
*Expected Output*
```text
AI: Suggested action: cooling fan level 2
```

## 7. Modules
- **Web** → build UI snippets.
- **IoT** → connect sensors and devices.
- **Cloud** → bridge APIs and services.
- **ML** → run inference models.
- **System** → monitor health and performance.
