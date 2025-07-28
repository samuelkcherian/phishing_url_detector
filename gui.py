# gui.py (polished cybersecurity theme)
import tkinter as tk
from tkinter import ttk, messagebox
import pyperclip
import joblib
from features import extract_features
import os
import sys

# Load model path (for .exe compatibility)
base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
model_path = os.path.join(base_path, 'model.pkl')
model = joblib.load(model_path)

# Theme colors
DARK_BG = "#0f111a"
TEXT_COLOR = "#e5e5e5"
ACCENT = "#00ff88"
ENTRY_BG = "#1a1d2e"
RESULT_GREEN = "#55ff55"
RESULT_RED = "#ff4d4d"
LOG_BG = "#11131a"
LOG_FG = "#0ef6ff"

# Main window
root = tk.Tk()
root.title("Phishing URL Detector")
root.geometry("680x520")
root.configure(bg=DARK_BG)
root.resizable(False, False)

# --- Styles ---
style = ttk.Style()
style.theme_use('clam')
style.configure("TButton", foreground="black", background=ACCENT, font=("Segoe UI", 10), padding=6)
style.map("TButton", background=[("active", "#00cc6a")])

# --- Header ---
header = tk.Label(root, text="🛡️ Phishing URL Detector", font=("Segoe UI", 18, "bold"),
                  fg=ACCENT, bg=DARK_BG)
header.pack(pady=15)

# --- URL Entry ---
entry = tk.Entry(root, font=("Segoe UI", 12), width=52,
                 bg=ENTRY_BG, fg=TEXT_COLOR, insertbackground=TEXT_COLOR,
                 relief="flat")
entry.pack(pady=8)
entry.focus()

# --- Button Frame ---
btn_frame = tk.Frame(root, bg=DARK_BG)
btn_frame.pack(pady=8)

ttk.Button(btn_frame, text="Check", command=lambda: check_url()).grid(row=0, column=0, padx=6)
ttk.Button(btn_frame, text="Paste", command=lambda: paste_clipboard()).grid(row=0, column=1, padx=6)
ttk.Button(btn_frame, text="Clear", command=lambda: clear_all()).grid(row=0, column=2, padx=6)

# --- Result Label ---
result_label = tk.Label(root, text="", font=("Segoe UI", 13, "bold"),
                        fg=TEXT_COLOR, bg=DARK_BG)
result_label.pack(pady=12)

# --- History Title ---
tk.Label(root, text="📜 Scan History", font=("Segoe UI", 11, "bold"),
         fg=ACCENT, bg=DARK_BG).pack()

# --- History Frame ---
log_frame = tk.Frame(root, bg=DARK_BG)
log_frame.pack(pady=5)

log_scroll = tk.Scrollbar(log_frame)
log_scroll.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(log_frame, font=("Consolas", 10), height=12, width=78,
                   yscrollcommand=log_scroll.set,
                   bg=LOG_BG, fg=LOG_FG, insertbackground=LOG_FG,
                   relief="flat", wrap="word")
log_text.pack()
log_scroll.config(command=log_text.yview)

# --- Functionality ---
def check_url():
    url = entry.get().strip()
    if not url:
        messagebox.showwarning("Input Error", "Please enter a URL.")
        return
    if not url.startswith("http"):
        url = "http://" + url

    features = extract_features(url)
    prediction = model.predict([features])[0]

    if prediction == 1:
        verdict = "⚠️ PHISHING SITE DETECTED!"
        result_label.config(text=verdict, fg=RESULT_RED)
    else:
        verdict = "✅ URL Seems Legitimate"
        result_label.config(text=verdict, fg=RESULT_GREEN)

    log_text.insert(tk.END, f"🔍 {url}\n→ {verdict}\n\n")
    log_text.see(tk.END)

def clear_all():
    entry.delete(0, tk.END)
    result_label.config(text="", fg=TEXT_COLOR)

def paste_clipboard():
    pasted = pyperclip.paste()
    entry.delete(0, tk.END)
    entry.insert(0, pasted)

# --- Start App ---
root.mainloop()
