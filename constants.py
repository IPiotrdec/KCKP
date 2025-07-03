import tkinter as tk
from tkinter import messagebox
import tkinter.ttk as ttk
from task import Task
import utils
import data_manager

def add_task_window(app):
    def save_new_task():
        name = name_entry.get()
        description = description_entry.get("1.0", tk.END).strip()
        due_date = date_entry.get()
        category = category_combo.get()
        priority = priority_combo.get()

        if not name:
            messagebox.showwarning("Błąd", "Nazwa zadania jest wymagana.")
            return

        app.tasks = utils.add_task(app.tasks, name, description, due_date, category, priority)
        app.refresh_ui()
        add_window.destroy()

    def start_move(event):          #StackOverflow code purpose only for one window to be draggable without task bar
        add_window.startX = event.x
        add_window.startY = event.y

    def do_move(event):
        x = add_window.winfo_pointerx() - add_window.startX  #It's working somehow
        y = add_window.winfo_pointery() - add_window.startY
        add_window.geometry(f"+{x}+{y}")

    add_window = tk.Toplevel(app.root)
    add_window.geometry("400x450+300+200")
    add_window.configure(bg="#eaf6fb")
    add_window.overrideredirect(1)
    add_window.attributes('-topmost', True)

    header = tk.Frame(add_window, bg="#81c8dd", height=40)
    header.pack(fill=tk.X)
    header.bind("<Button-1>", start_move)
    header.bind("<B1-Motion>", do_move)

    tk.Label(header, text="Dodawanie zadania", bg="#81c8dd", fg="white", font=("Arial", 12, "bold")).pack(side=tk.LEFT, padx=10, pady=5)
    tk.Button(header, text="X", bg="#81c8dd", fg="white", borderwidth=0, font=("Arial", 12), command=add_window.destroy).pack(side=tk.RIGHT, padx=10, pady=5)

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
    default_tags = ["Szkoła", "Praca", "Dom", "Inne"]
    category_values = list(dict.fromkeys(default_tags + app.tags))
    category_combo = ttk.Combobox(form_frame, values=category_values, state="readonly", width=37)
    category_combo.set("Szkoła")
    category_combo.pack(pady=3)

    tk.Label(form_frame, text="Priorytet:", bg="#eaf6fb").pack(anchor="w", pady=(5, 0))
    priority_combo = ttk.Combobox(form_frame, values=["Niski", "Średni", "Wysoki"], state="readonly", width=37)
    priority_combo.set("Średni")
    priority_combo.pack(pady=3)

    submit_frame = tk.Frame(add_window, bg="#eaf6fb")
    submit_frame.pack(fill=tk.X, pady=10)

    tk.Button(submit_frame, text="Dodaj zadanie", command=save_new_task, bg="#81c8dd", fg="white", width=20).pack(pady=5)
