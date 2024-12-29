from core.task_manager import TaskManager
from data.storage import Storage
from ui.gui import run_gui

def main():
    storage = Storage("data/db/tasks.json")
    task_manager = TaskManager(storage)
    task_manager.load_tasks()  # Load existing tasks
    run_gui(task_manager)

if __name__ == "__main__":
    main()