import tkinter as tk
from tkinter import ttk, messagebox
import os
from quarantine_manager import restore_file

QUARANTINE_DIR = "quarantine"


class QuarantineWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.title("Karantina")
        self.geometry("600x400")
        self.resizable(False, False)

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True, padx=10, pady=10)

        self.tree = ttk.Treeview(
            container,
            columns=("file",),
            show="headings",
            height=10
        )
        self.tree.heading("file", text="Karantinadaki Dosyalar")
        self.tree.pack(fill="x", pady=(0, 10))

        btn_frame = ttk.Frame(container)
        btn_frame.pack(fill="x")

        ttk.Button(
            btn_frame,
            text="♻️ Geri Yükle",
            command=self.restore_selected
        ).pack(side="left", padx=5)

        ttk.Button(
            btn_frame,
            text="🗑️ Sil",
            command=self.delete_selected
        ).pack(side="left", padx=5)

        self.load_files()

    def load_files(self):
        self.tree.delete(*self.tree.get_children())

        if not os.path.exists(QUARANTINE_DIR):
            return

        # SADECE JSON DOSYALARINI LİSTELE
        for f in os.listdir(QUARANTINE_DIR):
            if f.endswith(".json"):
                self.tree.insert("", "end", values=(f,))

    def get_selected(self):
        item = self.tree.focus()
        if not item:
            return None
        return self.tree.item(item, "values")[0]

    def restore_selected(self):
        selected = self.get_selected()
        if not selected:
            return

        metadata_path = os.path.join(QUARANTINE_DIR, selected)

        # 🔥 SADECE 1 PARAMETRE
        success, result = restore_file(metadata_path)

        if success:
            messagebox.showinfo("Restore", f"Geri yüklendi:\n{result}")
            self.load_files()
        else:
            messagebox.showerror("Hata", result)

    def delete_selected(self):
        selected = self.get_selected()
        if not selected:
            return

        metadata_path = os.path.join(QUARANTINE_DIR, selected)

        if messagebox.askyesno("Onay", "Dosya kalıcı olarak silinsin mi?"):
            try:
                import json

                # Metadata oku
                with open(metadata_path, "r", encoding="utf-8") as f:
                    metadata = json.load(f)

                # Karantinadaki gerçek dosyanın yolu
                quarantined_path = metadata.get("quarantined_path")

                # Gerçek karantina dosyasını sil
                if quarantined_path and os.path.exists(quarantined_path):
                    os.remove(quarantined_path)

                # JSON metadata dosyasını sil
                if os.path.exists(metadata_path):
                    os.remove(metadata_path)

                messagebox.showinfo("Başarılı", "Dosya karantinadan kalıcı olarak silindi.")
                self.load_files()

            except Exception as e:
                messagebox.showerror("Hata", str(e))
