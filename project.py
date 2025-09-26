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

# Add new item
def add_item():
    def save_item():
        item = {
            "name": entry_name.get(),
            "description": entry_desc.get(),
            "poster": entry_poster.get(),
            "contact": entry_contact.get(),
            "password": entry_pass.get(),
            "status": "Open"
        }
        
        if not item["name"] or not item["poster"] or not item["password"]:
            messagebox.showerror("Error", "Name, Posted By, and Password are required.")
            return
            
        data.append(item)
        save_data(data)
        messagebox.showinfo("Success", "Item added successfully!")
        add_win.destroy()

    add_win = tk.Toplevel(root)
    add_win.title("Add Lost/Found Item")
    add_win.geometry("400x350")

    # Item Name
    tk.Label(add_win, text="Item Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(add_win, width=30)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    # Description
    tk.Label(add_win, text="Description:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_desc = tk.Entry(add_win, width=30)
    entry_desc.grid(row=1, column=1, padx=10, pady=5)

    # Posted By
    tk.Label(add_win, text="Posted By:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    entry_poster = tk.Entry(add_win, width=30)
    entry_poster.grid(row=2, column=1, padx=10, pady=5)

    # Contact
    tk.Label(add_win, text="Contact:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_contact = tk.Entry(add_win, width=30)
    entry_contact.grid(row=3, column=1, padx=10, pady=5)

    # Password
    tk.Label(add_win, text="Password:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_pass = tk.Entry(add_win, show="*", width=30)
    entry_pass.grid(row=4, column=1, padx=10, pady=5)

    # Buttons
    tk.Button(add_win, text="Save Item", command=save_item, bg="green", fg="white").grid(row=5, column=0, pady=20)
    tk.Button(add_win, text="Cancel", command=add_win.destroy).grid(row=5, column=1, pady=20)

#Main app window
root = tk.Tk()
root.title("Lost & Found System")
root.geometry("400x300")
data = load_data()

#Label
title_label = tk.Label(root, text="Lost & Found Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=50)

# Add button
add_btn = tk.Button(root, text="Add Item", command=add_item, bg="blue", fg="white", font=("Arial", 12))
add_btn.pack(pady=10)

# Show data status
status_label = tk.Label(root, text=f"Total items: {len(data)}", font=("Arial", 10))
status_label.pack(pady=20)

root.mainloop()
