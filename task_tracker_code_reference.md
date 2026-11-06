# Task Tracker — Code Reference
Updated: 2026-11-05 (through Lesson 11: terminal done, done-flag round trip)

This sheet is a field guide, not a textbook. Each entry is something you have already typed.

How to read a line of code:
1. What kind of thing is each word? (keyword, function, variable, string, tag…)
2. Who created that name — you, Python, Flask, or HTML?
3. Does this line *do* work now, or *define* work for later?

---

## Marking convention (yours vs required)

Going forward, examples use this labeling:

- **YOURS** — you picked the spelling. Another name would still run.
- **REQUIRED** — the language needs this exact word or symbol.
- **YOURS TEXT** — a string or visible phrase. Contents are your choice; the quotes or tags around it are required.
- **FIXED VOCAB** — not a keyword, but a specific allowed word (`"w"`, `"POST"`, `type="hidden"`). Changing it changes behavior or breaks.

Quick test: if you rename it and only *your other lines* need updating, it is YOURS. If Python/Flask/the browser error, it is REQUIRED or FIXED VOCAB.

### Python

| Piece | Category | Example |
|---|---|---|
| Keywords | REQUIRED | `def`, `for`, `in`, `if`, `with`, `try`, `return` |
| Function names you create | YOURS | `save_tasks`, `load_tasks`, `show_tasks` |
| Built-in / library functions | REQUIRED | `print`, `open`, `len`, `int`, `render_template` |
| Parameters and variables | YOURS | `tasks`, `task`, `task_list`, `FILENAME`, `file` |
| String contents | YOURS TEXT | `"tasks.txt"`, `"Buy coffee"`, `"Hello from a template file."` |
| File mode, HTTP method | FIXED VOCAB | `"w"`, `"r"`, `"GET"`, `"POST"` |
| Punctuation | REQUIRED | `=`, `==`, `:`, `()`, `[]`, `.` |

`FILENAME` is YOURS as a name. `"tasks.txt"` is YOURS TEXT as the filename. `open` and `"w"` are not yours.

### HTML

HTML is sneakier. **Tag names are not yours.** You may not invent `<header1>` or `<mybox>` and expect the browser to know what you mean.

| Piece | Category | Example |
|---|---|---|
| Tag name | REQUIRED | `h1`, `p`, `ul`, `li`, `form`, `input`, `a`, `body` |
| Attribute name (most) | REQUIRED or FIXED VOCAB | `href`, `type`, `action`, `method` |
| Attribute name `name` | REQUIRED word; its *value* is YOURS | `name="task"` — `name` stays; `task` is yours |
| Attribute values that pick a mode | FIXED VOCAB | `type="text"`, `type="hidden"`, `method="POST"` |
| Attribute values that are your data | YOURS TEXT | `href="/tasks"`, `action="/remove"`, `value="2"` |
| Text between tags | YOURS TEXT | `Your tasks`, `Add`, `Home` |

`name="task"`: the word `name` is the HTML rule. The word `task` is your handshake with `request.form.get("task")`. If you change it to `name="item"`, you must also change the Python to `request.form.get("item")`.

### Jinja

| Piece | Category | Example |
|---|---|---|
| Braces | REQUIRED | `{{ }}`, `{% %}` |
| Keywords | REQUIRED | `for`, `in`, `endfor`, `extends`, `block`, `endblock` |
| Variables | YOURS (must match Python) | `task`, `number`, `tasks` |
| Block names | YOURS (must match between base and child) | `title`, `content` |
| Template filenames | YOURS TEXT | `"base.html"` |

`{% for number, task in tasks %}`  
`for` / `in` = REQUIRED. `number`, `task`, `tasks` = YOURS, but `tasks` must be the same name you passed in `render_template(..., tasks=numbered)`.

---

## 0. The four languages in this project

| Language | Files | Job |
|---|---|---|
| Python | `main.py`, `app.py`, `file_practice.py` | Logic: lists, files, decisions |
| HTML | `templates/*.html` | Structure of the page |
| Jinja | pieces *inside* those HTML files | Fill the page with Python data |
| CSS | `static/style.css` | Look and layout |

Jinja is not HTML and not Python. It is a small language that *lives in HTML files* and is processed *before* the browser sees the page.

---

## 1. How to recognize a piece of Python

| If you see… | It is usually… | Example |
|---|---|---|
| word in lowercase, no quotes, Python reserved | **keyword** | `def`, `if`, `for`, `with`, `try`, `return` |
| `Name(` with parentheses | **function call** or **definition** | `print("Hi")`, `def save_tasks(tasks):` |
| `object.method(` | **method** — a function that belongs to an object | `file.write(...)`, `"  x".strip()` |
| `ALL_CAPS` or `snake_case` with no parentheses | **variable** (a name you chose) | `FILENAME`, `task_list` |
| text in `"..."` or `'...'` | **string** (literal text) | `"tasks.txt"`, `"w"` |
| `[...]` | **list** | `["Eat dinner", "Be happy!"]` |
| `(1, "Eat dinner")` | **tuple** (a pair) | from `enumerate` |
| `#` to end of line | **comment** (Python ignores it) | `# save after add` |
| indentation (spaces) | **block membership** | body of `if` / `def` / `for` |
| `:` at end of line | “a block starts next” | `def save_tasks(tasks):` |

You invent variable names and function names. You do **not** invent keywords (`if`, `def`, `with`).

---

## 2. The `save_tasks(tasks)` vs `save_tasks(task_list)` question

This is the most important distinction in the whole project so far.

### Definition vs call

```python
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        for task in tasks:
            file.write(task + "\n")
```

`def` **defines** a machine. It does not run the machine.

- `save_tasks` = the **name of the machine**
- `(tasks)` = a **parameter** = an empty loading dock with a label
- The indented body = what the machine does *once something is parked in that dock*

**Analogy:** A blender recipe card that says “blend `fruit`.”  
`fruit` is not a fruit in your kitchen. It is a *role*. When you actually blend, you pass `bananas` or `strawberries`. Inside the recipe they are still called `fruit`.

### Call

```python
task_list = load_tasks()
save_tasks(task_list)
```

- `save_tasks(task_list)` **runs** the machine
- `task_list` is the **argument** = the real box you hand over
- Python copies that list into the parameter name `tasks` *inside the function*
- For the duration of that call, inside the function, `tasks` *is* `task_list`

```text
outside:  task_list  ──handed to──►  inside: tasks
```

The names do **not** have to match. These are all legal:

```python
save_tasks(task_list)
save_tasks(sample)
save_tasks(["Buy coffee", "Email the team"])
```

Inside the function it is always `tasks`, because that is the dock label you wrote in `def`.

If you wrote `def save_tasks(items):`, then the loop would have to say `for task in items`.

### Why not use the same name everywhere?

You can:

```python
def save_tasks(task_list):
    for task in task_list:
        ...
```

That works. Many people do it. We used `tasks` inside the function because it is short and generic: “whatever list you handed me.” Outside we used `task_list` so it does not collide with the function named `tasks` you once had, and so “the list in this route” is easy to spot.

### `save_tasks()` with empty parentheses

That would call the function with **no** argument. Python would raise `TypeError: save_tasks() missing 1 required positional argument: 'tasks'`. The loading dock is required.

`load_tasks()` has empty parentheses on purpose: it needs no list. It only needs `FILENAME`, which it already can see.

---

## 3. Python keywords we have used

Keywords are built into Python. You cannot use them as variable names.

### `def`
Starts a function definition.  
Structure: `def name(parameter1, parameter2):` then an indented body.  
Does not run the body until you **call** `name(...)`.

### `return`
Hands a value back to the caller and exits the function.  
`return contents.splitlines()` means “stop this function; the answer is that list.”  
A function without `return` (like `save_tasks`) comes back as `None`. That is fine when the useful result is a side effect (writing a file).

### `if` / `elif` / `else`
A fork in the road.  
Structure:

```python
if condition:
    ...
elif other_condition:
    ...
else:
    ...
```

`condition` must be something True or False, such as `choice == "1"` or `task != ""`.

### `while`
Repeat a block until you `break` (or the condition becomes False).  
`while True:` means “until I say stop.”

### `for`
Walk a collection one item at a time.  
`for task in tasks:`  
- `tasks` is the collection  
- `task` is a new name for “the current item”  
You chose the name `task`. You could have written `for line in tasks`.

### `in`
Two jobs:  
1. In a `for` line: “walk this collection.”  
2. As a test: `if "coffee" in task_list:` (we have not needed this yet).

### `with`
A setup/cleanup block.  
`with open(...) as file:` opens the file, runs the block, then **closes** the file even if something fails.  
**Analogy:** a library checkout. `with` returns the book for you.

### `as`
Gives a temporary name to the thing `with` set up.  
`as file` means “call that open file `file` in this block.” You could write `as task_file`.

### `try` / `except`
Attempt risky code; if a *specific* error happens, run a backup.  
We catch `FileNotFoundError` and `ValueError` because we know those two can happen from missing files and bad `int(...)`.

### `break`
Leave the nearest loop immediately. Used in the terminal menu to Quit.

### `continue`
Skip the rest of this loop pass and start the next pass. Used after a bad number in Remove.

### `from` / `import`
Bring names in from another module.  
`from flask import Flask, request, redirect, render_template`  
means “from the Flask library, I need these four tools.”

---

## 4. Python functions and methods we have used

A **function** is called by name: `open(...)`, `print(...)`, `len(...)`.  
A **method** is called on an object: `file.write(...)`, `task.strip()`.

### Built-in functions

| Call | What it does |
|---|---|
| `print(x)` | Show `x` in the console |
| `input(prompt)` | Show prompt, wait for the user to type, return a string |
| `len(tasks)` | How many items in the list |
| `int("2")` | Turn that string into the integer `2` |
| `str(2)` | Turn that integer into the string `"2"` |
| `list(enumerate(...))` | Turn an enumerate recipe into a real list |
| `enumerate(tasks, start=1)` | Pair each item with a number starting at 1 |
| `open(FILENAME, "w")` | Open (or create) a file. `"w"` write, `"r"` read |
| `range(...)` | Not used yet. Makes a sequence of numbers |

### String methods

| Call | What it does |
|---|---|
| `"  hi  ".strip()` | Drop spaces at both ends → `"hi"` |
| `contents.splitlines()` | Cut a big string on newlines → list of lines |
| `task + "\n"` | Glue two strings. `+` on strings is concatenation |

### List methods

| Call | What it does |
|---|---|
| `tasks.append(task)` | Add one item at the end |
| `tasks.pop(index)` | Remove the item at that index and return it |

### File methods

| Call | What it does |
|---|---|
| `file.write(text)` | Write text into the open file. Does not add a newline unless you include `"\n"` |
| `file.read()` | Return the whole file as one string |

### Functions you wrote

| Call | Job | Needs | Gives back |
|---|---|---|---|
| `save_tasks(tasks)` | list → `tasks.txt` | a list | nothing useful (`None`) |
| `load_tasks()` | `tasks.txt` → list | nothing | a list |
| `home()` | Flask route for `/` | nothing | HTML (via template) |
| `show_tasks()` | Flask route for `/tasks` | uses `request` | redirect or HTML |
| `remove_task()` | Flask route for `/remove` | form field `number` | redirect |

### Flask tools

| Name | Kind | Job |
|---|---|---|
| `Flask` | class (blueprint) | `app = Flask(__name__)` builds your app object |
| `app` | object you created | the website |
| `@app.route("/tasks", methods=["GET", "POST"])` | decorator | Attach this function to that URL |
| `app.run(debug=True)` | method | Start the local server |
| `request` | object Flask fills in | The incoming browser request |
| `request.method` | string | `"GET"` or `"POST"` |
| `request.form.get("task", "")` | method | Read a posted field; use `""` if missing |
| `redirect("/tasks")` | function | Tell the browser to GET that URL next |
| `render_template("tasks.html", tasks=numbered)` | function | Fill a template and return HTML |

`@app.route` is a **decorator**. The `@` line marks the function *below* it. You do not call `home()` yourself. The browser does, by visiting `/`.

`Flask(__name__)` — `__name__` is a special Python variable meaning “this file’s name.” Flask uses it to know where `templates/` lives. Treat it as required boilerplate for now.

---

## 5. Python operators and punctuation

| Symbol | Meaning in our code |
|---|---|
| `=` | Assign. Put the right-hand value into the left-hand name |
| `==` | Compare. “Are these equal?” Used in `if` |
| `!=` | Compare. “Are these different?” `task != ""` |
| `<` `>` | Less / greater. `number < 1` |
| `+` on strings | Glue. `"<li>" + task` |
| `+` on numbers | Add. We have barely used this |
| `:` | “Block starts on the next indented lines” |
| `.` | “Reach inside this object for a method or field” |
| `()` | Call a function, or group, or define parameters |
| `[]` | List literal, or index a list later (`tasks[0]`) |
| `{}` | We have not used Python dicts much yet. In `f"{number}. {task}"` they mark placeholders |
| `,` | Separate items or arguments |
| `\` in `"\n"` | Escape. `\n` is a newline, not the letters n |

`=` vs `==` is a classic mix-up.  
`choice = "1"` *makes* choice become `"1"`.  
`choice == "1"` *asks* whether it already is.

---

## 6. HTML — tags we have used

HTML is nested boxes. A **tag** usually comes in a pair:

```html
<h1>Your tasks</h1>
```

- `<h1>` open (begin heading level 1)
- `Your tasks` content (what humans see)
- `</h1>` close (end heading)

The slash in `</h1>` means “stop this box.”

Some tags are empty (no content): `<input ...>` often has no close pair in our code. A button *does* wrap text: `<button>Add</button>`.

| Tag | Meaning |
|---|---|
| `<!DOCTYPE html>` | Declaration: treat this as modern HTML |
| `<html>` | The whole document |
| `<head>` | Invisible metadata (title, later CSS) |
| `<title>` | Browser tab text |
| `<body>` | Visible page |
| `<nav>` | Navigation region |
| `<h1>` | Top heading |
| `<p>` | Paragraph |
| `<ul>` | Unordered (bullet) list |
| `<li>` | One list item |
| `<a href="...">` | Link. `href` is the destination |
| `<form action="..." method="POST">` | Group of fields to submit |
| `<input type="text" name="task">` | Typing box. `name` is the key Flask reads |
| `<input type="hidden" name="number" value="1">` | Invisible field still submitted |
| `<button type="submit">` | Send the form |

### HTML attributes

Attributes live *inside* the opening tag:

```html
<a href="/tasks">Open your tasks</a>
<input type="text" name="task">
```

- `href`, `type`, `name`, `value`, `action`, `method` are **attribute names**
- `"/tasks"`, `"text"`, `"task"` are **attribute values**
- Values are usually in quotes

`name="task"` is how HTML talks to Python. Flask looks up that name in `request.form`.

---

## 7. Jinja — the bits inside `{% %}` and `{{ }}`

Jinja runs on the **server**, in Flask, *before* HTML is sent. The browser never sees `{% for %}`. It only sees the finished `<li>` tags.

| Syntax | Kind | Prints on the page? |
|---|---|---|
| `{{ task }}` | expression / output | Yes |
| `{% for number, task in tasks %}` | statement / instruction | No |
| `{% endfor %}` | end of for | No |
| `{% if ... %}` | statement (not used yet) | No |
| `{% block title %}` | named hole in a parent template | No |
| `{% endblock %}` | close that hole | No |
| `{% extends "base.html" %}` | “use that file as my frame” | No |

### `{{ task }}`
Print the variable `task`.  
Equivalent idea in Python: `print(task)` but the output goes into the HTML.

### `{% for number, task in tasks %}`
Same idea as Python:

```python
for number, task in tasks:
    ...
```

`tasks` here is whatever you passed in:

```python
render_template("tasks.html", tasks=numbered)
```

The left-hand name in Python (`tasks=`) **is** the name Jinja sees.

### Why two languages that both have `for`?

Python `for` runs when the route runs, building data.  
Jinja `for` runs when the page is filled, building markup.  
Same idea, different workshop.

---

## 8. Names *you* chose vs names you must keep

You chose: `FILENAME`, `task`, `task_list`, `save_tasks`, `show_tasks`, `home.html`.

You must keep: `def`, `if`, `with`, `print`, `open`, `Flask`, `request`, `render_template`, `<form>`, `{% block %}`, `"w"`, `"r"`.

Rule of thumb: if changing the spelling would still make sense in English (`task` → `item`), it is probably your name. If changing it would crash (`def` → `define`, `<h1>` → `<header1>`), it belongs to the language.

---

## 9. One line, fully labeled

```python
def save_tasks(tasks):
```

| Piece | Kind | Who owns it |
|---|---|---|
| `def` | keyword | Python |
| `save_tasks` | function name | you |
| `(` `)` | parameter list | Python syntax |
| `tasks` | parameter name | you |
| `:` | start of block | Python |

```python
save_tasks(task_list)
```

| Piece | Kind |
|---|---|
| `save_tasks` | function name being **called** |
| `task_list` | **argument** (real list) |

```html
{{ task }}
```

| Piece | Kind |
|---|---|
| `{{` `}}` | Jinja output markers |
| `task` | variable that came from the `for` loop |

```html
<input type="hidden" name="number" value="{{ number }}">
```

| Piece | Kind |
|---|---|
| `input` | HTML tag |
| `type` `name` `value` | HTML attributes |
| `"hidden"` `"number"` | literal attribute values |
| `{{ number }}` | Jinja: fill in the current task number |

---

## 10. Template inheritance (Lesson 5.4)

`base.html` = the frame. Child pages fill named holes.

| Piece | Label | Role |
|---|---|---|
| `{% extends "base.html" %}` | REQUIRED `extends`; YOURS TEXT filename | Child uses that frame. Must be first Jinja line |
| `{% block title %}` | REQUIRED `block`/`endblock`; YOURS name `title` | Hole for the browser tab |
| `{% block content %}` | REQUIRED words; YOURS name `content` | Hole for the page body |
| `<nav>` | REQUIRED tag | Navigation region |
| `Task Tracker` default inside title block | YOURS TEXT | Fallback if a child skips the title block |

Block names must match between base and child. If the base says `content` and the child says `body`, the hole stays empty.

## 11. CSS (Lesson 6)

CSS lives in `static/style.css` and is linked from `base.html`.

| Piece | Label | Role |
|---|---|---|
| `<link rel="stylesheet" href="...">` | REQUIRED tag; FIXED VOCAB `rel` | Attach the CSS file |
| `{{ url_for('static', filename='style.css') }}` | REQUIRED Flask helper; YOURS filename | Build the `/static/style.css` URL |
| `body { ... }` | REQUIRED selector (tag name) | Style every body |
| `.empty` | REQUIRED dot + YOURS class name | Style only elements with `class="empty"` |
| `font-family`, `margin`, `color`, `display`, `flex` | FIXED VOCAB | CSS property names |
| `Arial`, `#f4f1ea`, `1rem`, `flex` | YOURS values | What it should look like |
| `li span { flex: 1; }` | YOURS selector | Let the text stretch so buttons stay aligned on the right |

`class` is an HTML attribute (REQUIRED name, YOURS value). The matching CSS starts with a dot.

## 12. Shared storage module (Lesson 7)

`storage.py` holds the file logic. `main.py` and `app.py` both import it.

| Piece | Label | Role |
|---|---|---|
| `from storage import load_tasks, save_tasks` | REQUIRED `from`/`import`; YOURS module and function names | Bring the shared tools into this file |
| `FILENAME = "tasks.txt"` | YOURS name; YOURS TEXT | Defined once in `storage.py` |

Change the save/load logic in one place; both the terminal and the website pick it up.

## 13. Mark done (Lesson 8)

Each task is now a dictionary: `{"done": False, "text": "Buy coffee"}`.

| Piece | Label | Role |
|---|---|---|
| `{"done": ..., "text": ...}` | REQUIRED braces; YOURS keys | One task with two named pieces |
| `task["done"]` / `task.text` | YOURS key | Look up the flag (Python vs Jinja) |
| `"1" if task["done"] else "0"` | REQUIRED `if`/`else`; FIXED VOCAB `"1"`/`"0"` | Write the flag to the file |
| `line.split("|", 1)` | REQUIRED method; FIXED VOCAB `"|"` | Split on the first pipe |
| `task["done"] = not task["done"]` | YOURS key; REQUIRED `not` | Flip True ↔ False |
| `@app.route("/done", methods=["POST"])` | REQUIRED decorator; YOURS path | New route that toggles done |
| `.done { text-decoration: line-through; }` | YOURS class; FIXED VOCAB property | Strikethrough for finished tasks |

Old plain lines (no pipe) still load as not-done.

## 13b. Done flag round trip

The file never contains the word `done`. It stores `0` or `1`. Python names that yes/no `"done"`.

```text
tasks.txt          0|Email team
                   1|Celebrate

load_tasks()       {"done": False, "text": "Email team"}
                   {"done": True,  "text": "Celebrate"}

menu / website     task["done"]  →  [ ] or [x]  /  Done or Undo

save_tasks()       0|Email team
                   1|Celebrate
```

| Step | Code | What happens |
|---|---|---|
| Load | `done_flag == "1"` | `"1"` becomes `True`, `"0"` becomes `False`, stored as `task["done"]` |
| Use | `task["done"]` | Menu prints `[x]` or `[ ]`; website shows Done/Undo and strikethrough |
| Toggle | `task["done"] = not task["done"]` | Flip True ↔ False |
| Save | `"1" if task["done"] else "0"` | Write `1|text` or `0|text` back to the file |

`"done"` is a key you chose. The file only has `0` and `1`. Once you pick the key, every `task["done"]` must use that spelling.

## 13c. Brackets

| Shape | Name | Job in Python |
|---|---|---|
| `()` | parentheses | Call a function, group, or define parameters |
| `[]` | square brackets | List, or look up by position / key |
| `{}` | curly braces | Dictionary |

```python
load_tasks()                   # call
tasks[number - 1]              # list lookup (0-based)
task["done"]                   # dict lookup by key
{"done": False, "text": line}  # dict literal
```

Jinja `{{ }}` and `{% %}`, and CSS `{ }`, are different languages using similar characters.

## 14. Git (Lesson 9)

Git saves versions of the project locally. `git push` sends those versions to GitHub.

| Command | Role |
|---|---|
| `git init` | Create a hidden `.git` folder (local history) |
| `git add .` or `git add path` | Stage files for the next commit |
| `git status` | Show staged, unstaged, and untracked files |
| `git diff` | Show unstaged changes (red/green lines) |
| `git commit -m "message"` | Save a local snapshot with a caption |
| `git log --oneline` | Compact list of commits |
| `git show` | Show a commit and its diff (press `q` to quit the pager) |
| `git show HEAD~1:path` | See a file as it was one commit ago |
| `git remote add origin URL` | Name the GitHub address `origin` |
| `git push -u origin main` | Upload unpushed commits and remember the link |

**Commit vs push:**  
`commit` = photo in your local drawer.  
`push` = send every local photo that GitHub does not already have.

`.gitignore` skips `.venv/`, `__pycache__/`, and `.idea/`.

## 15. Edit a task (Lesson 10)

A form posts the task number and the new text to `/edit`. The route updates only `["text"]` and saves.

| Piece | Label | Role |
|---|---|---|
| `name="text"` on the input | YOURS | Key the form sends |
| `request.form.get("text")` | YOURS (must match the HTML `name`) | Read that field |
| `raw = request.form.get("number", "")` | YOURS variable | Unprocessed number string |
| `task_list[number - 1]["text"] = new_text` | YOURS keys | Replace wording; leave `done` alone |

**Form names vs Python variables:**  
The `name="..."` in HTML is the envelope label. `request.form.get("...")` must use the same spelling. The variable you store it in (`raw`, `new_text`) is only for you — it does not have to match.

## 16. FAQ

**Why is it `request.form.get("number")` and not just the variable?**  
Because the browser sends fields by the `name` attribute. Python looks up that key. The variable (`raw`) is only where you park the result.

**Why `number - 1`?**  
Humans count from 1. Python lists count from 0. Task 2 is index 1.

**Why redirect after POST?**  
So a refresh does not submit the form again (duplicate add, edit, or delete).

**Why `from storage import ...`?**  
So `main.py` and `app.py` share one definition of save/load. Change it once.

**Commit vs push?**  
Commit = local snapshot. Push = send unpushed commits to GitHub.

**Why press `q` in `git show`?**  
Git opened a pager. `q` quits it and returns to the terminal.

## 17. Glossary by language

### Python
| Term | Meaning |
|---|---|
| keyword | Reserved word (`def`, `if`, `for`, `with`, `return`) |
| function | Named block you define with `def` and call with `()` |
| parameter | Name in the `def` parentheses (the slot) |
| argument | Value you pass when you call the function |
| variable | Name you assign a value to |
| method | Function that belongs to an object (`file.write`, `str.strip`) |
| list | Ordered collection `[...]`, 0-based |
| dictionary | Labeled collection `{"done": False, "text": "..."}` |
| module | A `.py` file you can import |
| exception | Error you can catch with `try` / `except` |

### HTML
| Term | Meaning |
|---|---|
| tag | Element name in angle brackets (`<h1>`, `<form>`) |
| attribute | Name/value inside a tag (`name="text"`, `href="/tasks"`) |
| form | Group of fields submitted together |
| `name` | Attribute that becomes the key in `request.form` |

### Jinja
| Term | Meaning |
|---|---|
| `{{ }}` | Print a value |
| `{% %}` | Instruction (`for`, `if`, `block`, `extends`) |
| `extends` | Use another template as the frame |
| `block` | Named hole the child fills |

### CSS
| Term | Meaning |
|---|---|
| selector | Who to style (`body`, `.empty`, `li span`) |
| property | What to change (`color`, `display`, `flex`) |
| class | HTML attribute; CSS selects it with a leading dot |

### Flask
| Term | Meaning |
|---|---|
| route | URL path attached to a function (`@app.route`) |
| `request` | The incoming browser request |
| `request.form` | Posted form fields, looked up by `name` |
| `redirect` | Tell the browser to GET another URL |
| `render_template` | Fill an HTML file and return it |

### Git
| Term | Meaning |
|---|---|
| commit | Local snapshot with a message |
| stage (`git add`) | Mark files for the next commit |
| push | Upload commits the remote does not have |
| `HEAD` | Current commit |
| origin | Default name for the GitHub remote |
| pager | Viewer `git show` opens; quit with `q` |

## 18. What we will add later

- Terminal edit
- Deploy the site
- More Git (branches, pull)

Last updated after: terminal done toggle, done-flag round trip, brackets (Lesson 11).
