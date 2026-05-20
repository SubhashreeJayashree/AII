# FlowLang - Complete Beginner's Guide

## Welcome to FlowLang! 🌟

FlowLang is **your own programming language** - designed to be the easiest programming language in the world! Whether you're a complete beginner or an experienced programmer, FlowLang makes coding simple and fun.

---

## Table of Contents

1. [Getting Started](#getting-started)
2. [Basic Commands](#basic-commands)
3. [Variables](#variables)
4. [Conditional Statements](#conditional-statements)
5. [Loops](#loops)
6. [Input and Output](#input-and-output)
7. [Examples](#examples)
8. [Tips and Tricks](#tips-and-tricks)
9. [AI Assistant Features](#ai-assistant-features)

---

## Getting Started

### What is FlowLang?

FlowLang is a simple, easy-to-learn programming language that:
- ✅ No complex syntax
- ✅ No semicolons or braces needed
- ✅ No type declarations
- ✅ Natural, readable commands
- ✅ Built-in AI assistant to help you

### How to Use FlowLang

1. Open the FlowLang application in your web browser
2. Type code in the **Code Editor** on the left
3. Click **Run** to execute your code
4. See results in the **FlowLang Shell** on the right
5. Or type commands directly in the shell!

---

## Basic Commands

### 1. SHOW - Display Text or Values

The `show` command displays text or values on the screen.

**Syntax:**
```
show "text"
show number
show variable
```

**Examples:**
```
show "Hello World"
show 42
show "The answer is " + 42
```

**Output:**
```
Hello World
42
The answer is 42
```

---

### 2. LET - Create Variables

The `let` command creates variables to store values.

**Syntax:**
```
let variable_name = value
```

**Examples:**
```
let name = "Alice"
let age = 25
let price = 19.99
let total = 10 + 20
```

**Important Notes:**
- Variable names can contain letters, numbers, and underscores
- Variable names must start with a letter or underscore
- No need to declare types - FlowLang figures it out!

---

### 3. ASK - Get User Input

The `ask` command gets input from the user.

**Syntax:**
```
ask "Question?" -> variable_name
```

**Examples:**
```
ask "What is your name?" -> name
show "Hello, " + name

ask "How old are you?" -> age
show "You are " + age + " years old"
```

---

## Variables

### Using Variables

Once you create a variable with `let`, you can use it anywhere:

```
let x = 10
let y = 20
show x + y        # Output: 30
show x * y        # Output: 200
```

### String Concatenation

Combine text using the `+` operator:

```
let firstName = "John"
let lastName = "Doe"
show firstName + " " + lastName    # Output: John Doe
```

### Math Operations

FlowLang supports all basic math operations:

```
let a = 10
let b = 5

show a + b    # Addition: 15
show a - b    # Subtraction: 5
show a * b    # Multiplication: 50
show a / b    # Division: 2
```

---

## Conditional Statements

### IF/ELSE Statements

Make decisions in your code with `if` and `else`.

**Syntax:**
```
if condition
    # code to run if true
else
    # code to run if false
end
```

**Examples:**
```
let age = 20

if age >= 18
    show "You are an adult"
else
    show "You are a minor"
end
```

**Comparison Operators:**
- `>` - Greater than
- `<` - Less than
- `>=` - Greater than or equal
- `<=` - Less than or equal
- `==` - Equal to (Note: Use single `=` for assignment)

**Example with Multiple Conditions:**
```
let score = 85

if score >= 90
    show "Grade: A"
else
    if score >= 80
        show "Grade: B"
    else
        show "Grade: C or below"
    end
end
```

---

## Loops

### WHILE Loops

Repeat code while a condition is true.

**Syntax:**
```
while condition
    # code to repeat
end
```

**Examples:**
```
# Count from 1 to 5
let i = 1
while i <= 5
    show i
    let i = i + 1
end
```

**Output:**
```
1
2
3
4
5
```

**Important:** Always make sure your loop condition will eventually become false, or you'll create an infinite loop!

---

## Input and Output

### Complete Input/Output Example

```
ask "What is your name?" -> name
ask "How old are you?" -> age

show "Hello, " + name
show "You are " + age + " years old"

if age >= 18
    show "You can vote!"
else
    show "You cannot vote yet"
end
```

---

## Examples

### Example 1: Simple Calculator

```
let a = 10
let b = 5

show "First number: " + a
show "Second number: " + b
show "Sum: " + (a + b)
show "Difference: " + (a - b)
show "Product: " + (a * b)
show "Quotient: " + (a / b)
```

### Example 2: Greeting Program

```
ask "What is your name?" -> name
ask "What is your favorite color?" -> color

show "Hello, " + name + "!"
show "Your favorite color is " + color
show "That's a great color!"
```

### Example 3: Number Counter

```
let count = 1
while count <= 10
    show "Count: " + count
    let count = count + 1
end
show "Counting complete!"
```

### Example 4: Age Checker

```
ask "How old are you?" -> age

if age >= 18
    show "You are an adult"
    show "You can drive and vote"
else
    show "You are a minor"
    show "You need to wait " + (18 - age) + " more years"
end
```

### Example 5: Simple Quiz

```
let score = 0

ask "What is 2 + 2?" -> answer1
if answer1 == "4"
    show "Correct!"
    let score = score + 1
else
    show "Wrong! The answer is 4"
end

ask "What is the capital of France?" -> answer2
if answer2 == "Paris"
    show "Correct!"
    let score = score + 1
else
    show "Wrong! The answer is Paris"
end

show "Your score: " + score + " out of 2"
```

---

## Tips and Tricks

### 1. Comments

Use `#` to add comments to your code:

```
# This is a comment
show "Hello"  # This is also a comment
```

### 2. String vs Numbers

- Use quotes for text: `"Hello"`
- No quotes for numbers: `42`
- Combine with `+`: `"The answer is " + 42`

### 3. Variable Naming

- Use descriptive names: `userName` instead of `x`
- Use camelCase: `firstName`, `lastName`
- Or use underscores: `first_name`, `last_name`

### 4. Indentation

While FlowLang doesn't require indentation, it makes your code more readable:

```
if age >= 18
    show "Adult"
    show "You can vote"
else
    show "Minor"
    show "Wait a bit more"
end
```

### 5. Testing Your Code

- Start with simple examples
- Test each part separately
- Use `show` to debug and see what values your variables have

---

## AI Assistant Features

FlowLang comes with a built-in AI assistant! Turn on **AI Mode** to get help with:

### 1. Spelling Correction

The AI can fix spelling mistakes in your code:
- `shwo` → `show`
- `lt` → `let`
- `aks` → `ask`

**How to use:** Ask the AI: "Fix spelling mistakes" or "Correct my spelling"

### 2. Code Correction

The AI can find and fix errors in your code:
- Missing quotes
- Wrong syntax
- Logic errors

**How to use:** Ask the AI: "Fix my code" or "There's an error"

### 3. Build Features

The AI can create programs for you:
- Calculators
- Counters
- Greeting programs
- And more!

**How to use:** Ask the AI: "Build a calculator" or "Create a counter program"

### 4. Get Help

Ask the AI questions about FlowLang:
- "How do I use loops?"
- "What is the syntax for variables?"
- "Help me with conditionals"

---

## Common Mistakes to Avoid

1. **Forgetting quotes for text:**
   - ❌ `show Hello`
   - ✅ `show "Hello"`

2. **Using wrong comparison operator:**
   - ❌ `if age = 18` (this assigns, not compares)
   - ✅ `if age >= 18`

3. **Infinite loops:**
   - ❌ `while 1` (never ends!)
   - ✅ `while count < 10` (has an end condition)

4. **Missing `end` for blocks:**
   - ❌ `if age >= 18 show "Adult"`
   - ✅ `if age >= 18 show "Adult" end`

---

## Practice Exercises

### Exercise 1: Hello World
Write a program that displays "Hello, World!"

### Exercise 2: Personal Greeting
Ask for the user's name and greet them personally.

### Exercise 3: Simple Math
Create two variables with numbers and display their sum, difference, product, and quotient.

### Exercise 4: Age Checker
Ask for age and tell if the person is an adult or minor.

### Exercise 5: Countdown
Create a countdown from 10 to 1.

### Exercise 6: Number Guessing
Create a simple number guessing game (hint: use if/else).

---

## Next Steps

Now that you know the basics of FlowLang:

1. **Practice** - Write your own programs
2. **Experiment** - Try different combinations
3. **Use AI Assistant** - Get help when stuck
4. **Build Projects** - Create something useful
5. **Share** - Show your programs to others!

---

## Quick Reference

| Command | Syntax | Example |
|---------|--------|---------|
| Show | `show "text"` | `show "Hello"` |
| Variable | `let name = value` | `let x = 10` |
| Input | `ask "Q?" -> var` | `ask "Name?" -> name` |
| If | `if condition ... end` | `if x > 5 show "Big" end` |
| While | `while condition ... end` | `while i < 10 ... end` |
| Comment | `# text` | `# This is a comment` |

---

## Conclusion

Congratulations! You've learned FlowLang - your own programming language! 🎉

Remember:
- **Practice makes perfect** - Keep coding!
- **Use the AI Assistant** - It's there to help!
- **Have fun** - Programming should be enjoyable!

Happy coding with FlowLang! 🌟

---

*FlowLang - The Easiest Programming Language in the World*
