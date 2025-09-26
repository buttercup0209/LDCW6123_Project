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
            "id": str(uuid.uuid4()),
            "name": entry_name.get(),
            "description": entry_desc.get(),
            "type": type_var.get(),
            "poster": entry_poster.get(),
            "contact": entry_contact.get(),
            "password": entry_pass.get(),
            "status": "Open",
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        if not item["name"] or not item["poster"] or not item["password"]:
            messagebox.showerror("Error", "Name, Posted By, and Password are required.")
            return
            
        if not item["type"]:
            messagebox.showerror("Error", "Please select if this is Lost or Found.")
            return
            
        data.append(item)
        save_data(data)
        messagebox.showinfo("Success", "Item added successfully!")
        add_win.destroy()
        update_status_display()

    add_win = tk.Toplevel(root)
    add_win.title("Add Lost/Found Item")
    add_win.geometry("450x400")

    # Item Name
    tk.Label(add_win, text="Item Name:").grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(add_win, width=30)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    # Description
    tk.Label(add_win, text="Description:").grid(row=1, column=0, sticky="w", padx=10, pady=5)
    entry_desc = tk.Entry(add_win, width=30)
    entry_desc.grid(row=1, column=1, padx=10, pady=5)

    # Type (Lost or Found)
    tk.Label(add_win, text="Type:").grid(row=2, column=0, sticky="w", padx=10, pady=5)
    type_var = tk.StringVar()
    type_frame = tk.Frame(add_win)
    type_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
    tk.Radiobutton(type_frame, text="Lost", variable=type_var, value="Lost").pack(side=tk.LEFT)
    tk.Radiobutton(type_frame, text="Found", variable=type_var, value="Found").pack(side=tk.LEFT, padx=(20, 0))

    # Posted By
    tk.Label(add_win, text="Posted By:").grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_poster = tk.Entry(add_win, width=30)
    entry_poster.grid(row=3, column=1, padx=10, pady=5)

    # Contact
    tk.Label(add_win, text="Contact:").grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_contact = tk.Entry(add_win, width=30)
    entry_contact.grid(row=4, column=1, padx=10, pady=5)

    # Password
    tk.Label(add_win, text="Password:").grid(row=5, column=0, sticky="w", padx=10, pady=5)
    entry_pass = tk.Entry(add_win, show="*", width=30)
    entry_pass.grid(row=5, column=1, padx=10, pady=5)

    # Buttons
    tk.Button(add_win, text="Save Item", command=save_item, bg="green", fg="white").grid(row=6, column=0, pady=20)
    tk.Button(add_win, text="Cancel", command=add_win.destroy).grid(row=6, column=1, pady=20)

# View all items 
def view_items():
    view_win = tk.Toplevel(root)
    view_win.title("All Items")
    view_win.geometry("900x500")

    if not data:
        tk.Label(view_win, text="No items found!", font=("Arial", 16)).pack(pady=50)
        return

    # Create text widget with scrollbar
    frame = tk.Frame(view_win)
    frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

    text_widget = tk.Text(frame, wrap=tk.WORD, font=("Arial", 10))
    scrollbar = tk.Scrollbar(frame, orient=tk.VERTICAL, command=text_widget.yview)
    text_widget.configure(yscrollcommand=scrollbar.set)

    text_widget.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    # Display all items 
    for i, item in enumerate(data, 1):
        text_widget.insert(tk.END, f"--- Item {i} ---\n")
        text_widget.insert(tk.END, f"ID: {item.get('id', 'N/A')}\n")
        text_widget.insert(tk.END, f"Name: {item['name']}\n")
        text_widget.insert(tk.END, f"Type: {item.get('type', 'N/A')}\n")
        text_widget.insert(tk.END, f"Description: {item.get('description', 'N/A')}\n")
        text_widget.insert(tk.END, f"Status: {item['status']}\n")
        text_widget.insert(tk.END, f"Posted by: {item['poster']}\n")
        text_widget.insert(tk.END, f"Contact: {item.get('contact', 'N/A')}\n")
        text_widget.insert(tk.END, f"Created: {item.get('created_at', 'N/A')[:19]}\n")
        text_widget.insert(tk.END, f"Updated: {item.get('updated_at', 'N/A')[:19]}\n")
        text_widget.insert(tk.END, f"\n")

    text_widget.config(state=tk.DISABLED)

# Update item with timestamps
def update_status():
    def mark_claimed():
        name = entry_name.get()
        password = entry_pass.get()
        
        if not name or not password:
            messagebox.showerror("Error", "Both Item Name and Password are required.")
            return
        
        for item in data:
            if item["name"].lower() == name.lower():
                if item["password"] == password:
                    if item["status"] == "Claimed":
                        messagebox.showinfo("Info", f"{name} is already marked as Claimed.")
                        return
                    
                    item["status"] = "Claimed"
                    item["updated_at"] = datetime.now().isoformat()
                    save_data(data)
                    messagebox.showinfo("Success", f"{name} marked as Claimed!")
                    update_win.destroy()
                    update_status_display()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect password.")
                    return
        messagebox.showerror("Error", "Item not found.")

    update_win = tk.Toplevel(root)
    update_win.title("Update Item Status")
    update_win.geometry("400x200")

    tk.Label(update_win, text="Item Name:").grid(row=0, column=0, sticky="w", padx=10, pady=10)
    entry_name = tk.Entry(update_win, width=30)
    entry_name.grid(row=0, column=1, padx=10, pady=10)

    tk.Label(update_win, text="Password:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_pass = tk.Entry(update_win, show="*", width=30)
    entry_pass.grid(row=1, column=1, padx=10, pady=10)

    tk.Button(update_win, text="Mark as Claimed", command=mark_claimed, bg="orange", fg="white").grid(row=2, column=0, columnspan=2, pady=20)

# Delete item
def delete_item():
    def confirm_delete():
        name = entry_name.get()
        password = entry_pass.get()
        
        if not name or not password:
            messagebox.showerror("Error", "Both Item Name and Password are required.")
            return
        
        for i, item in enumerate(data):
            if item["name"].lower() == name.lower():
                if item["password"] == password:
                    confirm = messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete '{name}'?")
                    if confirm:
                        data.pop(i)
                        save_data(data)
                        messagebox.showinfo("Success", f"Item '{name}' deleted successfully!")
                        delete_win.destroy()
                        update_status_display()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect password.")
                    return
        messagebox.showerror("Error", "Item not found.")

    delete_win = tk.Toplevel(root)
    delete_win.title("Delete Item")
    delete_win.geometry("400x250")

    tk.Label(delete_win, text="WARNING: This will permanently delete the item!", 
             font=("Arial", 10, "bold"), fg="red").pack(pady=10)

    tk.Label(delete_win, text="Item Name:").grid(row=1, column=0, sticky="w", padx=10, pady=10)
    entry_name = tk.Entry(delete_win, width=30)
    entry_name.grid(row=1, column=1, padx=10, pady=10)

    tk.Label(delete_win, text="Password:").grid(row=2, column=0, sticky="w", padx=10, pady=10)
    entry_pass = tk.Entry(delete_win, show="*", width=30)
    entry_pass.grid(row=2, column=1, padx=10, pady=10)

    button_frame = tk.Frame(delete_win)
    button_frame.pack(pady=20)
    tk.Button(button_frame, text="Delete Item", command=confirm_delete, bg="red", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=delete_win.destroy).pack(side=tk.LEFT, padx=5)

# Update status display
def update_status_display():
    total = len(data)
    open_items = len([item for item in data if item['status'] == 'Open'])
    claimed_items = len([item for item in data if item['status'] == 'Claimed'])
    lost_items = len([item for item in data if item.get('type') == 'Lost'])
    found_items = len([item for item in data if item.get('type') == 'Found'])
    
    status_label.config(text=f"Total: {total} | Open: {open_items} | Claimed: {claimed_items} | Lost: {lost_items} | Found: {found_items}")

# Main app window
root = tk.Tk()
root.title("Lost & Found System")
root.geometry("500x450")
data = load_data()

#Label
title_label = tk.Label(root, text="Lost & Found Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=30)

# Buttons
add_btn = tk.Button(root, text="Add Item", command=add_item, bg="blue", fg="white", font=("Arial", 12))
add_btn.pack(pady=10)

view_btn = tk.Button(root, text="View Items", command=view_items, bg="green", fg="white", font=("Arial", 12))
view_btn.pack(pady=10)

update_btn = tk.Button(root, text="Update Status", command=update_status, bg="orange", fg="white", font=("Arial", 12))
update_btn.pack(pady=10)

delete_btn = tk.Button(root, text="Delete Item", command=delete_item, bg="red", fg="white", font=("Arial", 12))
delete_btn.pack(pady=10)

# Show data status
status_label = tk.Label(root, text="Loading...", font=("Arial", 10))
status_label.pack(pady=20)

update_status_display()

root.mainloop()