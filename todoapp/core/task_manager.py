from core.task import Task

class TaskManager:
    def __init__(self, storage):
        """
        Initialize the TaskManager.

        :param storage: A storage instance for saving/loading tasks.
        """
        self.storage = storage
        self.tasks = []
        self.completed_tasks = []

    def add_task(self, title, priority):
        """
        Add a new task to the task list.

        :param title: The title of the task.
        :param priority: The priority of the task (e.g., "High", "Medium", "Low").
        """
        new_task = Task(title, priority)
        self.tasks.append(new_task)

    def get_tasks(self):
        """
        Retrieve the list of incomplete tasks sorted by priority.

        :return: A sorted list of incomplete tasks.
        """
        priority_order = {"High": 1, "Medium": 2, "Low": 3}
        return sorted(self.tasks, key=lambda t: priority_order[t.priority])

    def get_completed_tasks(self):
        """
        Retrieve the list of completed tasks.

        :return: A list of completed tasks.
        """
        return self.completed_tasks

    def mark_task_completed(self, task_index):
        """
        Mark a task as completed and move it to the completed list.

        :param task_index: The index of the task to mark as completed.
        """
        if 0 <= task_index < len(self.tasks):
            task = self.tasks.pop(task_index)
            task.mark_completed()
            self.completed_tasks.append(task)

    def load_tasks(self):
        """
        Load tasks and completed tasks from storage.
        """
        data = self.storage.load()
        self.tasks = [Task.from_dict(task) for task in data.get("tasks", [])]
        self.completed_tasks = [Task.from_dict(task) for task in data.get("completed_tasks", [])]

    def save_tasks(self):
        """
        Save tasks and completed tasks to storage.
        """
        data = {
            "tasks": [task.to_dict() for task in self.tasks],
            "completed_tasks": [task.to_dict() for task in self.completed_tasks]
        }
        self.storage.save(data)
