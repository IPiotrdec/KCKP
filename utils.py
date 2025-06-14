from datetime import datetime

#Date safeguard
def parse_date(date_str):
    try:
        return datetime.strptime(date_str, "%Y-%m-%d")
    except ValueError:
        return None

#Revere for listbox
def format_date(date_obj):
    if date_obj:
        return date_obj.strftime("%Y-%m-%d")
    return ""

#Sorting
def sort_tasks_by_date(tasks):
    return sorted(tasks, key=lambda t: parse_date(t.due_date) or datetime.max)
