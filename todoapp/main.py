from core.task_manager import TaskManager
from data.storage import Storage
from ui.cli import CLI

def main():
    # Initialize storage and task manager
    storage = Storage("data/db/tasks.json")  # Change to .db if using SQLite
    task_manager = TaskManager(storage)
    cli = CLI(task_manager)
    
    # Load existing tasks from storage
    task_manager.load_tasks()

    # Main menu loop
    while True:
        cli.display_menu()
        choice = input("Choose an option: ").strip()

        if choice == "1":
            cli.add_task()
        elif choice == "2":
            cli.view_tasks()
        elif choice == "3":
            cli.mark_task_completed()
        elif choice == "4":
            cli.view_completed_tasks()
        elif choice == "5":
            print("Exiting... Goodbye!")
            task_manager.save_tasks()  # Save tasks before exiting
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
