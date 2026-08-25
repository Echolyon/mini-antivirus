import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from scanner import scan_directory
from ui.quarantine_window import QuarantineWindow
from ui.log_window import LogWindow
import threading


class MiniAVApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("MiniAV")
        self.geometry("900x520")
        self.resizable(False, False)

        self._setup_style()
        self._build_ui()

    # 🎨 STYLE
    def _setup_style(self):
        style = ttk.Style(self)
        style.theme_use("default")

        style.configure(
            "Treeview",
            background="#1e1e1e",
            foreground="white",
            rowheight=24,
            fieldbackground="#1e1e1e",
            font=("Segoe UI", 10)
        )

        style.configure(
            "Treeview.Heading",
            background="#2d2d2d",
            foreground="white",
            font=("Segoe UI", 10, "bold")
        )

        style.map(
            "Treeview",
            background=[("selected", "#007acc")]
        )

        style.configure(
            "Action.TButton",
            font=("Segoe UI", 10, "bold"),
            padding=6
        )

    # 🧱 UI
    def _build_ui(self):
        top = ttk.Frame(self)
        top.pack(fill="x", padx=10, pady=10)

        ttk.Button(
            top,
            text="📂 Klasör Tara",
            style="Action.TButton",
            command=self.choose_folder
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="🧪 Karantina",
            style="Action.TButton",
            command=self.open_quarantine
        ).pack(side="left", padx=5)

        ttk.Button(
            top,
            text="📄 Loglar",
            style="Action.TButton",
            command=lambda: LogWindow(self)
        ).pack(side="left", padx=5)

        columns = ("name", "status", "score")
        self.tree = ttk.Treeview(
            self,
            columns=columns,
            show="headings",
            height=18
        )

        self.tree.heading("name", text="Dosya")
        self.tree.heading("status", text="Durum")
        self.tree.heading("score", text="Risk")

        self.tree.column("name", width=520)
        self.tree.column("status", width=140, anchor="center")
        self.tree.column("score", width=80, anchor="center")

        self.tree.pack(fill="both", expand=True, padx=10)

        # ✅ DOĞRU TAG İSİMLERİ
        self.tree.tag_configure("MALWARE", background="#5c1a1a")
        self.tree.tag_configure("SUSPICIOUS", background="#5c3b1a")
        self.tree.tag_configure("CLEAN", background="#1a5c2e")

        self.tree.bind("<Double-1>", self.show_details)

    # 📂 KLASÖR SEÇ
    def choose_folder(self):
        path = filedialog.askdirectory()
        if not path:
            return

        self.tree.delete(*self.tree.get_children())

        threading.Thread(
            target=self.scan_thread,
            args=(path,),
            daemon=True
        ).start()

    # 🔄 THREAD (UI GÜVENLİ)
    def scan_thread(self, path):
        results = scan_directory(path)

        # UI güncellemesini ana threade bırakıyoruz
        self.after(0, self.fill_tree, results)

    # 🌳 TREE DOLDUR
    def fill_tree(self, results):
        status_map = {
            "MALWARE": "ZARARLI",
            "SUSPICIOUS": "ŞÜPHELİ",
            "CLEAN": "TEMİZ"
        }

        for r in results:
            raw_status = r["status"]
            display_status = status_map.get(raw_status, raw_status)

            self.tree.insert(
                "",
                "end",
                values=(
                    r["name"],
                    display_status,
                    r.get("risk_score", 0)
                ),
                tags=(raw_status,)
            )


    # 📦 KARANTİNA
    def open_quarantine(self):
        QuarantineWindow(self)

    # 🔎 DETAY
    def show_details(self, event):
        item = self.tree.focus()
        if not item:
            return

        values = self.tree.item(item, "values")

        messagebox.showinfo(
            "Dosya Detayı",
            f"Dosya: {values[0]}\nDurum: {values[1]}\nRisk Skoru: {values[2]}"
        )