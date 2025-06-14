class Task:
    def __init__(self, task_id, name, description, due_date, category, priority, completed=False):
        self.task_id = task_id
        self.name = name
        self.description = description
        self.due_date = due_date
        self.category = category
        self.priority = priority
        self.completed = completed

    def to_dict(self):
        return {
            "task_id": self.task_id,
            "name": self.name,
            "description": self.description,
            "due_date": self.due_date,
            "category": self.category,
            "priority": self.priority,
            "completed": self.completed
        }
    #Dict Format (read ".json")
    @staticmethod
    def from_dict(data):
        return Task(
            task_id=data["task_id"],
            name=data["name"],
            description=data["description"],
            due_date=data["due_date"],
            category=data["category"],
            priority=data["priority"],
            completed=data.get("completed", False)
        )
