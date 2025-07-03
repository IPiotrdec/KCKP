import tkinter as tk
from tkinter import messagebox
import utils
import ThemeManagera as theme

def show_settings(app):
    #Clean View
    if app.calendar_container:
        app.calendar_container.destroy()
    app.task_box.pack_forget()
    app.button_frame.pack_forget()
    if hasattr(app, "settings_frame"):
        app.settings_frame.destroy()

    app.current_view = "settings"
    app.header_label.config(text="Ustawienia")

    #Main Frame
    app.settings_frame = tk.Frame(app.content_frame, bg=app.theme_bg)
    app.settings_frame.place(relx=0.5, rely=0.3, anchor="n")

    # Add Tags
    tk.Label(app.settings_frame, text="Dodaj własny tag:",
             bg=app.theme_bg, fg=app.theme_fg).pack(pady=(10, 0))
    app.tag_entry = tk.Entry(app.settings_frame, width=30)
    app.tag_entry.pack(pady=5)
    tk.Button(app.settings_frame, text="Dodaj tag",
              command=lambda: add_tag(app),
              bg=app.theme_btn_bg, fg=app.theme_fg).pack()

    # Reset
    app.reset_button = tk.Button(
        app.settings_frame, text="Resetuj wszystko",
        bg="#cc3333", fg="white", width=20,
        command=lambda: confirm_reset(app)
    )
    app.reset_button.pack(pady=20)

    # DarkMode
    app.dark_mode_var = tk.BooleanVar(value=app.dark_mode)
    tk.Checkbutton(
        app.settings_frame, text="Tryb ciemny",
        variable=app.dark_mode_var,
        command=lambda: toggle_dark_mode(app),
        bg=app.theme_bg, fg=app.theme_fg,
        selectcolor=app.theme_bg
    ).pack(pady=10)

    theme.apply_theme(app)     #Repaint


def add_tag(app):
    tag = app.tag_entry.get().strip()
    if tag and tag not in app.tags:
        app.tags.append(tag)
        messagebox.showinfo("Dodano tag", f"Tag '{tag}' został dodany.")
        app.tag_entry.delete(0, tk.END)
    elif tag in app.tags:
        messagebox.showwarning("Tag istnieje", "Taki tag już istnieje.")

def confirm_reset(app):
    if not app.reset_confirm:
        app.reset_button.config(text="Na pewno?", bg="#990000")
        app.reset_confirm = True
    else:
        app.tasks = utils.reset_all_tasks()
        app.refresh_ui()
        app.reset_confirm = False
        app.reset_button.config(text="Resetuj wszystko", bg="#cc3333")

def toggle_dark_mode(app):
    app.dark_mode = app.dark_mode_var.get()
    from ThemeManagera import apply_theme
    apply_theme(app)


