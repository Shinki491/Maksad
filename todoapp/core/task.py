class Task:
    def __init__(self, title, description, priority_type, difficulty, days, deadline, priority, completed=False):
        self.title = title
        self.description = description
        self.priority_type = priority_type
        self.difficulty = difficulty
        self.days = days
        self.deadline = deadline
        self.priority = priority
        self.completed = completed

    def mark_completed(self):
        self.completed = True

    def to_dict(self):
        return {
            "title": self.title,
            "description": self.description,
            "priority_type": self.priority_type,
            "difficulty": self.difficulty,
            "days": self.days,
            "deadline": self.deadline,
            "priority": self.priority,
            "completed": self.completed
        }

    @staticmethod
    def from_dict(data):
        return Task(
            title=data["title"],
            description=data["description"],
            priority_type=data["priority_type"],
            difficulty=data["difficulty"],
            days=data["days"],
            deadline=data["deadline"],
            priority=data["priority"],
            completed=data["completed"]
        )
