import os

FILENAME = os.environ.get("TASKS_FILE", "tasks.txt")
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        for task in tasks:
            done = "1" if task["done"] else "0"
            due = task.get("due", "")
            file.write(done + "|" + due + "|" + task["text"] + "\n")

def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return []

    tasks = []
    for line in contents.splitlines():
        parts = line.split("|", 2)
        if len(parts) ==3:
            done_flag, due, text = parts
            tasks.append({
                "done": done_flag == "1",
                "due": due,
                "text": text
            })
        elif len(parts) ==2:
            done_flag, text = parts
            tasks.append({
                "done": done_flag == "1",
                "due": "",
                "text": text,
            })

        else:
            tasks.append({"done": False, "due": "", "text": line})
    return tasks
