# 🔍 Log Analyzer (Zen UI)

A lightweight desktop app built with Python and Tkinter that allows users to analyze log files (e.g. charger offline / router offline / online events) within a specified date range — all with a calming Zen-style interface and splash screen.

---

## 📦 Features

- 📂 Import `.txt` log files (Thai/English logs)
- 🗓 Select start & end dates via calendar
- 🔌 Auto-detect keywords: `charger offline`, `router offline`, and `online`
- 📊 View results in a table, grouped by day
- 🧘‍♀️ Zen-inspired splash screen and minimal UI
- ✅ Bundled into `.exe` — no need to install Python

---

## 🚀 How to Use

### ✅ Windows `.exe` version

> File: `dist/main.exe`

1. Double-click `main.exe`
2. Splash screen appears briefly
3. Use the date picker to choose a range
4. Click `📂 Import Log File` to select your log `.txt`
5. View the summarized table by day, including:
   - Charger Offline
   - Router Offline
   - Online (fix)

---

## 🛠 Developer Setup (Python)

> Python 3.10+ required

```bash
pip install -r requirements.txt
python main.py
