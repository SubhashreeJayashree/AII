# Novi / OrionLang Demo Script

This script walks through a live demonstration of how the language integrates voice and text inputs with real-time AI and dynamic output.

## Setup
1. Launch the IDE by opening `http://localhost:5500/index.html`.
2. Ensure you have microphone permissions enabled for voice input.

## Scene 1: Basic Voice Input Command
**User Action:** Clicks the "Voice Input" button.
**User Speaks:** "Write a hello world program."

**IDE Behavior:** 
1. The speech-to-text layer captures the input.
2. The code editor automatically populates with:
```text
core main {
  show "hello world"
}
```
**User Action:** Clicks `Run`.
**Expected Result:** (Program Output)
```text
hello world
```
*Note for audience: This demonstrates the ultra-simple syntax and instant voice-to-code generation.*

## Scene 2: Text Input with AI Problem Solving
**User Action:** In the "Ask in natural language" box, the user types:
> *optimize a loop that counts from 1 to 5 and tells if number is even or odd*

**User Action:** Clicks `Send Query`.
**IDE Behavior:** 
The AI generates the exact loop in Novi syntax in the editor:
```text
core main {
  repeat 5 {
    x := counter
    if x % 2 = 0 {
      show "even: " + x
    } else {
      show "odd: " + x
    }
  }
}
```
**User Action:** Clicks `Run`.
**Expected Result:** (Program Output)
```text
odd: 1
even: 2
odd: 3
even: 4
odd: 5
```
*Note for audience: This highlights the compiler's successful `if/else` execution and evaluated `+` concatenations.*

## Scene 3: Inline AI Queries
**User Action:** The user types the following code manually in the editor:
```text
core main {
  temp := 95
  if temp > 90 {
    note := ask "temperature is 95, suggest emergency cooling action"
    show note.text
  } else {
    show "systems stable"
  }
}
```
**User Action:** Clicks `Run`.
**Expected Result:** (Program Output)
```text
AI: Suggested action: Activate emergency cooling fan level 3 immediately.
```
*Note for audience: This demonstrates the `ask` keyword seamlessly connecting the execution model to an AI Engine on the fly.*

## Scene 4: Code Auto-Correction
**User Action:** The user purposefully types 'C-style' code into the editor:
```text
if (a = 1) {
   print("hello")
}
```
**User Action:** Clicks `Fix` or `Run`.
**IDE Behavior:** 
The text is immediately auto-converted into Novi syntax before running:
```text
when a = 1 {
  show "hello"
}
```
**Expected Result:** The code evaluates perfectly and prints "hello".
*Note for audience: Emphasizes the beginner-friendliness and automatic syntax correction to reduce developer frustration.*
