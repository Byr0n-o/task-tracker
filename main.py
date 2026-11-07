from storage import load_tasks, save_tasks

print("Welcome to the Task Tracker")

tasks = load_tasks()

while True:
    print()
    print("1. Add a task")
    print("2. View tasks")
    print("3. Quit")
    print("4. Remove a task")
    print("5. Mark done / undo")
    print("6. Edit a task")


    choice = input("Choose 1, 2, 3, or 4: ").strip()

    if choice == "1":
        task = input("What do you need to do? ").strip()
        if task == "":
            print("Empty task ignored.")
        else:
            tasks.append(task)
            print("Added:", task)
            save_tasks(tasks)

    elif choice == "2":
        if len(tasks) == 0:
            print("No tasks yet.")
        else:
            print("Your Tasks:")
            for number, task in enumerate(tasks, start=1):
                mark = "x" if task["done"] else " "
                print(f" {number}. [{mark}] {task['text']}")

    elif choice == "3":
        print("Goodbye.")
        break

    elif choice == "4":
        if len(tasks) == 0:
            print("No tasks to remove.")
        else:
            print("Your Tasks:")
            for number, task in enumerate(tasks, start=1):
                print(f" {number}. {task}")

            raw = input("Which task do you want to remove? ").strip()
            try:
                number = int(raw)
            except ValueError:
                print("Please type a number.")
                continue
            if number < 1 or number > len(tasks):
                print("That number is not on the list.")
            else:
                removed = tasks.pop(number - 1)
                print("Removed:", removed)
                save_tasks(tasks)

    elif choice == "5":
        if len(tasks) == 0:
            print("No tasks to update.")
        else:
            print("Your Tasks:")
            for number, task in enumerate(tasks, start=1):
                mark = "x" if task["done"] else " "
                print(f" {number}. [{mark}] {task['text']}")
            raw = input("Which number do you want to update? ").strip()
            try:
                number = int(raw)
            except ValueError:
                print("Please type a number.")
                continue
            if number < 1 or number > len(tasks):
                print("That number is not on the list.")
            else:
                tasks[number -1]["done"] = not tasks[number - 1]["done"]
                save_tasks(tasks)
                print("Updated.")

    elif choice == "6":
        if len(tasks) == 0:
            print("Not tasks to edit.")
        else:
            print("Your Tasks:")
            for number, task in enumerate(tasks, start=1):
                mark = "x" if task["done"] else " "
                print(f" {number}. [{mark}] {task['text']}")
            raw = input("Which number do you want to update? ").strip()
            try:
                number = int(raw)
            except ValueError:
                print("Please type a number.")
                continue
            if number < 1 or number > len(tasks):
                print("That number is not on the list.")
            else:
                current = tasks[number -1]["text"]
                new_text = input(f"New text: ").strip()
                if new_text == "":
                    print("Please type a new text.")
                else:
                    tasks[number -1]["text"] = new_text
                    save_tasks(tasks)
                    print(f"Now: {new_text} (was: {current})")

    else:
        print("Please type 1, 2, 3, or 4.")
