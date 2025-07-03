from datetime import datetime
from task import Task
import data_manager

def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

def format_date(date_obj):
    if date_obj:
        return date_obj.strftime("%Y-%m-%d")
    return ""

def sort_tasks_by_date(tasks):
    return sorted(tasks, key=lambda t: parse_date(t.due_date) or datetime.max)


def get_visible_tasks(tasks, view, selected_date=None):
    if view == "tasks":
        return [t for t in tasks if not t.completed]
    elif view == "archive":
        return [t for t in tasks if t.completed]
    elif view == "calendar" and selected_date:
        return [t for t in tasks if t.due_date == selected_date]   #check layter!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    return []

# Task operator
def add_task(tasks, name, description, due_date, category, priority):
    task_id = max([t.task_id for t in tasks], default=0) + 1
    task = Task(task_id, name, description, due_date, category, priority)
    tasks.append(task)
    data_manager.save_tasks(tasks)
    return tasks

def delete_task(tasks, task_id):
    tasks = [t for t in tasks if t.task_id != task_id]
    data_manager.save_tasks(tasks)
    return tasks

def complete_task(tasks, task_id):
    for task in tasks:
        if task.task_id == task_id:
            task.completed = True
            break
    data_manager.save_tasks(tasks)
    return tasks

def reset_all_tasks():
    data_manager.save_tasks([])
    return []
