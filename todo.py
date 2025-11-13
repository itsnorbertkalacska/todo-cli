import json
import os

TASK_FILE = "tasks.json"

def load_tasks():
    if not os.path.exists(TASK_FILE):
        return []
    try:
        with open(TASK_FILE, "r") as file:
            return json.load(file)
    except json.JSONDecodeError:
        print("Error: Corrupted tasks file. Starting with an empty list.")
        return []

def save_tasks(tasks):
    try:
        with open(TASK_FILE, "w") as file:
            json.dump(tasks, file, indent=4)
    except Exception as e:
        print(f"Error saving tasks: {e}")

def add_task(tasks, description):
    task_id = 1 if not tasks else max(task["id"] for task in tasks) + 1
    task = { "id": task_id, "description": description, "completed": False }
    tasks.append(task)
    save_tasks(tasks)
    print(f"Added task: {description}, (ID: {task_id})")

def delete_task(tasks, task_id):
    for i, task in enumerate(tasks):
        if tasks["id"] == task_id:
            tasks.pop(i)
            save_tasks(tasks)
            print(f"Deleted task ID {task_id}")
            return
    print(f"Task ID {task} not found")

def complete_task(tasks, task_id):
    for task in tasks:
        if task["id"] == task_id:
            task["completed"] = True
            save_tasks(tasks)
            print(f"Marked task ID {task_id} as completed")
            return
    print(f"Task ID {task_id} not found")

def list_tasks(tasks):
    if not tasks:
        print("No tasks found.")
        return
    print("\nTasks:")
    for task in tasks:
        status = "✓" if task["completed"] else " "
        print(f"[{status}] ID: {task['id']} - {task['description']}")

def main():
    tasks = load_tasks()
    print("Welcome to Todo CLI! Commands: add <task>, delete <id>, complete <id>, list, quit")

    while True:
        try:
            command = input("> ").strip().split(maxsplit=1)
            if not command:
                continue

            action = command[0].lower()
            args = command[1] if len(command) > 1 else ""

            if action == "quit":
                print("See you later!")
                break
            elif action == "list":
                list_tasks(tasks)
            elif action == "add" and args:
                add_task(tasks, args)
            elif action == "delete" and args:
                try:
                    task_id = int(args)
                    delete_task(tasks, task_id)
                except ValueError:
                    print("Error: Please provide a valid task ID")
            elif action == "complete" and args:
                try:
                    task_id = int(args)
                    complete_task(tasks, task_id)
                except ValueError: 
                    print("Error: Please provide a valid task ID")
            else:
                print("Invalid command. Use: add <task>, complete <id>, delete <id>, list, quit")

        except KeyboardInterrupt:
            print("\nSee you later!")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()

