import os

FILENAME = os.environ.get("TASKS_FILE", "tasks.txt")
def save_tasks(tasks):
    with open(FILENAME, "w") as file:
        for task in tasks:
            done = "1" if task["done"] else "0"
            file.write(done + "|" + task["text"] + "\n")

def load_tasks():
    try:
        with open(FILENAME, "r") as file:
            contents = file.read()
    except FileNotFoundError:
        return []

    tasks = []
    for line in contents.splitlines():
        if "|" in line:
            done_flag, text = line.split("|", 1)
            tasks.append({"done": done_flag == "1", "text": text})
        else:
            tasks.append({"done": False, "text": line})
    return tasks
