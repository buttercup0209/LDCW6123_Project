import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import os
import uuid
from datetime import datetime
import shutil

DATA_FILE = "lost_found.json"

# Load existing data
def load_data():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return []

# Save data
def save_data(data):
    with open(DATA_FILE, "w") as f:
        json.dump(data, f, indent=4)

#Main app window
root = tk.Tk()
root.title("Lost & Found System")
root.geometry("400x300")

#Label
title_label = tk.Label(root, text="Lost & Found Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=50)

root.mainloop()
