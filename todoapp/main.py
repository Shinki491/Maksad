from core.task_manager import TaskManager
from data.storage import Storage
from ui.gui import run_gui
# from ui.cli import CLI

def main():
    storage = Storage("data/db/tasks.json")
    task_manager = TaskManager(storage)
    task_manager.load_tasks()  # Load existing tasks
    run_gui(task_manager)

if __name__ == "__main__":
    main()


# In case you wanna try out the CLI version, uncomment the CLI import and comment the gui import and main() 

# def main():
#     storage = Storage("data/db/tasks.json")  
#     task_manager = TaskManager(storage)
#     cli = CLI(task_manager)  
    
#     task_manager.load_tasks()

#     while True:
#         cli.display_menu()
#         choice = input("Choose an option: ").strip()

#         if choice == "1":
#             cli.add_task()
#         elif choice == "2":
#             cli.view_tasks()
#         elif choice == "3":
#             cli.mark_task_completed()
#         elif choice == "4":
#             cli.view_completed_tasks()
#         elif choice == "5":
#             print("Exiting... Goodbye!")
#             task_manager.save_tasks()  
#             break
#         else:
#             print("Invalid choice. Please try again.")