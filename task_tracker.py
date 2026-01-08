import argparse
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    # TO-DO: Do something if the file is corrupted
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    else:
        tasks = []
    return tasks
 
def save_tasks(tasks):
    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False)

def get_id(tasks):
    if tasks:
        return max(task['id'] for task in tasks) + 1
    return 1

def add_task(task):
    tasks = load_tasks()
    new_task = {
        'id': get_id(tasks),
        'description': task,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
        }
    tasks.append(new_task)
    save_tasks(tasks)
    print(f'Task "{task}" was successfully saved.')

def update_task(id, new_description):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task['id'] == id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            found = True
            break
    if found:
        save_tasks(tasks)
        print('Task was successfully updated')
    else:
        print(f'Task with ID {id} was not found')

def delete_task(id):
    tasks = load_tasks()
    found = False
    for i, task in enumerate(tasks):
        if task['id'] == id:
            tasks.pop(i)
            found = True
            break
    if found:
        save_tasks(tasks)
        print('Task was successfully deleted')
    else:
        print(f'Task with ID {id} was not found')

def list_tasks():
    # TO-DO: Add listing by status
    tasks = load_tasks()
    for task in tasks:
        print(f'ID: {task['id']}')
        print(f'Description: {task['description']}')
        print(f'Status: {task['status']}')
        print(f'Created At: {task['createdAt']}')
        print("-----------------------------------")
    else:
        print('There is no tasks available')

def change_status(id, status):
    tasks = load_tasks()
    found = False
    for task in tasks:
        if task['id'] == id:
            task['status'] = status
            found = True
            break
    if found:
        save_tasks(tasks)
        print('Status was successfully updated')
    else:
        print(f'Task with ID {id} was not found')

def main():
    parser = argparse.ArgumentParser(description='Simple CLI tool to organize your tasks')

    subparsers = parser.add_subparsers(dest='action', required=True, help='Actions available')

    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('task', type=str, help='Description of the task to be added')

    parser_update = subparsers.add_parser('update', help='Update an existing task')
    parser_update.add_argument('id', type=int, help='Unique ID of the task to be modified')
    parser_update.add_argument('new_description', type=str, help='New description for the specified task')

    parser_delete = subparsers.add_parser('delete', help='Delete an existing task')
    parser_delete.add_argument('id', type=int, help='Unique ID of the task to be updated')

    parser_list = subparsers.add_parser('list', help='List the available tasks')

    args = parser.parse_args()

    if args.action == 'add':
        add_task(args.task)
    elif args.action == 'list':
        list_tasks()
    elif args.action == 'update':
        update_task(args.id, args.new_description)
    elif args.action == 'delete':
        delete_task(args.id)
    
    # TO-DO: Add mark_in_progress status logic
    # TO-DO: Add mark-done status logic

if __name__ == "__main__":
    main()