import tkinter as tk
from tkinter import ttk
import os

LOG_FILE = "scan_report.log"


class LogWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Tarama Logları")
        self.geometry("800x400")

        text = tk.Text(
            self,
            bg="#1e1e1e",
            fg="white",
            font=("Consolas", 10)
        )
        text.pack(fill="both", expand=True)

        if os.path.exists(LOG_FILE):
            with open(LOG_FILE, "r", encoding="utf-8", errors="ignore") as f:
                text.insert("1.0", f.read())
        else:
            text.insert("1.0", "Log dosyası bulunamadı.")

        text.config(state="disabled")
