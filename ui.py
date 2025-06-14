import tkinter as tk
from tkinter import messagebox, simpledialog
from task import Task
import data_manager
import utils
import tkinter.ttk as ttk

class TaskApp:
    def __init__(self, root):
        self.root = root
        self.root.title("TaskFlow - Zarządzanie zadaniami")
        self.root.geometry("1000x600")

        self.tasks = data_manager.load_tasks()

        self.create_widgets()
        self.refresh_list()
    #Widget Interface
    def create_widgets(self):
        # Header
        self.header = tk.Frame(self.root, bg="#81c8dd", height=50)
        self.header.pack(side=tk.TOP, fill=tk.X)

        self.title_label = tk.Label(self.header, text="TaskFlow", bg="#81c8dd", fg="white", font=("Arial", 18, "bold"))
        self.title_label.pack(side=tk.LEFT, padx=20, pady=10)

        # Content
        self.content = tk.Frame(self.root)
        self.content.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        # Menu (Left Panel)
        self.menu_frame = tk.Frame(self.content, bg="#f1f1f1", width=200)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        #Placeholders WIP
        buttons = [
            ("Moje zadania", self.show_tasks),
            ("Kalendarz", self.placeholder),
            ("Archiwum", self.placeholder),
            ("Ustawienia", self.placeholder),
            ("Zespół", self.placeholder)
        ]
        #Hide border of buttons and apply same bg as Menu
        for text, command in buttons:
            btn = tk.Button(
                self.menu_frame,
                text=text,
                command=command,
                width=20,
                bg="#f1f1f1",
                relief="flat",
                borderwidth=0,
                activebackground="#f1f1f1",
                highlightthickness=0
            )
            btn.pack(pady=5, padx=10)


        # Body
        self.main_frame = tk.Frame(self.content, bg="#eaf6fb")  # BB with opacity
        self.main_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        # Header
        self.header_label = tk.Label(self.main_frame, text="Moje zadania", font=("Arial", 16), bg="#eaf6fb")
        self.header_label.pack(anchor="nw", padx=20, pady=(20, 10))

        # Task Holder (Body)
        self.task_box = tk.Frame(self.main_frame, bg="#ffffff")
        self.task_box.pack(padx=20, pady=10, ipadx=10, ipady=10, fill=tk.X)

        self.listbox = tk.Listbox(self.task_box, height=10, borderwidth=0, highlightthickness=0)
        self.listbox.pack(padx=10, pady=10, fill=tk.X)

        # Button "Dodaj zadanie"
        self.add_button = tk.Button(self.main_frame, text="Dodaj zadanie", command=self.add_task, bg="#81c8dd", fg="white", width=15)
        self.add_button.pack(anchor="e", padx=30, pady=10)

        # Button "Usuń zaznaczone"
        self.delete_button = tk.Button(self.main_frame, text="Usuń zaznaczone", command=self.delete_task, bg="#FAA0A0")
        self.delete_button.pack(pady=5)

    def add_task(self):
        def save_new_task():
            name = name_entry.get()
            description = description_entry.get("1.0", tk.END).strip()
            due_date = date_entry.get()
            category = category_combo.get()
            priority = priority_combo.get()

            if not name:
                messagebox.showwarning("Błąd", "Nazwa zadania jest wymagana.")
                return

            task_id = len(self.tasks) + 1
            task = Task(task_id, name, description, due_date, category, priority)
            self.tasks.append(task)
            data_manager.save_tasks(self.tasks)
            self.refresh_list()
            add_window.destroy()

        # Dragable Window
        def start_move(event):
            add_window.x = event.x
            add_window.y = event.y

        # Geometry x,y relative to window
        def do_move(event):
            x = add_window.winfo_pointerx() - add_window.x #It's fine it works somehow
            y = add_window.winfo_pointery() - add_window.y
            add_window.geometry(f"+{x}+{y}")

        add_window = tk.Toplevel(self.root)
        add_window.geometry("400x450+300+200")
        add_window.configure(bg="#eaf6fb")
        add_window.overrideredirect(1)
        add_window.attributes('-topmost', True)

        header = tk.Frame(add_window, bg="#81c8dd", height=40)
        header.pack(fill=tk.X)

        header.bind("<Button-1>", start_move)
        header.bind("<B1-Motion>", do_move)

        header_label = tk.Label(header, text="Dodawanie zadania", bg="#81c8dd", fg="white", font=("Arial", 12, "bold"))
        header_label.pack(side=tk.LEFT, padx=10, pady=5)

        close_btn = tk.Button(header, text="X", bg="#81c8dd", fg="white", borderwidth=0, font=("Arial", 12), command=add_window.destroy)
        close_btn.pack(side=tk.RIGHT, padx=10, pady=5)

        # Form (Center)
        form_frame = tk.Frame(add_window, bg="#eaf6fb")
        form_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        tk.Label(form_frame, text="Nazwa:", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
        name_entry = tk.Entry(form_frame, width=40)
        name_entry.pack(pady=3)

        tk.Label(form_frame, text="Opis:", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
        description_entry = tk.Text(form_frame, width=40, height=3)
        description_entry.pack(pady=3)

        tk.Label(form_frame, text="Termin (YYYY-MM-DD):", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
        date_entry = tk.Entry(form_frame, width=40)
        date_entry.pack(pady=3)

        tk.Label(form_frame, text="Kategoria:", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
        category_combo = ttk.Combobox(form_frame, values=["Szkoła", "Praca", "Dom", "Inne"], state="readonly", width=37)
        category_combo.set("Szkoła")
        category_combo.pack(pady=3)

        tk.Label(form_frame, text="Priorytet:", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
        priority_combo = ttk.Combobox(form_frame, values=["Niski", "Średni", "Wysoki"], state="readonly", width=37)
        priority_combo.set("Średni")
        priority_combo.pack(pady=3)

        # Button Bottom "Dodaj zadanie"
        submit_frame = tk.Frame(add_window, bg="#eaf6fb")
        submit_frame.pack(fill=tk.X, pady=10)

        submit_btn = tk.Button(submit_frame, text="Dodaj zadanie", command=save_new_task, bg="#81c8dd", fg="white", width=20)
        submit_btn.pack(pady=5)



    # Task Delete F
    def delete_task(self):
        selected = self.listbox.curselection()
        if not selected:
            messagebox.showwarning("Brak wyboru", "Wybierz zadanie do usunięcia.")
            return

        index = selected[0]
        del self.tasks[index]
        data_manager.save_tasks(self.tasks)
        self.refresh_list()

    def refresh_list(self):
        self.tasks = utils.sort_tasks_by_date(self.tasks)
        self.listbox.delete(0, tk.END)
        for task in self.tasks:
            self.listbox.insert(tk.END, f"{task.name} | {task.due_date} | {task.category} | Priorytet: {task.priority}")

    #Header text
    def show_tasks(self):
        self.header_label.config(text="Moje zadania")

    def placeholder(self):
        messagebox.showinfo("Informacja", "Funkcja w trakcie budowy")
