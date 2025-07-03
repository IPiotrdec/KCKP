import tkinter as tk
from tkinter import Listbox, Scrollbar, Frame, Label, Button, messagebox
import data_manager
import utils
import constants
import settings_manager
import ThemeManagera as theme

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Zarządzanie zadaniami")
        self.root.geometry("1000x600")
        self.current_view = "tasks"
        self.selected_date = None
        self.reset_confirm = False
        self.calendar_container = None
        self.tasks = data_manager.load_tasks()
        self.tags = []
        self.dark_mode = False

        self._build_ui()
        theme.apply_theme(self)
        theme.show_tasks(self)

    def _build_ui(self):
        # Header
        self.header_frame = Frame(self.root, height=60)
        self.header_frame.pack(fill=tk.X, side=tk.TOP)

        self.logo_label = Label(
            self.header_frame,
            text="TaskFlow",
            font=("Arial", 20, "bold"),
            bg=theme.DEFAULT_ACCENT,
            fg="white"
        )
        self.logo_label.pack(side=tk.LEFT, padx=10, pady=10)

        # Div1
        self.main_frame = Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # Div2
        self.menu_frame = Frame(self.main_frame, width=150)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)
        self._add_menu_buttons()

        # Div3
        self.content_frame = Frame(self.main_frame)
        self.content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.view_header = Label(self.content_frame,
                                 text="Moje zadania",
                                 font=("Arial", 14))
        self.view_header.pack(pady=10, anchor="w", padx=20)
        self.header_label = self.view_header
        # Task list
        self.task_box = Frame(self.content_frame)
        self.task_box.pack(fill=tk.BOTH, expand=True, padx=20)

        self.listbox = Listbox(self.task_box)
        self.listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.listbox.bind("<Double-Button-1>", self.show_description)

        sb = Scrollbar(self.task_box, command=self.listbox.yview)
        sb.pack(side=tk.RIGHT, fill=tk.Y)
        self.listbox.config(yscrollcommand=sb.set)

        # Div for buttons
        self.button_frame = Frame(self.content_frame)
        self.button_frame.pack(pady=10)

        Button(self.button_frame, text="Dodaj zadanie",
               bg="#a7d9f5",
               command=lambda: constants.add_task_window(self)).grid(row=0, column=0, padx=5)
        Button(self.button_frame, text="Usuń zaznaczone",
               bg="#f5a7a7",
               command=self.remove_selected_task).grid(row=0, column=1, padx=5)
        Button(self.button_frame, text="Oznacz jako ukończone",
               bg="#c8f5a7",
               command=self.complete_selected_task).grid(row=0, column=2, padx=5)

    def _add_menu_buttons(self):
        buttons = [
            ("Moje zadania", lambda: theme.show_tasks(self)),
            ("Kalendarz", lambda: theme.show_calendar(self)),
            ("Archiwum", lambda: theme.show_archive(self)),
            ("Ustawienia", lambda: settings_manager.show_settings(self)),
            ("Zespół", lambda: theme.placeholder(self))
        ]
        for label, cmd in buttons:
            Button(
                self.menu_frame,
                text=label,
                command=cmd,
                bg=self.menu_frame["bg"],
                bd=0,
                relief="flat",
                highlightthickness=0,
                fg="black",
                activeforeground="gray20",
                font=("Arial", 10),
                anchor="w"
            ).pack(fill=tk.X, pady=4, padx=20)

    def show_description(self, event):
        selection = self.listbox.curselection()
        if selection:
            task = utils.get_visible_tasks(self.tasks, self.current_view, self.selected_date)[selection[0]]
            messagebox.showinfo(task.name, f"{task.description}\n\nTermin: {task.due_date}\nKategoria: {task.category}\nPriorytet: {task.priority}")

    def refresh_ui(self):
        self.listbox.delete(0, tk.END)
        for task in utils.get_visible_tasks(self.tasks, self.current_view, self.selected_date):
            self.listbox.insert(tk.END, f"[{task.priority}] {task.name} ({task.due_date}) - {task.category}")

    def remove_selected_task(self):
        selection = self.listbox.curselection()
        if selection:
            task = utils.get_visible_tasks(self.tasks, self.current_view, self.selected_date)[selection[0]]
            self.tasks = utils.delete_task(self.tasks, task.task_id)
            self.refresh_ui()

    def complete_selected_task(self):
        selection = self.listbox.curselection()
        if selection:
            task = utils.get_visible_tasks(self.tasks, self.current_view, self.selected_date)[selection[0]]
            self.tasks = utils.complete_task(self.tasks, task.task_id)
            self.refresh_ui()