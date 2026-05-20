# SimpleLang - Complete Features List

## 🎯 Easy but Powerful!

SimpleLang is designed to be as easy as possible but with powerful features like other programming languages.

---

## 📦 All Features

### 1. **Basic Commands**
- `say` - Display text, numbers, or variables
- `make` - Create variables (auto-saved!)
- `ask` - Get user input

### 2. **Arrays** (Like Lists)
- `array name [item1, item2]` - Create array
- `add name value` - Add item to array
- `get name index varname` - Get item from array
- `name[index]` - Access array element

### 3. **Loops** (Repeat Code)
- `loop condition ... endloop` - Repeat while condition is true
- Example: `loop i < 10 ... endloop`

### 4. **Conditionals** (If/Else)
- `if condition ... endif` - Execute if condition is true
- `else` - Alternative path
- Example: `if score > 80 ... else ... endif`

### 5. **Functions** (Reusable Code)
- `func name() ... endfunc` - Define function
- `name()` - Call function

### 6. **Data Storage** ⭐ NEW!
- `store key "value"` - Store data permanently
- `view` - View stored data
- `viewall` - View all variables, arrays, functions
- **Auto-save**: All variables and arrays are automatically saved!

---

## 💾 Data Storage Features

### Automatic Storage
- All variables are automatically saved
- All arrays are automatically saved
- All functions are automatically saved
- Data persists even after closing browser!

### Permanent Storage
- Use `store key "value"` for permanent storage
- Use `view` to see stored data
- Data survives browser restarts

### View Data
- Click **"View Data"** button to see everything
- Or type `viewall` in shell
- See all variables, arrays, functions, and stored data

---

## 📝 Examples

### Variables & Math
```simplelang
make x 10
make y 20
make total x + y
say total
```

### Arrays
```simplelang
array fruits ["apple", "banana", "orange"]
say fruits[0]
add fruits "grape"
say "Added grape!"
```

### Loops
```simplelang
make i 1
loop i <= 5
    say i
    make i i + 1
endloop
```

### Conditionals
```simplelang
make score 85
if score >= 80
    say "Great!"
else
    say "Try harder!"
endif
```

### Functions
```simplelang
func greet()
    say "Hello!"
    say "Welcome!"
endfunc

greet()
```

### Data Storage
```simplelang
make name "John"
make age 25
store username name
store userage age
view
```

---

## 🎨 UI Features

- **Multicolor Shell** - Beautiful colored output
- **AI Assistant** - Get help with coding
- **View Data Button** - See all stored data
- **Auto-Save** - Everything saves automatically
- **Code Editor** - Write and run code
- **Interactive Shell** - Type commands directly

---

## 🔄 Comparison with Other Languages

| Feature | SimpleLang | Python | JavaScript |
|---------|-----------|--------|------------|
| Syntax | Very Simple | Simple | Medium |
| Variables | `make x 10` | `x = 10` | `let x = 10` |
| Arrays | `array x [1,2]` | `x = [1,2]` | `let x = [1,2]` |
| Loops | `loop i < 10` | `while i < 10` | `while(i < 10)` |
| Functions | `func name()` | `def name()` | `function name()` |
| Data Storage | Built-in! | Need files | Need localStorage |
| Auto-Save | ✅ Yes | ❌ No | ❌ No |

---

## 🚀 Why SimpleLang?

1. **Easy to Learn** - Simple syntax, no complex rules
2. **Powerful** - Arrays, loops, functions, storage
3. **Auto-Save** - Never lose your data
4. **View Data** - See everything you've stored
5. **Like Real Languages** - But much easier!

---

**SimpleLang** - Easy but Powerful! 🌟
