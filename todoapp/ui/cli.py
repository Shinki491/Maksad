from datetime import datetime

class CLI:
    def __init__(self, task_manager):
        self.task_manager = task_manager

    def display_menu(self):
        print("\n===================================")
        print("     📝  To-Do List Menu  📝")
        print("===================================")
        print("1. ➕ Add a new task")
        print("2. 📋 View tasks")
        print("3. ✅ Mark a task as completed")
        print("4. 🔍 View completed tasks")
        print("5. ❌ Exit")
        print("===================================")
        print("Please select an option (1-5):")

    def add_task(self):
        title = input("Task title: ").strip()
        while not title:
            title = input("Task title: ").strip()
        description = input("Task description: ")
        priority_type = input("Task priority (High/Medium/Low): ").strip().capitalize()
        difficulty = int(input("Task difficulty ([1-5]): "))
        deadline = input("Enter the deadline date (YYYY-MM-DD): ")
        try:
            user_date = datetime.strptime(deadline, "%Y-%m-%d").date()
            print(f"Date entered: {user_date}")
        except ValueError:
            print("Invalid date format! Please use YYYY-MM-DD.")

        if self.task_manager.has_task(title):
            print("A task with this name exists.")
            return
        if priority_type not in ["High", "Medium", "Low"]:
            print("Invalid priority. Task not added.")
            return
        if difficulty > 5 or difficulty < 1:
            print("Invalid difficulty. Task not added.")
            return
        days = (user_date - datetime.today().date()).days
        self.task_manager.add_task(title, description, priority_type, difficulty, days, deadline)
        print(f"Task added with title: '{title}'")

    def view_tasks(self):
        tasks = self.task_manager.get_tasks()
        if not tasks:
            print("No tasks available.")
            return

        print("\n---------- Tasks ----------")
        for idx, task in enumerate(tasks):
            if isinstance(task.deadline, str):
                task_deadline = datetime.strptime(task.deadline, "%Y-%m-%d")  
                days_left = (task_deadline.date() - datetime.today().date()).days
            else:
                days_left = (task.deadline - datetime.today().date()).days
            task.days = days_left
            if task.priority_type == "High":
                pr_num = 100    
            elif task.priority_type == "Medium":
                pr_num = 50
            elif task.priority_type == "Low":
                pr_num = 10
            priority = (pr_num * int(task.difficulty))/ (task.days + 1) 
            task.priority = priority
            print(f"{idx + 1}. {task.title} (Priority: {task.priority})")

        print(" -------------------------------------------")
        print("| To go back press Enter.                  |")
        print("| To view a task enter the id of the task. |")
        print(" -------------------------------------------")
        task_check = input("View task: ")
        if (task_check.strip()):
            for idx, task in enumerate(tasks):
                if idx == int(task_check.strip()) - 1:
                    self.expand_task(task)
                else: 
                    print(f"Task #{task_check} does not exist.")
                    self.view_tasks()


    def expand_task(self, task):
        print("--------------------------------------------------------------")
        print(f"Title: '{task.title}'")
        print(f"Priority: '{task.priority}'")
        print(f"Difficulty: '{task.difficulty}'")
        print(f"Deadline: '{task.deadline}'")        
        print("Description: ")
        print(task.description)
        print("--------------------------------------------------------------")
        
        print("1. Edit task")
        print("2. Delete task")
        print("3. Go back")
        edit = input("What do you want to do? ")
        if edit == "1":
            self.edit_task(task)
        elif edit == "2":
            del_task_name = task.title
            self.task_manager.delete_task(task)
            print(f"Task '{del_task_name}' successfully deleted!")
            self.view_tasks()    
        elif edit == "3":
            self.view_tasks()    
        else: 
            print("ERROR: something weird just happened while exitting the editting task section in view_tasks()") 
            

    def expand_completed_task(self, task):
        print("--------------------------------------------------------------")
        print(f"Title: '{task.title}'")
        print(f"Priority: '{task.priority}'")
        print(f"Difficulty: '{task.difficulty}'")
        print(f"Deadline: '{task.deadline}'")     
        print("Description: ")
        print(task.description)
        print("--------------------------------------------------------------")
        
        print("1. Delete task")
        print("2. Go back")
        delete = input("What do you want to do? ")
        
        if delete == "1":
            del_task_name = task.title
            self.task_manager.delete_completed_task(task)
            print(f"Task '{del_task_name}' successfully deleted!")
            self.view_completed_tasks()    
        elif delete == "2":
            self.view_completed_tasks()    
        else: 
            print("ERROR: something weird just happened while exitting the editting task section in view_tasks()") 

    def edit_task(self, task):
        print("\nWhat would you like to edit?")
        print("1. Title.")
        print("2. Description.")
        print("3. Priority.")
        print("4. Difficulty.")
        print("5. Deadline.")
        print("6. Nothing. Go back.")
        choice = input("Please select an option (1-6): ")
        if choice == '1':
            print("Change the title.") 
            changed = input("New title: ").strip()
            task.title = changed
            print("Change successful!")
            self.expand_task(task)
        elif choice == '2':
            print("Change the description.") 
            changed = input("New description: ").strip()
            task.description = changed
            print("Change successful!")
            self.expand_task(task)   
        elif choice == '3':
            print("Change the priority.") 
            changed = input("New priority (high/medium/low): ").strip().capitalize()
            if changed == "High":
                pr_num = 125
            elif changed == "Medium":
                pr_num = 25
            elif changed == "Low":
                pr_num = 5
            new_priority = (pr_num * int(task.difficulty))/ (task.days + 1)
            task.priority = new_priority
            print("Change successful!")
            self.expand_task(task)   
        elif choice == '4':
            print("Change the difficulty.") 
            changed = input("New difficulty: (1-5) ").strip()
            task.difficulty = changed
            print("Change successful!")
            if task.priority_type == "High":
                pr_num = 100    
            elif task.priority_type == "Medium":
                pr_num = 50
            elif task.priority_type == "Low":
                pr_num = 10
            priority = (pr_num * int(task.difficulty))/ (task.days + 1)
            task.priority = priority
            self.expand_task(task)   
        elif choice == '5':
            print("Change the deadline.")
            deadline = input("Enter the new deadline date (YYYY-MM-DD): ")
            try:
                user_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                print(f"Date entered: {user_date}")
            except ValueError:
                print("Invalid date format! Please use YYYY-MM-DD.")

            task.deadline = user_date
            days_left = (user_date - datetime.today().date()).days
            task.days = days_left

            if task.priority_type == "High":
                pr_num = 100    
            elif task.priority_type == "Medium":
                pr_num = 50
            elif task.priority_type == "Low":
                pr_num = 10
            priority = (pr_num * int(task.difficulty))/ (task.days + 1) 
            task.priority = priority

            self.expand_task(task)   
        elif choice == '6':
            self.expand_task(task)
        else: print("ERROR: something weird in edit_task()")


    def mark_task_completed(self):
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
        completed_tasks = self.task_manager.get_completed_tasks()
        if not completed_tasks:
            print("No completed tasks.")
            return

        print("\n--- Completed Tasks ---")
        for idx, task in enumerate(completed_tasks):
            print(f"{idx + 1}. {task.title} (Priority: {task.priority})")

        print(" -------------------------------------------")
        print("| To go back press Enter.                  |")
        print("| To view a task enter the id of the task. |")
        print(" -------------------------------------------")
        task_check = input("View task: ")
        if (task_check.strip()):
            for idx, task in enumerate(completed_tasks):
                if idx == int(task_check.strip()) - 1:
                    self.expand_completed_task(task)
                else: 
                    print(f"Task #{task_check} does not exist.")
                    self.view_completed_tasks()
