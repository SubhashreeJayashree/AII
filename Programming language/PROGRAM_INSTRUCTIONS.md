# Novi One IDE v2 - User Friendly Guide

This app is built as a new, easy, and efficient Novi language workspace.
You can build web, IoT, cloud, ML, system logic, and ask AI coding questions in one place.

## 1) Start the app correctly

Always use:

`http://localhost:5500/index.html`

Do not use `file://...`.

## 2) Quick start in 30 seconds

1. Open the app URL.
2. Type Novi code in the editor.
3. Click `Run`.
4. Read results in **Program Output**.
5. Use `Ask AI` for explanation or fixes.

## 3) Easy Novi language rules

- Program entry: `core main { ... }`
- Variable assign: `name := value`
- Condition: `when condition { ... }`
- Print/display: `show "text"`
- AI support: `note := ask "your question"`
- AI correction: click `Ask AI` to auto-correct common typing mistakes

## 3.1) Universal typing support (easy for all users)

Novi keeps a unique syntax, but it accepts common typing styles from other languages and auto-corrects them:

- `a = 1` -> auto-converts to `a := 1`
- `if (a = 1) print(hello)` -> auto-converts to:

```txt
when a = 1 {
  show "hello"
}
```

- `print("hello")` -> auto-converts to `show "hello"`

This makes it easy for users from Python, JavaScript, .NET/C#, Java, SQL, and other backgrounds.

Simple program:

```txt
core main {
  temp := 82
  when temp > 80 {
    note := ask "suggest immediate cooling action"
    show note.text
  }
  show "done"
}
```

## 4) Full button instructions (all clickable)

Top buttons:

- `Run` -> executes current editor code and updates **Program Output**.
- `Ask AI` -> explains current code and gives learning hints.
- `Ask AI` -> also auto-corrects common syntax mistakes in editor text.
- `Generate` -> inserts a Novi starter code block.
- `Fix` -> applies safe conversion style in current code.
- `Help` -> opens this instructions file.
- `Switch Theme` -> toggles light/dark colorful theme.

Module buttons:

- `+ Web` -> adds Novi web module snippet.
- `+ IoT` -> adds Novi IoT stream snippet.
- `+ Cloud` -> adds Novi cloud bridge snippet.
- `+ ML` -> adds Novi ML inference snippet.
- `+ System` -> adds Novi system health snippet.

AI panel button:

- `Send Query` -> sends your typed question and shows AI answer.
- Special case: if you ask for `hello world` and `a+b` with `a=1 b=4`, it auto-generates that program in the editor.
- You can ask broad tech questions (example: `.NET`, `Node.js`, `RDBMS`, `SQL`, architecture, debugging).

Quick chips under editor (also clickable):

- `Explain` -> same as `Ask AI`.
- `Fix` -> same as top `Fix`.
- `Generate` -> same as top `Generate`.
- `Reduce latency` -> shows performance optimization tips.

## 5) How to write your own task

1. Clear old code from editor.
2. Start with `core main {`.
3. Add variables with `:=`.
4. Add `when` blocks for decisions.
5. Add `show` lines for output.
6. Click `Run`.

Starter template:

```txt
core main {
  device := "pump-1"
  status := "online"
  show "device: " + device
  show "status: " + status
}
```

## 6) Your requested example (Hello World + add)

Type this directly:

```txt
core main {
  a := 1
  b := 4
  show "hello world"
  show a + b
}
```

Then click `Run`.

Expected **Program Output**:

```txt
hello world
5
```

Alternative method:

1. In AI input box, type: `write a program for hello world and add a+b a=1 b=4`
2. Click `Send Query`
3. Click `Run`

## 7) If a button does not work

- Confirm URL is `http://localhost:5500/index.html`
- Press `Ctrl + F5` to refresh
- Re-open the app from localhost
- Do not run from `file://...`

## 8) Practice AI queries

- `optimize this loop for low latency`
- `add error handling for sensor data`
- `generate iot + cloud integration in novi`
- `best .NET API structure`
- `node.js async error handling`
- `rdbms indexing strategy for fast queries`

