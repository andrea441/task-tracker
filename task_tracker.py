import argparse
import json
import os
from datetime import datetime

TASKS_FILE = 'tasks.json'

def get_id(tasks):
    if tasks:
        return max(task['id'] for task in tasks) + 1
    return 1

def add_task(task):    
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r', encoding='utf-8') as f:
            tasks = json.load(f)
    else:
        tasks = []

    new_task = {
        'id': get_id(tasks),
        'description': task,
        'status': 'todo',
        'createdAt': datetime.now().isoformat(),
        'updatedAt': datetime.now().isoformat()
        }
    
    tasks.append(new_task)

    with open(TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(tasks, f, indent=2, ensure_ascii=False) 

def delete_task(id):
    # TO-DO: Create the logic for this function deleting the specified task using its id.
    pass

def list_tasks():
    # TO-DO: Create the logic for this function. Iterate through tasks.json and print each object.
    pass

def main():
    parser = argparse.ArgumentParser(description='Simple CLI tool to organize your tasks')

    subparsers = parser.add_subparsers(dest='action', required=True, help='Actions available')

    parser_add = subparsers.add_parser('add', help='Add a new task')
    parser_add.add_argument('task', type=str, help='Description of the task to be added')

    args = parser.parse_args()

    if args.action == 'add':
        add_task(args.task)
        print(f'Task "{args.task}" was successfully saved.')

''' 
Example of an "task" object:
{
    'id': 1,
    'description': 'Example',
    'status': 'todo',
    'createdAt': "2026-01-07T18:24:06.336485",
    "updatedAt": "2026-01-07T18:24:06.336509"

}
''' 

if __name__ == "__main__":
    main()