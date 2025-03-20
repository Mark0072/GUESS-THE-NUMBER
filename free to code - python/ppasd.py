import json
import os
import argparse

# File to store tasks
TASKS_FILE = 'tasks.json'

# Default task structure
DEFAULT_TASKS = []

# Load tasks from the JSON file
def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as f:
            return json.load(f)
    else:
        return DEFAULT_TASKS

# Save tasks to the JSON file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as f:
        json.dump(tasks, f, indent=4)

# Add a task
def add_task(title, description):
    tasks = load_tasks()
    new_task = {
        'id': len(tasks) + 1,
        'title': title,
        'description': description,
        'status': 'not started'
    }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f"Task '{title}' added.")

# Update a task
def update_task(task_id, title=None, description=None, status=None):
    tasks = load_tasks()
    task = next((task for task in tasks if task['id'] == task_id), None)
    
    if task:
        if title:
            task['title'] = title
        if description:
            task['description'] = description
        if status:
            task['status'] = status
        save_tasks(tasks)
        print(f"Task {task_id} updated.")
    else:
        print(f"Task with id {task_id} not found.")

# Delete a task
def delete_task(task_id):
    tasks = load_tasks()
    tasks = [task for task in tasks if task['id'] != task_id]
    save_tasks(tasks)
    print(f"Task {task_id} deleted.")

# List tasks
def list_tasks(status=None):
    tasks = load_tasks()
    if status:
        tasks = [task for task in tasks if task['status'] == status]
    
    if tasks:
        for task in tasks:
            print(f"ID: {task['id']}, Title: {task['title']}, Status: {task['status']}")
    else:
        print("No tasks found.")

# Main function to handle CLI arguments
def main():
    parser = argparse.ArgumentParser(description="Task Tracker CLI")
    
    # Add task
    parser.add_argument('--add', metavar=('title', 'description'), nargs=2, help="Add a new task")
    
    # Update task
    parser.add_argument('--update', metavar=('id', 'title', 'description', 'status'), nargs=4, type=str, help="Update a task")
    
    # Delete task
    parser.add_argument('--delete', metavar='id', type=int, help="Delete a task")
    
    # List tasks
    parser.add_argument('--list', action='store_true', help="List all tasks")
    parser.add_argument('--done', action='store_true', help="List all done tasks")
    parser.add_argument('--not-done', action='store_true', help="List all tasks that are not done")
    parser.add_argument('--in-progress', action='store_true', help="List all tasks that are in progress")
    
    args = parser.parse_args()
    
    if args.add:
        title, description = args.add
        add_task(title, description)
    elif args.update:
        task_id, title, description, status = args.update
        update_task(int(task_id), title, description, status)
    elif args.delete:
        delete_task(args.delete)
    elif args.list:
        list_tasks()
    elif args.done:
        list_tasks('done')
    elif args.not_done:
        list_tasks('not started')
    elif args.in_progress:
        list_tasks('in progress')
    else:
        print("Invalid command. Use --help to see available commands.")

if __name__ == "__main__":
    main()
