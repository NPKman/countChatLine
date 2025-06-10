import tkinter as tk
from tkinter import filedialog, messagebox, ttk
from tkcalendar import DateEntry
from datetime import datetime
from collections import defaultdict
from PIL import Image, ImageTk
import re

# ==== Patterns สำหรับตรวจ log ====
date_line_pattern = re.compile(r"^(\d{4})\.(\d{2})\.(\d{2})")
charger_offline_pattern = re.compile(r"charger\s+offline", re.IGNORECASE)
router_offline_pattern = re.compile(r"router\s+offline", re.IGNORECASE)
online_pattern = re.compile(r"\bonline\b", re.IGNORECASE)

# ==== Main Window ====
root = tk.Tk()
root.title("Log Analyzer - Glass UI")
root.geometry("760x580")
root.configure(bg="#b0d8ff")  # พื้นหลังฟ้าอ่อน (ไม่โปร่งใส)

# ==== Load logo ====
try:
    logo = Image.open("logo.png").resize((60, 60))
    logo_img = ImageTk.PhotoImage(logo)
except Exception:
    logo_img = None

# ==== Style ====
style = ttk.Style()
style.theme_use("clam")
style.configure("TLabel", font=("Segoe UI", 11), background="#ffffff", foreground="#333")
style.configure("TButton", font=("Segoe UI", 11), padding=6, relief="flat")
style.map("TButton", background=[("active", "#e0f0ff")])
style.configure("Treeview", font=("Segoe UI", 10), rowheight=28, background="#ffffff", fieldbackground="#ffffff", foreground="#333")
style.configure("Treeview.Heading", font=("Segoe UI", 11, "bold"), background="#f0f0f0")

# ==== Top container ====
container = tk.Frame(root, bg="#ffffff", highlightbackground="#ddeeff", highlightthickness=1)
container.pack(pady=25, padx=30, fill=tk.X)

if logo_img:
    tk.Label(container, image=logo_img, bg="#ffffff").grid(row=0, column=0, rowspan=2, padx=(10, 20), pady=10, sticky="w")

tk.Label(container, text="Start Date:", bg="#ffffff").grid(row=0, column=1, sticky="e")
start_date = DateEntry(container, width=15, background='lightblue', foreground='black', date_pattern='yyyy.mm.dd')
start_date.set_date(datetime(2025, 5, 1))
start_date.grid(row=0, column=2, padx=5, pady=5, sticky="w")

tk.Label(container, text="End Date:", bg="#ffffff").grid(row=1, column=1, sticky="e")
end_date = DateEntry(container, width=15, background='lightblue', foreground='black', date_pattern='yyyy.mm.dd')
end_date.set_date(datetime(2025, 5, 31))
end_date.grid(row=1, column=2, padx=5, pady=5, sticky="w")

# ==== Summary ====
result_text = tk.StringVar()
result_label = tk.Label(root, textvariable=result_text, bg="#b0d8ff", font=("Consolas", 12), anchor="w", justify="left")
result_label.pack(pady=(10, 0), fill=tk.X, padx=30)

# ==== Table ====
table_frame = tk.Frame(root)
table_frame.pack(fill=tk.BOTH, expand=True, padx=30, pady=10)

tree = ttk.Treeview(table_frame, columns=("date", "charger", "router", "fix"), show="headings")
tree.heading("date", text="Date")
tree.heading("charger", text="🔌 Charger Offline")
tree.heading("router", text="📡 Router Offline")
tree.heading("fix", text="🟢 Fixed (Online)")
for col in ("date", "charger", "router", "fix"):
    tree.column(col, anchor="center", width=150)
tree.pack(fill=tk.BOTH, expand=True)

# ==== วิเคราะห์ log ====
def analyze_log_file(filepath, start_date_obj, end_date_obj):
    log_data = defaultdict(lambda: {"charger_offline": 0, "router_offline": 0, "fix": 0})
    waiting_fix = 0
    current_date = None
    within_range = False

    try:
        with open(filepath, "r", encoding="utf-8") as file:
            for line in file:
                line = line.strip()

                match = date_line_pattern.match(line)
                if match:
                    current_date = datetime.strptime(".".join(match.groups()), "%Y.%m.%d")
                    within_range = start_date_obj <= current_date.date() <= end_date_obj
                    continue

                if not within_range or not line:
                    continue

                day_str = current_date.strftime("%Y-%m-%d")

                if charger_offline_pattern.search(line):
                    log_data[day_str]["charger_offline"] += 1
                    waiting_fix += 1
                elif router_offline_pattern.search(line):
                    log_data[day_str]["router_offline"] += 1
                elif online_pattern.search(line):
                    if waiting_fix > 0:
                        log_data[day_str]["fix"] += 1
                        waiting_fix -= 1

        # ล้างตาราง
        for item in tree.get_children():
            tree.delete(item)

        total_charger, total_router, total_fix = 0, 0, 0
        for date in sorted(log_data):
            c = log_data[date]["charger_offline"]
            r = log_data[date]["router_offline"]
            f = log_data[date]["fix"]
            tree.insert("", "end", values=(date, c, r, f))
            total_charger += c
            total_router += r
            total_fix += f

        result_text.set(
            f"📆 From {start_date_obj} to {end_date_obj}\n"
            f"🔌 Charger Offline: {total_charger}   📡 Router Offline: {total_router}   🟢 Fixed: {total_fix}"
        )

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read log:\n{e}")

# ==== ปุ่ม Import ====
def import_file():
    file = filedialog.askopenfilename(title="Select Log File", filetypes=[("Text files", "*.txt")])
    if file:
        analyze_log_file(file, start_date.get_date(), end_date.get_date())

import_btn = ttk.Button(container, text="📂 Import Log File", command=import_file)
import_btn.grid(row=1, column=3, padx=10, sticky="w")

# ==== Footer ====
tk.Label(root, text="Glass UI 💠 for Log Monitoring", bg="#b0d8ff", fg="#444", font=("Segoe UI", 9)).pack(side="bottom", pady=5)

root.mainloop()
