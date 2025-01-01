import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, timedelta
import calendar
from tkinter import Canvas
from datetime import date

def run_gui(task_manager):
    app = TaskManagerApp(task_manager)
    app.mainloop()

class TaskManagerApp(tk.Tk):
    def __init__(self, task_manager):
        super().__init__()
        self.task_manager = task_manager
        self.title("To-Do List App")
        self.geometry("800x400")

        # Frames
        self.task_list_frame = ttk.Frame(self)
        self.task_list_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.calendar_frame = ttk.Frame(self)
        self.calendar_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.button_frame = ttk.Frame(self.task_list_frame)
        self.button_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.calendar_nav_frame = ttk.Frame(self.calendar_frame)
        self.calendar_nav_frame.pack(side=tk.TOP, fill=tk.X)

        # Task List
        self.task_listbox = tk.Listbox(self.task_list_frame, height=15)
        self.task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.scrollbar = ttk.Scrollbar(self.task_list_frame, command=self.task_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.task_listbox.config(yscrollcommand=self.scrollbar.set)

        # Buttons
        ttk.Button(self.button_frame, text="Add Task", command=self.add_task_popup).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="View Task", command=self.view_task).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Mark Completed", command=self.mark_completed).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="View Completed", command=self.view_completed).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.button_frame, text="Exit", command=self.exit_app).pack(side=tk.RIGHT, padx=5, pady=5)

        # Initialize calendar
        self.current_year = date.today().year
        self.current_month = date.today().month
        self.calendar_canvas = Canvas(self.calendar_frame)
        self.calendar_canvas.pack(fill=tk.BOTH, expand=True)

        ttk.Button(self.calendar_nav_frame, text="Previous", command=self.prev_month).pack(side=tk.LEFT, padx=5, pady=5)
        ttk.Button(self.calendar_nav_frame, text="Next", command=self.next_month).pack(side=tk.RIGHT, padx=5, pady=5)

        # Load tasks and initialize view
        self.refresh_task_list()
        self.create_calendar_view()

    def create_calendar_view(self):
        """Create or update the calendar view."""
        self.calendar_canvas.delete("all")  # Clear the canvas

        # Generate calendar for the current month
        cal = calendar.TextCalendar()
        calendar_data = cal.formatmonth(self.current_year, self.current_month)
        self.calendar_canvas.create_text(
            10, 10, anchor="nw", text=calendar_data, font=("Courier", 10), fill="black"
        )

        # Highlight task deadlines
        tasks = self.task_manager.get_tasks()
        for task in tasks:
            task_deadline = datetime.strptime(task.deadline, "%Y-%m-%d").date() if isinstance(task.deadline, str) else task.deadline
            if task_deadline.year == self.current_year and task_deadline.month == self.current_month:
                self.highlight_date(task_deadline.day, task.title)

    def highlight_date(self, day, task_title):
        """Highlight a specific day on the calendar."""
        self.calendar_canvas.create_text(
            10, 100 + (day * 20), anchor="nw", text=f"{day:2} - {task_title}", font=("Courier", 8), fill="blue"
        )

    def prev_month(self):
        """Navigate to the previous month."""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.create_calendar_view()

    def next_month(self):
        """Navigate to the next month."""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.create_calendar_view()

    def refresh_task_list(self):
        """Refresh the task listbox and update the calendar."""
        self.task_listbox.delete(0, tk.END)
        for idx, task in enumerate(self.task_manager.get_tasks()):
            self.task_listbox.insert(tk.END, f"{idx + 1}. {task.title} (Priority: {task.priority})")
        self.create_calendar_view()

    def add_task_popup(self):
        """Open a popup window to add a new task."""
        popup = tk.Toplevel(self)
        popup.title("Add Task")
        popup.geometry("400x300")

        tk.Label(popup, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(popup, width=30)
        title_entry.pack()

        tk.Label(popup, text="Description:").pack(pady=5)
        desc_entry = ttk.Entry(popup, width=30)
        desc_entry.pack()

        tk.Label(popup, text="Priority (High/Medium/Low):").pack(pady=5)
        priority_entry = ttk.Entry(popup, width=30)
        priority_entry.pack()

        tk.Label(popup, text="Difficulty (1-5):").pack(pady=5)
        difficulty_entry = ttk.Entry(popup, width=30)
        difficulty_entry.pack()

        tk.Label(popup, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        deadline_entry = ttk.Entry(popup, width=30)
        deadline_entry.pack()

        def save_task():
            title = title_entry.get().strip()
            description = desc_entry.get().strip()
            priority = priority_entry.get().strip().capitalize()
            difficulty = difficulty_entry.get().strip()
            deadline = deadline_entry.get().strip()

            if not title or not priority or not difficulty or not deadline:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                difficulty = int(difficulty)
                user_date = datetime.strptime(deadline, "%Y-%m-%d").date()
                days_until_deadline = (user_date - datetime.today().date()).days

                if days_until_deadline < 0:
                    messagebox.showerror("Error", "The deadline cannot be in the past!")
                    return

                self.task_manager.add_task(title, description, priority, difficulty, days_until_deadline, deadline)
                messagebox.showinfo("Success", "Task added successfully!")
                self.refresh_task_list()
                popup.destroy()
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Ensure difficulty is a number and the date is in YYYY-MM-DD format.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        ttk.Button(popup, text="Save Task", command=save_task).pack(pady=10)

    def view_task(self):
        """View and edit the selected task's details."""
        selected_idx = self.task_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("Warning", "No task selected.")
            return

        task = self.task_manager.get_tasks()[selected_idx[0]]

        # Popup for viewing/editing
        popup = tk.Toplevel(self)
        popup.title("View/Edit Task")
        popup.geometry("400x400")

        # Task Details
        tk.Label(popup, text="Title:").pack(pady=5)
        title_entry = ttk.Entry(popup, width=30)
        title_entry.insert(0, task.title)
        title_entry.pack()

        tk.Label(popup, text="Description:").pack(pady=5)
        desc_entry = ttk.Entry(popup, width=30)
        desc_entry.insert(0, task.description)
        desc_entry.pack()

        tk.Label(popup, text="Priority (High/Medium/Low):").pack(pady=5)
        priority_entry = ttk.Entry(popup, width=30)
        priority_entry.insert(0, task.priority_type)
        priority_entry.pack()

        tk.Label(popup, text="Difficulty (1-5):").pack(pady=5)
        difficulty_entry = ttk.Entry(popup, width=30)
        difficulty_entry.insert(0, task.difficulty)
        difficulty_entry.pack()

        tk.Label(popup, text="Deadline (YYYY-MM-DD):").pack(pady=5)
        deadline_entry = ttk.Entry(popup, width=30)
        deadline_entry.insert(0, task.deadline)
        deadline_entry.pack()

        def save_changes():
            """Save the edited task details."""
            new_title = title_entry.get().strip()
            new_description = desc_entry.get().strip()
            new_priority = priority_entry.get().strip().capitalize()
            new_difficulty = difficulty_entry.get().strip()
            new_deadline = deadline_entry.get().strip()

            if not new_title or not new_priority or not new_difficulty or not new_deadline:
                messagebox.showerror("Error", "All fields are required!")
                return

            try:
                new_difficulty = int(new_difficulty)
                user_date = datetime.strptime(new_deadline, "%Y-%m-%d").date()
                days_until_deadline = (user_date - datetime.today().date()).days

                if days_until_deadline < 0:
                    messagebox.showerror("Error", "The deadline cannot be in the past!")
                    return

                # Update task attributes
                task.title = new_title
                task.description = new_description
                task.priority = new_priority
                task.difficulty = new_difficulty
                task.deadline = new_deadline
                task.days = days_until_deadline

                # Recalculate priority if necessary
                if new_priority == "High":
                    pr_num = 125
                elif new_priority == "Medium":
                    pr_num = 25
                elif new_priority == "Low":
                    pr_num = 5
                else:
                    messagebox.showerror("Error", "Invalid priority type!")
                    return

                task.priority = (pr_num * new_difficulty) / (days_until_deadline + 1)

                self.refresh_task_list()
                popup.destroy()
                messagebox.showinfo("Success", "Task updated successfully!")
            except ValueError:
                messagebox.showerror("Error", "Invalid input. Ensure difficulty is a number and the date is in YYYY-MM-DD format.")
            except Exception as e:
                messagebox.showerror("Error", f"An error occurred: {e}")

        # Buttons for saving or canceling
        ttk.Button(popup, text="Save Changes", command=save_changes).pack(side=tk.LEFT, padx=10, pady=10)
        ttk.Button(popup, text="Cancel", command=popup.destroy).pack(side=tk.RIGHT, padx=10, pady=10)


    def mark_completed(self):
        """Mark the selected task as completed."""
        selected_idx = self.task_listbox.curselection()
        if not selected_idx:
            messagebox.showwarning("Warning", "No task selected.")
            return

        self.task_manager.mark_task_completed(selected_idx[0])
        self.refresh_task_list()
        messagebox.showinfo("Success", "Task marked as completed.")

    def view_completed(self):
        """View the list of completed tasks."""
        completed_tasks = self.task_manager.get_completed_tasks()
        if not completed_tasks:
            messagebox.showinfo("Completed Tasks", "No completed tasks.")
            return

        popup = tk.Toplevel(self)
        popup.title("Completed Tasks")
        popup.geometry("400x300")

        task_listbox = tk.Listbox(popup, height=15)
        task_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar = ttk.Scrollbar(popup, command=task_listbox.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        task_listbox.config(yscrollcommand=scrollbar.set)

        for idx, task in enumerate(completed_tasks):
            task_listbox.insert(tk.END, f"{idx + 1}. {task.title} (Completed)")

        ttk.Button(popup, text="Close", command=popup.destroy).pack(pady=10)

    def exit_app(self):
        """Exit the application."""
        self.task_manager.save_tasks()
        self.destroy()
