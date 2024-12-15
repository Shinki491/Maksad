class CLI:
    def __init__(self, task_manager):
        """
        Initialize the CLI.

        :param task_manager: An instance of TaskManager to manage tasks.
        """
        self.task_manager = task_manager

    def display_menu(self):
        """
        Display the main menu options.
        """
        print("\n--- To-Do List Menu ---")
        print("1. Add a new task")
        print("2. View tasks")
        print("3. Mark a task as completed")
        print("4. View completed tasks")
        print("5. Exit")

    def add_task(self):
        """
        Prompt the user to add a new task.
        """
        title = input("Enter task title: ").strip()
        priority = input("Enter task priority (High/Medium/Low): ").strip().capitalize()
        if priority not in ["High", "Medium", "Low"]:
            print("Invalid priority. Task not added.")
            return

        self.task_manager.add_task(title, priority)
        print(f"Task '{title}' added with priority '{priority}'.")

    def view_tasks(self):
        """
        Display the list of tasks sorted by priority.
        """
        tasks = self.task_manager.get_tasks()
        if not tasks:
            print("No tasks available.")
            return

        print("\n--- Tasks ---")
        for idx, task in enumerate(tasks):
            print(f"{idx + 1}. {task.title} (Priority: {task.priority})")

    def mark_task_completed(self):
        """
        Prompt the user to mark a task as completed.
        """
        tasks = self.task_manager.get_tasks()
        if not tasks:
            print("No tasks available to complete.")
            return

        print("\n--- Tasks ---")
        for idx, task in enumerate(tasks):
            print(f"{idx + 1}. {task.title} (Priority: {task.priority})")

        try:
            task_index = int(input("Enter the number of the task to mark as completed: ")) - 1
            self.task_manager.mark_task_completed(task_index)
            print("Task marked as completed.")
        except (ValueError, IndexError):
            print("Invalid selection. Please try again.")

    def view_completed_tasks(self):
        """
        Display the list of completed tasks.
        """
        completed_tasks = self.task_manager.get_completed_tasks()
        if not completed_tasks:
            print("No completed tasks.")
            return

        print("\n--- Completed Tasks ---")
        for idx, task in enumerate(completed_tasks):
            print(f"{idx + 1}. {task.title} (Priority: {task.priority})")
