class Task:
    def __init__(self, title, priority, completed=False):
        """
        Initialize a new Task.

        :param title: The title of the task.
        :param priority: The priority of the task (e.g., "High", "Medium", "Low").
        :param completed: The completion status of the task (default is False).
        """
        self.title = title
        self.priority = priority
        self.completed = completed

    def mark_completed(self):
        """Mark the task as completed."""
        self.completed = True

    def to_dict(self):
        """
        Convert the task to a dictionary representation.

        :return: A dictionary containing task attributes.
        """
        return {
            "title": self.title,
            "priority": self.priority,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        """
        Create a Task instance from a dictionary.

        :param data: A dictionary containing task attributes.
        :return: A Task instance.
        """
        return Task(
            title=data["title"],
            priority=data["priority"],
            completed=data["completed"]
        )
