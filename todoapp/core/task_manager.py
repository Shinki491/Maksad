from core.task import Task

class TaskManager:
    def __init__(self, storage):
        self.storage = storage
        self.tasks = []
        self.completed_tasks = []

    def add_task(self, title, description, priority_type, difficulty, days, deadline): 
        if priority_type == "High":
            pr_num = 100
        elif priority_type == "Medium":
            pr_num = 50
        elif priority_type == "Low":
            pr_num = 10
        priority = (pr_num * int(difficulty))/ (days + 1) 
        new_task = Task(title, description, priority_type, difficulty, days, deadline, priority)
        self.tasks.append(new_task)

    def get_tasks(self):
        return sorted(self.tasks, key=lambda t: t.priority, reverse=True)  


    def get_completed_tasks(self):
        return self.completed_tasks

    def mark_task_completed(self, task_index):
        if 0 <= task_index < len(self.tasks):
            task = self.tasks.pop(task_index)
            task.mark_completed()
            self.completed_tasks.append(task)

    def load_tasks(self):
        data = self.storage.load()
        self.tasks = [Task.from_dict(task) for task in data.get("tasks", [])]
        self.completed_tasks = [Task.from_dict(task) for task in data.get("completed_tasks", [])]

    def save_tasks(self):
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "completed_tasks": [task.to_dict() for task in self.completed_tasks]
        }
        self.storage.save(data)

    def has_task(self, title):
        for _,task in enumerate(self.tasks):
            if (task.title == title):
                return True
            
        return False
    
    def delete_task(self, task):
        self.tasks.remove(task)
    
    def delete_completed_task(self, task):
        self.completed_tasks.remove(task)