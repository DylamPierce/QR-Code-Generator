import qrcode
import tkinter as tk
import json
import os
from tkinter import filedialog, messagebox


# ---------------- SETTINGS ---------------- #
SETTINGS_FILE = os.path.join(os.path.expanduser("~"), "qr_settings.json")

DEFAULT_SETTINGS = {
    "theme": "Light",
    "window_size": "600x300",
    "last_url": "",
    "default_folder": "",
    "auto_focus": True
}

def load_settings():
    if os.path.exists(SETTINGS_FILE):
        with open(SETTINGS_FILE, "r") as f:
            data = json.load(f)
            return {**DEFAULT_SETTINGS, **data}
    return DEFAULT_SETTINGS.copy()

def save_settings():
    global settings

    settings["theme"] = current_theme

    if root:
        settings["window_size"] = root.geometry()
    if entry:
        settings["last_url"] = entry.get()

    with open(SETTINGS_FILE, "w") as f:
        json.dump(settings, f, indent=4)


# ---------------- THEMES ---------------- #
themes = {
    "Light": {"bg": "white", "fg": "black", "entry_bg": "white", "entry_fg": "black"},
    "Dark": {"bg": "#1e1e1e", "fg": "white", "entry_bg": "#2e2e2e", "entry_fg": "white"},
    "Red": {"bg": "#a33434", "fg": "white", "entry_bg": "#ffe6e6", "entry_fg": "black"},
    "Blue": {"bg": "#44719e", "fg": "white", "entry_bg": "#e6f2ff", "entry_fg": "black"},
    "Yellow": {"bg": "#bea540", "fg": "black", "entry_bg": "#fff8cc", "entry_fg": "black"},
    "Green": {"bg": "#4dce78", "fg": "black", "entry_bg": "#e6fff0", "entry_fg": "black"},
    "Purple": {"bg": "#9252d3", "fg": "white", "entry_bg": "#f2e6ff", "entry_fg": "black"},
    "Brown": {"bg": "#97644d", "fg": "white", "entry_bg": "#f3e6df", "entry_fg": "black"}
}


# ---------------- APP STATE ---------------- #
settings = load_settings()
current_theme = settings["theme"]


# ---------------- QR FUNCTION ---------------- #
def generate_qr():
    try:
        url = entry.get().strip()

        if not url:
            messagebox.showerror("Error", "Please enter a URL")
            return

        img = qrcode.make(url)

        file_path = filedialog.asksaveasfilename(
            defaultextension=".png",
            filetypes=[("PNG Image", "*.png")],
            title="Save QR Code As"
        )

        if file_path:
            img.save(file_path)
            messagebox.showinfo("Success", "QR Code saved successfully!")
    except Exception as e:
        messagebox.showerror("Error", str(e))

def on_enter(event):
    generate_qr()


# ---------------- THEME SYSTEM ---------------- #
def apply_theme():
    theme = themes[current_theme]

    root.configure(bg=theme["bg"])
    top_frame.configure(bg=theme["bg"])

    label.configure(bg=theme["bg"], fg=theme["fg"])

    entry.configure(
        bg=theme["entry_bg"],
        fg=theme["entry_fg"],
        insertbackground=theme["entry_fg"],
        selectbackground="#cccccc",
        selectforeground="black"
    )

    button.configure(
        bg=theme["fg"],
        fg=theme["bg"],
        activebackground=theme["fg"],
        activeforeground=theme["bg"]
    )

    gear_button.configure(
        bg=theme["bg"],
        fg=theme["fg"],
        activebackground=theme["bg"],
        activeforeground=theme["fg"]
    )

def set_theme(theme_name):
    global current_theme
    current_theme = theme_name
    apply_theme()
    apply_settings_theme()
    save_settings()


# ---------------- SETTINGS POPUP ---------------- #
settings_window = None

def open_settings():
    global settings_window

    settings_window = tk.Toplevel(root)
    settings_window.title("Settings")
    settings_window.geometry("250x300")

    apply_settings_theme()

    tk.Label(
        settings_window,
        text="Choose Theme:"
    ).pack(pady=10)

    for name in themes.keys():
        tk.Button(
            settings_window,
            text=name,
            command=lambda n=name: set_theme(n)
        ).pack(pady=3, fill="x")

def apply_settings_theme():
    if settings_window is None:
        return

    theme = themes[current_theme]

    settings_window.configure(bg=theme["bg"])

    for widget in settings_window.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(
                bg=theme["bg"],
                fg=theme["fg"]
            )

        elif isinstance(widget, tk.Button):
            button_bg = "white"
            button_fg = theme["bg"]

            if current_theme == "Light":
               button_fg = "black"

            widget.configure(
                bg=button_bg,
                fg=button_fg,
                activebackground="#f0f0f0",
                activeforeground=button_fg
            )


# ---------------- UI BUILD ---------------- #
def build_ui():
    global root, top_frame, gear_button, label, entry, button

    root = tk.Tk()
    root.title("QR Code Generator")
    root.geometry(settings.get("window_size", "600x300"))

    top_frame = tk.Frame(root)
    top_frame.pack(fill="x")

    gear_button = tk.Button(top_frame, text="⚙", font=("Arial", 14), bd=0, command=open_settings)
    gear_button.pack(side="right", padx=10, pady=5)

    label = tk.Label(root, text="Enter URL:")
    label.pack(pady=10)

    entry = tk.Entry(root, width=60)
    entry.pack(pady=10)
    entry.bind("<Return>", on_enter)
    entry.insert(0, settings.get("last_url", ""))
    entry.select_range(0, tk.END)
    entry.focus()

    button = tk.Button(root, text="Generate QR Code", command=generate_qr)
    button.pack(pady=20)

    apply_theme()

    root.mainloop()

# ---------------- START APP ---------------- #
build_ui()