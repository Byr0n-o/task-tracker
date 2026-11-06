from flask import Flask, request, redirect, render_template
from storage import load_tasks, save_tasks
app = Flask(__name__)

@app.route("/")
def home():
    return render_template("home.html")
@app.route("/tasks", methods=["GET", "POST"])
def show_tasks():
    if request.method == "POST":
        task = request.form.get("task", "").strip()
        if task != "":
            task_list = load_tasks()
            task_list.append(task)
            save_tasks(task_list)
        return redirect("/tasks")

    task_list = load_tasks()
    numbered = list(enumerate(task_list, start=1))
    return render_template("tasks.html", tasks=numbered)

@app.route("/remove", methods=["POST"])
def remove_task():
    raw = request.form.get("number", "").strip()
    try:
        number = int(raw)
    except ValueError:
        return redirect("/tasks")

    task_list = load_tasks()

    if number < 1 or number > len(task_list):
        return redirect("/tasks")

    task_list.pop(number - 1)
    save_tasks(task_list)
    return redirect("/tasks")

@app.route("/done", methods=["POST"])
def mark_done():
    raw = request.form.get("number", "").strip()
    try:
        number = int(raw)
    except ValueError:
        return redirect("/tasks")

    task_list = load_tasks()

    if number < 1 or number > len(task_list):
        return redirect("/tasks")

    task = task_list[number-1]
    task["done"] = not task["done"]
    save_tasks(task_list)
    return redirect("/tasks")

@app.route("/edit", methods=["POST"])
def edit_task():
    raw = request.form.get("number", "").strip()
    new_text = request.form.get("text", "").strip()

    try:
        number = int(raw)
    except ValueError:
        return redirect("/tasks")

    if new_text == "":
        return redirect("/tasks")

    task_list = load_tasks()

    if number < 1 or number > len(task_list):
        return redirect("/tasks")

    task_list[number -1]["text"] = new_text
    save_tasks(task_list)
    return redirect("/tasks")

if __name__ == "__main__":
    app.run(debug=True)

