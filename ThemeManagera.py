import tkinter as tk
from tkcalendar import Calendar
import ThemeManagera as theme
import constants

DEFAULT_ACCENT = "#87d7f8"          # babyblue
DARK_ACCENT    = "#00a0d0"          # darker bb for darkmode

from tkcalendar import Calendar as TkCalendar

def _paint(widget, bg, fg, btn_bg):
    """Rekurencyjnie koloruje drzewo widgetów; unika opcji,
    których dany typ nie obsługuje."""

    # ---------- sam widget ----------
    if isinstance(widget, TkCalendar):
        # kalendarz ma własne nazwy atrybutów
        widget.configure(
            background=bg,
            disabledbackground=bg,
            selectbackground=btn_bg,
            foreground=fg,
            headersbackground=btn_bg,
            headersforeground=fg
        )
    elif isinstance(widget, (tk.Frame, tk.Canvas)):
        widget.configure(bg=bg)                     # tylko tło
    elif isinstance(widget, tk.Button):
        widget.configure(bg=btn_bg, fg=fg,
                         activebackground=btn_bg,
                         activeforeground=fg)
    elif isinstance(widget, (tk.Label, tk.Checkbutton,
                             tk.Entry, tk.Listbox)):
        widget.configure(bg=bg, fg=fg)
        if isinstance(widget, tk.Checkbutton):
            widget.configure(selectcolor=bg)
    else:
        # próbuj, a jak nie działa – pomiń
        try:
            widget.configure(bg=bg, fg=fg)
        except tk.TclError:
            try:
                widget.configure(bg=bg)
            except tk.TclError:
                pass

    # ---------- dzieci ----------
    for child in widget.winfo_children():
        _paint(child, bg, fg, btn_bg)


def apply_theme(app):
    if app.dark_mode:
        bg, fg, btn_bg, menu_bg = "#1e1e1e", "#dddddd", "#444444", "#1a1a1a"
    else:
        bg, fg, btn_bg, menu_bg = "#eaf6fb", "black", "#81c8dd", "#f1f1f1"

    # bg of main containers
    app.root.configure(bg=bg)
    app.header_frame.configure(bg=btn_bg)
    app.header_label.configure(bg=bg, fg=fg)

    app.main_frame.configure(bg=bg)
    app.menu_frame.configure(bg=menu_bg)
    app.content_frame.configure(bg=bg)

    # Color all
    _paint(app.menu_frame, menu_bg, fg, menu_bg)
    _paint(app.content_frame, bg, fg, btn_bg)
    app.theme_bg      = bg
    app.theme_fg      = fg
    app.theme_btn_bg  = btn_bg
    app.theme_menu_bg = menu_bg

    accent = DEFAULT_ACCENT if not app.dark_mode else DARK_ACCENT
    app.logo_label.configure(bg=accent)


def show_tasks(app):
    # Clean View
    if hasattr(app, "settings_frame"):
        app.settings_frame.destroy()
    if app.calendar_container:
        app.calendar_container.destroy()

    app.current_view = "tasks"
    app.header_label.config(text="Moje zadania")
    app.task_box.pack(padx=20, pady=10, ipadx=10, ipady=10,
                      fill=tk.BOTH, expand=True)

    for w in app.button_frame.winfo_children():
        w.destroy()

    # buttons
    pastel = [
        ("Dodaj zadanie",         "#a7d9f5", lambda: constants.add_task_window(app)),
        ("Usuń zaznaczone",       "#f5a7a7", app.remove_selected_task),
        ("Oznacz jako ukończone", "#c8f5a7", app.complete_selected_task)
    ]
    for col, (txt, bg, cmd) in enumerate(pastel):
        tk.Button(app.button_frame, text=txt, command=cmd,
                  bg=bg, fg="black").grid(row=0, column=col, padx=5)

    # Allign Left
    app.button_frame.pack(pady=10, anchor="e", padx=20)

    # List and Colors
    app.refresh_ui()          # refresh
    apply_theme(app)

    #reverse white/dark text
    for btn in app.button_frame.winfo_children():
        btn.configure(fg="white" if app.dark_mode else "black")
    app.refresh_ui()
    apply_theme(app)                         #<- dont move

    #Buttons BG
    pastel = ["#a7d9f5", "#f5a7a7", "#c8f5a7"]
    for btn, bg in zip(app.button_frame.winfo_children(), pastel):
        btn.configure(
            bg=bg,
            fg=("white" if app.dark_mode else "black"),
            activebackground=bg,
            activeforeground=("white" if app.dark_mode else "black")
        )




def show_archive(app):

    if hasattr(app, "settings_frame"):
        app.settings_frame.destroy()
    if app.calendar_container:
        app.calendar_container.destroy()

    app.current_view = "archive"
    app.selected_date = None
    app.header_label.config(text="Archiwum")


    app.task_box.pack(padx=20, pady=10, ipadx=10, ipady=10,
                      fill=tk.BOTH, expand=True)

    # del button children
    for w in app.button_frame.winfo_children():
        w.destroy()

    del_btn = tk.Button(
        app.button_frame,
        text="Usuń zaznaczone",
        command=app.remove_selected_task,
        bg="#f5a7a7",                 # pink
        fg="black"
    )
    del_btn.pack()
    app.button_frame.pack(pady=10, anchor="e", padx=30)

    app.refresh_ui()                 # # refresh list
    apply_theme(app)                 # global paint

    # reverse colors
    del_btn.configure(
        bg="#f5a7a7",
        activebackground="#f5a7a7",
        fg=("white" if app.dark_mode else "black"),
        activeforeground=("white" if app.dark_mode else "black")
    )




def show_calendar(app):
    if hasattr(app, "settings_frame"):
        app.settings_frame.destroy()

    app.current_view = "calendar"
    app.selected_date = None
    app.header_label.config(text="Kalendarz")

    if app.calendar_container:
        app.calendar_container.destroy()

    app.task_box.pack_forget()
    app.button_frame.pack_forget()

    # container
    app.calendar_container = tk.Frame(app.content_frame, bg=app.theme_bg)
    app.calendar_container.pack(fill=tk.BOTH, expand=True)

    # callendar
    app.calendar_widget = Calendar(
        app.calendar_container,
        selectmode='day',
        date_pattern='yyyy-mm-dd',
        font=("Arial", 15),
        background=app.theme_bg,
        disabledbackground=app.theme_bg,
        selectbackground=app.theme_btn_bg,
        foreground=app.theme_fg,
        headersbackground=app.theme_btn_bg,
        headersforeground=app.theme_fg
    )
    app.calendar_widget.place(relx=0.5, rely=0.3, anchor="center")
    app.calendar_widget.bind("<<CalendarSelected>>",
                             lambda e: select_calendar_date(app))

    # task list
    app.tasks_frame = tk.Frame(app.calendar_container, bg=app.theme_bg)
    app.tasks_frame.place(relx=0.5, rely=0.6, anchor="n")

    app.refresh_ui()
    apply_theme(app)          #has to be in every function that changes screen view to fix colors



def select_calendar_date(app, event=None):
    from tkinter import messagebox

    app.selected_date = app.calendar_widget.get_date()

    # clear previous list
    for w in app.tasks_frame.winfo_children():
        w.destroy()

    # all task from "this" day
    day_tasks = [t for t in app.tasks if t.due_date == app.selected_date]

    if not day_tasks:
        tk.Label(app.tasks_frame, text="— Brak zadań —",
                 fg="gray", bg=app.theme_bg,
                 font=("Arial", 12, "italic")).pack()
        return

    # Show Task in label
    for task in day_tasks:
        status = "✅" if task.completed else "🕒"
        lbl = tk.Label(app.tasks_frame,
                       text=f"{status} {task.name}",
                       anchor="w",
                       bg=app.theme_bg,
                       font=("Arial", 12))
        lbl.pack(fill=tk.X, padx=10, pady=2)
        lbl.bind("<Button-1>",
                 lambda e, t=task: messagebox.showinfo(
                     t.name,
                     f"{t.description}\n\nTermin: {t.due_date}"
                     f"\nKategoria: {t.category}\nPriorytet: {t.priority}"))

def placeholder(app):
    from tkinter import messagebox
    messagebox.showinfo("Informacja", "Funkcja w trakcie budowy")


