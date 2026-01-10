import argparse
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    try:
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []
 
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
    for task in tasks:
        if task['id'] == id:
            task['description'] = new_description
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task with ID {id} was successfully updated')
            return
    print(f'Task with ID {id} was not found')

def delete_task(id):
    tasks = load_tasks()
    for i, task in enumerate(tasks):
        if task['id'] == id:
            tasks.pop(i)
            save_tasks(tasks)
            print(f'Task with ID {id} was successfully deleted')
            return
    print(f'Task with ID {id} was not found')

def list_tasks(status=None):
    tasks = load_tasks()
    print('------------------------------------')
    for task in tasks:
        if status and task['status'] != status:
            continue
        print(f'ID: {task['id']}')
        print(f'Description: {task['description']}')
        print(f'Status: {task['status']}')
        # TO-DO: Print the dates in a human-readable format
        print(f'Created at: {task['createdAt']}')
        print(f'Updated at: {task['updatedAt']}')
        print('------------------------------------')
    
    # TO-DO: Add this message when there is no tasks of a certain status
    if not tasks:
        print('There are no tasks available')

def change_status(id, status):
    tasks = load_tasks()
    for task in tasks:
        if task['id'] == id:
            task['status'] = status
            task['updatedAt'] = datetime.now().isoformat()
            save_tasks(tasks)
            print(f'Task with ID {id} was successfully marked as {status}')
            return
    print(f'Task with ID {id} was not found')

def main():
    parser = argparse.ArgumentParser(description='Simple CLI tool to organize your tasks')

    subparsers = parser.add_subparsers(dest='action', required=True, help='Actions available')

    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('task', type=str, help='Description of the task to be added')
    parser_add.set_defaults(func=lambda args: add_task(args.task))

    parser_update = subparsers.add_parser('update', help='Update an existing task')
    parser_update.add_argument('id', type=int, help='Unique ID of the task to be modified')
    parser_update.add_argument('new_description', type=str, help='New description for the specified task')
    parser_update.set_defaults(func=lambda args: update_task(args.id, args.new_description))

    parser_delete = subparsers.add_parser('delete', help='Delete an existing task')
    parser_delete.add_argument('id', type=int, help='Unique ID of the task to be updated')
    parser_delete.set_defaults(func=lambda args: delete_task(args.id))

    parser_list = subparsers.add_parser('list', help='List the available tasks')
    parser_list.add_argument('status', type=str, nargs='?', choices=['todo', 'done', 'in-progress'], help='Filter tasks by status')
    parser_list.set_defaults(func=lambda args: list_tasks(args.status))

    parser_mark = subparsers.add_parser('mark', help='Marks an specific task with a status')
    parser_mark.add_argument('id', type=int, help='Unique ID of the task to mark')
    parser_mark.add_argument('status', type=str, choices=['todo', 'done', 'in-progress'], help='New status to which the selected task will change')
    parser_mark.set_defaults(func=lambda args: change_status(args.id, args.status))

    args = parser.parse_args()

    if hasattr(args, 'func'):
        args.func(args)
    
if __name__ == "__main__":
    main()