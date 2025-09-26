import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import os
import uuid
from datetime import datetime
import shutil

#For image handling
try:
    from PIL import Image, ImageTk
    PIL_AVAILABLE = True
except ImportError:
    PIL_AVAILABLE = False
    print("Warning: Pillow not installed. Image functionality will be limited.")

try:
    import cv2
    CV2_AVAILABLE = True
except ImportError:
    CV2_AVAILABLE = False
    print("Warning: OpenCV not installed. Camera functionality will be disabled.")

DATA_FILE = "lost_found.json"
IMG_FOLDER = "img"

# Ensure img folder exists
def ensure_img_folder():
    if not os.path.exists(IMG_FOLDER):
        os.makedirs(IMG_FOLDER)

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

# Capture image from camera
def capture_image():
    if not CV2_AVAILABLE:
        messagebox.showerror("Error", "OpenCV not installed. Please install with: pip install opencv-python")
        return None
    
    try:
        cap = cv2.VideoCapture(0)
        if not cap.isOpened():
            messagebox.showerror("Error", "Cannot access camera")
            return None
        
        ret, frame = cap.read()
        if ret:
            ensure_img_folder()
            filename = f"captured_{datetime.now().strftime('%Y%m%d_%H%M%S')}.jpg"
            filepath = os.path.join(IMG_FOLDER, filename)
            cv2.imwrite(filepath, frame)
            cap.release()
            cv2.destroyAllWindows()
            return filepath
        else:
            cap.release()
            messagebox.showerror("Error", "Failed to capture image")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Camera error: {str(e)}")
        return None

# Upload image from file
def upload_image():
    filetypes = (
        ('Image files', '*.jpg *.jpeg *.png *.gif *.bmp'),
        ('All files', '*.*')
    )
    
    filename = filedialog.askopenfilename(
        title='Select an image',
        initialdir=os.getcwd(),
        filetypes=filetypes
    )
    
    if filename:
        ensure_img_folder()
        # Create unique filename
        file_ext = os.path.splitext(filename)[1]
        new_filename = f"uploaded_{datetime.now().strftime('%Y%m%d_%H%M%S')}{file_ext}"
        new_filepath = os.path.join(IMG_FOLDER, new_filename)
        
        try:
            shutil.copy2(filename, new_filepath)
            return new_filepath
        except Exception as e:
            messagebox.showerror("Error", f"Failed to copy image: {str(e)}")
            return None
    return None

# Add new item 
def add_item():
    selected_image = None
    
    def select_image_option():
        nonlocal selected_image
        choice = messagebox.askyesnocancel("Image Option", "Do you want to add an image?\nYes = Upload from file\nNo = Take photo\nCancel = No image")
        
        if choice is True:  # Upload from file
            selected_image = upload_image()
        elif choice is False:  # Take photo
            selected_image = capture_image()
        # choice is None means cancel (no image)
        
        if selected_image:
            img_label.config(text=f"Image: {os.path.basename(selected_image)}")
        else:
            img_label.config(text="No image selected")
    
    def save_item():
        item = {
            "id": str(uuid.uuid4()),
            "name": entry_name.get(),
            "description": entry_desc.get("1.0", tk.END).strip(),
            "type": type_var.get(),
            "status": "Open",
            "poster": entry_poster.get(),
            "contact": entry_contact.get(),
            "password": entry_pass.get(),
            "image_path": selected_image,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        if not item["name"] or not item["poster"] or not item["password"]:
            messagebox.showerror("Error", "Item Name, Posted By, and Password are required.")
            return
        
        if not item["type"]:
            messagebox.showerror("Error", "Please select if this is a Lost or Found item.")
            return
            
        data.append(item)
        save_data(data)
        messagebox.showinfo("Success", "Item added successfully!")
        add_win.destroy()
        refresh_main_view()

    add_win = tk.Toplevel(root)
    add_win.title("Add Lost/Found Item")
    add_win.geometry("500x600")

    # Item Name
    tk.Label(add_win, text="Item Name:*", font=("Arial", 10, "bold")).grid(row=0, column=0, sticky="w", padx=10, pady=5)
    entry_name = tk.Entry(add_win, width=40)
    entry_name.grid(row=0, column=1, padx=10, pady=5)

    # Description
    tk.Label(add_win, text="Description:", font=("Arial", 10, "bold")).grid(row=1, column=0, sticky="nw", padx=10, pady=5)
    entry_desc = tk.Text(add_win, width=40, height=4)
    entry_desc.grid(row=1, column=1, padx=10, pady=5)

    # Type (Lost or Found)
    tk.Label(add_win, text="Type:*", font=("Arial", 10, "bold")).grid(row=2, column=0, sticky="w", padx=10, pady=5)
    type_var = tk.StringVar()
    type_frame = tk.Frame(add_win)
    type_frame.grid(row=2, column=1, sticky="w", padx=10, pady=5)
    tk.Radiobutton(type_frame, text="Lost", variable=type_var, value="Lost").pack(side=tk.LEFT)
    tk.Radiobutton(type_frame, text="Found", variable=type_var, value="Found").pack(side=tk.LEFT, padx=(20, 0))

    # Posted By
    tk.Label(add_win, text="Posted By:*", font=("Arial", 10, "bold")).grid(row=3, column=0, sticky="w", padx=10, pady=5)
    entry_poster = tk.Entry(add_win, width=40)
    entry_poster.grid(row=3, column=1, padx=10, pady=5)

    # Contact
    tk.Label(add_win, text="Contact:", font=("Arial", 10, "bold")).grid(row=4, column=0, sticky="w", padx=10, pady=5)
    entry_contact = tk.Entry(add_win, width=40)
    entry_contact.grid(row=4, column=1, padx=10, pady=5)

    # Password with show/hide functionality
    tk.Label(add_win, text="Verification Password:*", font=("Arial", 10, "bold")).grid(row=5, column=0, sticky="w", padx=10, pady=5)
    pass_frame = tk.Frame(add_win)
    pass_frame.grid(row=5, column=1, sticky="w", padx=10, pady=5)
    
    entry_pass = tk.Entry(pass_frame, show="*", width=35)
    entry_pass.pack(side=tk.LEFT)
    
    show_pass_var = tk.BooleanVar()
    def toggle_password():
        if show_pass_var.get():
            entry_pass.config(show="")
        else:
            entry_pass.config(show="*")
    
    show_pass_check = tk.Checkbutton(pass_frame, text="Show", variable=show_pass_var, command=toggle_password)
    show_pass_check.pack(side=tk.LEFT, padx=(5, 0))

    # Image selection
    tk.Label(add_win, text="Image:", font=("Arial", 10, "bold")).grid(row=6, column=0, sticky="w", padx=10, pady=5)
    img_frame = tk.Frame(add_win)
    img_frame.grid(row=6, column=1, sticky="w", padx=10, pady=5)
    tk.Button(img_frame, text="Add Image", command=select_image_option).pack(side=tk.LEFT)
    img_label = tk.Label(img_frame, text="No image selected", fg="gray")
    img_label.pack(side=tk.LEFT, padx=(10, 0))

    # Buttons
    button_frame = tk.Frame(add_win)
    button_frame.grid(row=7, column=0, columnspan=2, pady=20)
    tk.Button(button_frame, text="Save Item", command=save_item, bg="green", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=add_win.destroy).pack(side=tk.LEFT, padx=5)

# View item details with image
def view_item_details(item):
    detail_win = tk.Toplevel(root)
    detail_win.title(f"Item Details: {item['name']}")
    detail_win.geometry("600x700")
    
    # Item information
    info_frame = tk.Frame(detail_win)
    info_frame.pack(fill="x", padx=10, pady=10)
    
    tk.Label(info_frame, text=f"Name: {item['name']}", font=("Arial", 12, "bold")).pack(anchor="w")
    tk.Label(info_frame, text=f"Type: {item.get('type', 'N/A')}", font=("Arial", 10)).pack(anchor="w")
    tk.Label(info_frame, text=f"Status: {item['status']}", font=("Arial", 10), 
             fg="green" if item['status'] == "Open" else "red").pack(anchor="w")
    tk.Label(info_frame, text=f"Posted by: {item['poster']}", font=("Arial", 10)).pack(anchor="w")
    tk.Label(info_frame, text=f"Contact: {item.get('contact', 'N/A')}", font=("Arial", 10)).pack(anchor="w")
    tk.Label(info_frame, text=f"Created: {item.get('created_at', 'N/A')[:19]}", font=("Arial", 9), fg="gray").pack(anchor="w")
    
    # Description
    if item.get('description'):
        desc_frame = tk.Frame(detail_win)
        desc_frame.pack(fill="both", padx=10, pady=5)
        tk.Label(desc_frame, text="Description:", font=("Arial", 10, "bold")).pack(anchor="w")
        desc_text = tk.Text(desc_frame, height=4, wrap=tk.WORD)
        desc_text.pack(fill="x")
        desc_text.insert(tk.END, item['description'])
        desc_text.config(state=tk.DISABLED)
    
    # Image display
    if item.get('image_path') and os.path.exists(item['image_path']):
        img_frame = tk.Frame(detail_win)
        img_frame.pack(fill="both", expand=True, padx=10, pady=10)
        tk.Label(img_frame, text="Image:", font=("Arial", 10, "bold")).pack(anchor="w")
        
        try:
            # Load and resize image
            if PIL_AVAILABLE:
                img = Image.open(item['image_path'])
                img.thumbnail((400, 300), Image.Resampling.LANCZOS)
                photo = ImageTk.PhotoImage(img)
                
                img_label = tk.Label(img_frame, image=photo)
                img_label.image = photo  # Keep a reference
                img_label.pack(pady=5)
            else:
                tk.Label(img_frame, text="Image file exists but PIL not installed\nInstall with: pip install pillow", fg="orange").pack()
        except Exception as e:
            tk.Label(img_frame, text=f"Error loading image: {str(e)}", fg="red").pack()

# View all items with filtering and search
def view_items():
    view_win = tk.Toplevel(root)
    view_win.title("Lost & Found Items")
    view_win.geometry("1200x700")
    
    # Filter frame
    filter_frame = tk.Frame(view_win, bg="#ecf0f1", relief=tk.RAISED, bd=2)
    filter_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(filter_frame, text="Filter by Status:", font=("Arial", 10, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5, pady=5)
    status_var = tk.StringVar(value="All")
    status_combo = ttk.Combobox(filter_frame, textvariable=status_var, values=["All", "Open", "Claimed"], state="readonly", width=10)
    status_combo.pack(side=tk.LEFT, padx=5, pady=5)
    
    tk.Label(filter_frame, text="Filter by Type:", font=("Arial", 10, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=(20, 5), pady=5)
    type_var = tk.StringVar(value="All")
    type_combo = ttk.Combobox(filter_frame, textvariable=type_var, values=["All", "Lost", "Found"], state="readonly", width=10)
    type_combo.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Search frame
    search_frame = tk.Frame(view_win, bg="#ecf0f1", relief=tk.RAISED, bd=2)
    search_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Label(search_frame, text="🔍 Search:", font=("Arial", 10, "bold"), bg="#ecf0f1").pack(side=tk.LEFT, padx=5, pady=5)
    search_var = tk.StringVar()
    search_entry = tk.Entry(search_frame, textvariable=search_var, width=30, font=("Arial", 10))
    search_entry.pack(side=tk.LEFT, padx=5, pady=5)
    
    # Main content frame with scrollable canvas
    main_frame = tk.Frame(view_win)
    main_frame.pack(fill="both", expand=True, padx=10, pady=5)
    
    # Create canvas and scrollbar for the items
    canvas = tk.Canvas(main_frame, bg="white")
    scrollbar = ttk.Scrollbar(main_frame, orient="vertical", command=canvas.yview)
    scrollable_frame = tk.Frame(canvas, bg="white")
    
    scrollable_frame.bind(
        "<Configure>",
        lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
    )
    
    canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
    canvas.configure(yscrollcommand=scrollbar.set)
    
    canvas.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    
    def update_items_display():
        # Clear existing items
        for widget in scrollable_frame.winfo_children():
            widget.destroy()
        
        # Filter data
        filtered_data = data[:]
        
        if status_var.get() != "All":
            filtered_data = [item for item in filtered_data if item['status'] == status_var.get()]
        
        if type_var.get() != "All":
            filtered_data = [item for item in filtered_data if item.get('type') == type_var.get()]
        
        search_text = search_var.get().lower()
        if search_text:
            filtered_data = [item for item in filtered_data if 
                           search_text in item['name'].lower() or 
                           search_text in item.get('description', '').lower() or
                           search_text in item['poster'].lower()]
        
        # Display items in cards with images
        for i, item in enumerate(filtered_data):
            # Create item card
            card_frame = tk.Frame(scrollable_frame, bg="#ffffff", relief=tk.RAISED, bd=2)
            card_frame.pack(fill="x", padx=10, pady=8, ipady=10)
            
            # Left side - Image
            left_frame = tk.Frame(card_frame, bg="#ffffff")
            left_frame.pack(side=tk.LEFT, padx=15, pady=10)
            
            # Load and display image thumbnail
            if item.get('image_path') and os.path.exists(item['image_path']):
                try:
                    if PIL_AVAILABLE:
                        img = Image.open(item['image_path'])
                        img.thumbnail((120, 120), Image.Resampling.LANCZOS)
                        photo = ImageTk.PhotoImage(img)
                        
                        img_label = tk.Label(left_frame, image=photo, bg="#ffffff", relief=tk.SUNKEN, bd=1)
                        img_label.image = photo  # Keep a reference
                        img_label.pack()
                    else:
                        info_label = tk.Label(left_frame, text="📷\nImage Available\n(PIL not installed)", 
                                            bg="#f8f9fa", fg="#6c757d", width=15, height=8,
                                            font=("Arial", 9), relief=tk.SUNKEN, bd=1, justify=tk.CENTER)
                        info_label.pack()
                except Exception:
                    no_img_label = tk.Label(left_frame, text="📷\nImage Error", 
                                          bg="#f8f9fa", fg="#6c757d", width=15, height=8,
                                          font=("Arial", 9), relief=tk.SUNKEN, bd=1, justify=tk.CENTER)
                    no_img_label.pack()
            else:
                no_img_label = tk.Label(left_frame, text="📷\nNo Image\nAvailable", 
                                      bg="#f8f9fa", fg="#6c757d", width=15, height=8,
                                      font=("Arial", 9), relief=tk.SUNKEN, bd=1, justify=tk.CENTER)
                no_img_label.pack()
            
            # Right side - Item details
            right_frame = tk.Frame(card_frame, bg="#ffffff")
            right_frame.pack(side=tk.LEFT, fill="both", expand=True, padx=15, pady=10)
            
            # Item name and type
            name_frame = tk.Frame(right_frame, bg="#ffffff")
            name_frame.pack(fill="x", anchor="w")
            
            name_label = tk.Label(name_frame, text=item['name'], font=("Arial", 14, "bold"), 
                                bg="#ffffff", fg="#2c3e50")
            name_label.pack(side=tk.LEFT)
            
            type_color = "#e74c3c" if item.get('type') == 'Lost' else "#27ae60"
            type_label = tk.Label(name_frame, text=f"  [{item.get('type', 'N/A')}]", 
                                font=("Arial", 10, "bold"), bg="#ffffff", fg=type_color)
            type_label.pack(side=tk.LEFT)
            
            # Status
            status_color = "#27ae60" if item['status'] == 'Open' else "#e74c3c"
            status_icon = "🟢" if item['status'] == 'Open' else "🔴"
            status_label = tk.Label(right_frame, text=f"{status_icon} Status: {item['status']}", 
                                  font=("Arial", 10, "bold"), bg="#ffffff", fg=status_color)
            status_label.pack(anchor="w", pady=(5, 2))
            
            # Description (truncated)
            desc_text = item.get('description', 'No description provided')
            if len(desc_text) > 100:
                desc_text = desc_text[:97] + "..."
            desc_label = tk.Label(right_frame, text=f"Description: {desc_text}", 
                                font=("Arial", 10), bg="#ffffff", fg="#34495e", wraplength=500, justify=tk.LEFT)
            desc_label.pack(anchor="w", pady=2)
            
            # Posted by and contact
            poster_label = tk.Label(right_frame, text=f"👤 Posted by: {item['poster']}", 
                                  font=("Arial", 10), bg="#ffffff", fg="#34495e")
            poster_label.pack(anchor="w", pady=2)
            
            if item.get('contact'):
                contact_label = tk.Label(right_frame, text=f"📞 Contact: {item['contact']}", 
                                       font=("Arial", 10), bg="#ffffff", fg="#34495e")
                contact_label.pack(anchor="w", pady=2)
            
            # Created date
            created = item.get('created_at', 'N/A')[:19] if item.get('created_at') else 'N/A'
            date_label = tk.Label(right_frame, text=f"📅 Created: {created}", 
                                font=("Arial", 9), bg="#ffffff", fg="#7f8c8d")
            date_label.pack(anchor="w", pady=2)
            
            # View details button
            detail_btn = tk.Button(right_frame, text="View Full Details", 
                                 command=lambda it=item: view_item_details(it),
                                 bg="#3498db", fg="white", font=("Arial", 9, "bold"),
                                 relief=tk.RAISED, bd=2)
            detail_btn.pack(anchor="e", pady=(10, 0))
        
        if not filtered_data:
            no_items_label = tk.Label(scrollable_frame, text="No items found matching your criteria", 
                                    font=("Arial", 16), bg="white", fg="#7f8c8d")
            no_items_label.pack(expand=True, pady=50)
    
    # Bind events
    status_combo.bind("<<ComboboxSelected>>", lambda e: update_items_display())
    type_combo.bind("<<ComboboxSelected>>", lambda e: update_items_display())
    search_entry.bind("<KeyRelease>", lambda e: update_items_display())
    
    # Buttons frame
    button_frame = tk.Frame(view_win, bg="#ecf0f1", relief=tk.RAISED, bd=2)
    button_frame.pack(fill="x", padx=10, pady=5)
    
    tk.Button(button_frame, text="🔄 Refresh", command=update_items_display, 
              bg="#9b59b6", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5, pady=5)
    tk.Button(button_frame, text="❌ Close", command=view_win.destroy,
              bg="#95a5a6", fg="white", font=("Arial", 10, "bold")).pack(side=tk.RIGHT, padx=5, pady=5)
    
    # Initial load
    update_items_display()
    
    # Bind mousewheel to canvas
    def _on_mousewheel(event):
        canvas.yview_scroll(int(-1*(event.delta/120)), "units")
    canvas.bind_all("<MouseWheel>", _on_mousewheel)

# Update status
def update_status():
    def mark_claimed():
        name = entry_name.get().strip()
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
                    messagebox.showinfo("Success", f"{name} marked as Claimed successfully!")
                    update_win.destroy()
                    refresh_main_view()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect verification password.")
                    return
        messagebox.showerror("Error", "Item not found. Please check the item name.")

    def reopen_item():
        name = entry_name.get().strip()
        password = entry_pass.get()
        
        if not name or not password:
            messagebox.showerror("Error", "Both Item Name and Password are required.")
            return
        
        for item in data:
            if item["name"].lower() == name.lower():
                if item["password"] == password:
                    if item["status"] == "Open":
                        messagebox.showinfo("Info", f"{name} is already marked as Open.")
                        return
                    
                    item["status"] = "Open"
                    item["updated_at"] = datetime.now().isoformat()
                    save_data(data)
                    messagebox.showinfo("Success", f"{name} reopened successfully!")
                    update_win.destroy()
                    refresh_main_view()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect verification password.")
                    return
        messagebox.showerror("Error", "Item not found. Please check the item name.")

    update_win = tk.Toplevel(root)
    update_win.title("Update Item Status")
    update_win.geometry("400x250")

    # Instructions
    instruction_label = tk.Label(update_win, 
                                text="Enter the exact item name and verification password\nto update the status:",
                                font=("Arial", 10), justify=tk.LEFT)
    instruction_label.pack(pady=10)

    # Item Name
    tk.Label(update_win, text="Item Name:*", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
    entry_name = tk.Entry(update_win, width=40)
    entry_name.pack(padx=20, pady=5)

    # Password with show/hide functionality
    tk.Label(update_win, text="Verification Password:*", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
    pass_frame = tk.Frame(update_win)
    pass_frame.pack(padx=20, pady=5)
    
    entry_pass = tk.Entry(pass_frame, show="*", width=35)
    entry_pass.pack(side=tk.LEFT)
    
    show_pass_var = tk.BooleanVar()
    def toggle_password():
        if show_pass_var.get():
            entry_pass.config(show="")
        else:
            entry_pass.config(show="*")
    
    show_pass_check = tk.Checkbutton(pass_frame, text="Show", variable=show_pass_var, command=toggle_password)
    show_pass_check.pack(side=tk.LEFT, padx=(5, 0))

    # Buttons
    button_frame = tk.Frame(update_win)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Mark as Claimed", command=mark_claimed, 
              bg="orange", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Reopen Item", command=reopen_item, 
              bg="blue", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=update_win.destroy).pack(side=tk.LEFT, padx=5)

# Delete item (for admins)
def delete_item():
    def confirm_delete():
        name = entry_name.get().strip()
        password = entry_pass.get()
        
        if not name or not password:
            messagebox.showerror("Error", "Both Item Name and Password are required.")
            return
        
        for i, item in enumerate(data):
            if item["name"].lower() == name.lower():
                if item["password"] == password:
                    confirm = messagebox.askyesno("Confirm Delete", 
                                                f"Are you sure you want to delete '{name}'?\nThis action cannot be undone.")
                    if confirm:
                        # Delete associated image if exists
                        if item.get('image_path') and os.path.exists(item['image_path']):
                            try:
                                os.remove(item['image_path'])
                            except:
                                pass  # Image deletion failed but continue with item deletion
                        
                        data.pop(i)
                        save_data(data)
                        messagebox.showinfo("Success", f"Item '{name}' deleted successfully!")
                        delete_win.destroy()
                        refresh_main_view()
                    return
                else:
                    messagebox.showerror("Error", "Incorrect verification password.")
                    return
        messagebox.showerror("Error", "Item not found. Please check the item name.")

    delete_win = tk.Toplevel(root)
    delete_win.title("Delete Item")
    delete_win.geometry("400x200")

    # Warning
    warning_label = tk.Label(delete_win, 
                           text="⚠️ WARNING: This will permanently delete the item!",
                           font=("Arial", 10, "bold"), fg="red")
    warning_label.pack(pady=10)

    tk.Label(delete_win, text="Item Name:*", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
    entry_name = tk.Entry(delete_win, width=40)
    entry_name.pack(padx=20, pady=5)

    tk.Label(delete_win, text="Verification Password:*", font=("Arial", 10, "bold")).pack(anchor="w", padx=20)
    pass_frame = tk.Frame(delete_win)
    pass_frame.pack(padx=20, pady=5)
    
    entry_pass = tk.Entry(pass_frame, show="*", width=35)
    entry_pass.pack(side=tk.LEFT)
    
    show_pass_var = tk.BooleanVar()
    def toggle_password():
        if show_pass_var.get():
            entry_pass.config(show="")
        else:
            entry_pass.config(show="*")
    
    show_pass_check = tk.Checkbutton(pass_frame, text="Show", variable=show_pass_var, command=toggle_password)
    show_pass_check.pack(side=tk.LEFT, padx=(5, 0))

    button_frame = tk.Frame(delete_win)
    button_frame.pack(pady=20)
    
    tk.Button(button_frame, text="Delete Item", command=confirm_delete, 
              bg="red", fg="white", font=("Arial", 10, "bold")).pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Cancel", command=delete_win.destroy).pack(side=tk.LEFT, padx=5)

# Dashboard status
def get_statistics():
    total_items = len(data)
    open_items = len([item for item in data if item['status'] == 'Open'])
    claimed_items = len([item for item in data if item['status'] == 'Claimed'])
    lost_items = len([item for item in data if item.get('type') == 'Lost'])
    found_items = len([item for item in data if item.get('type') == 'Found'])
    items_with_images = len([item for item in data if item.get('image_path') and os.path.exists(item.get('image_path', ''))])
    
    return {
        'total': total_items,
        'open': open_items,
        'claimed': claimed_items,
        'lost': lost_items,
        'found': found_items,
        'with_images': items_with_images
    }

# Refresh main view
def refresh_main_view():
    stats = get_statistics()
    stats_label.config(text=f"📊 Status: {stats['total']} Total | {stats['open']} Open | {stats['claimed']} Claimed | {stats['lost']} Lost | {stats['found']} Found | {stats['with_images']} With Images")

# Main window setup
def setup_main_window():
    global stats_label
    
    root.title("🔍 Lost & Found Management System")
    root.geometry("600x500")
    root.configure(bg="#f0f0f0")
    
    # Title
    title_label = tk.Label(root, text="Lost & Found Management System", 
                          font=("Arial", 18, "bold"), bg="#f0f0f0", fg="#2c3e50")
    title_label.pack(pady=20)
    
    # Statistics
    stats_label = tk.Label(root, text="Loading statistics...", 
                          font=("Arial", 12), bg="#ecf0f1", fg="#34495e", relief=tk.SUNKEN)
    stats_label.pack(fill="x", padx=20, pady=10)
    
    # Button frame
    button_frame = tk.Frame(root, bg="#f0f0f0")
    button_frame.pack(expand=True, pady=30)
    
    # Create simple working buttons
    btn1 = tk.Button(button_frame, text="➕ Add Item", command=add_item,
                    font=("Arial", 14, "bold"), bg="#27ae60", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn1.pack(pady=8)
    
    btn2 = tk.Button(button_frame, text="👁️ View Items", command=view_items,
                    font=("Arial", 14, "bold"), bg="#3498db", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn2.pack(pady=8)
    
    btn3 = tk.Button(button_frame, text="✏️ Update Status", command=update_status,
                    font=("Arial", 14, "bold"), bg="#f39c12", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn3.pack(pady=8)
    
    btn4 = tk.Button(button_frame, text="🗑️ Delete Item", command=delete_item,
                    font=("Arial", 14, "bold"), bg="#e74c3c", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn4.pack(pady=8)
    
    btn5 = tk.Button(button_frame, text="📊 Refresh Stats", command=refresh_main_view,
                    font=("Arial", 14, "bold"), bg="#9b59b6", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn5.pack(pady=8)
    
    btn6 = tk.Button(button_frame, text="❌ Exit", command=root.quit,
                    font=("Arial", 14, "bold"), bg="#95a5a6", fg="white",
                    width=25, height=2, relief=tk.RAISED, bd=3)
    btn6.pack(pady=8)
    
    # Instructions
    instructions = tk.Label(root, 
                           text="💡 Use verification passwords to secure your posts • Upload photos for better identification",
                           font=("Arial", 10), bg="#f0f0f0", fg="#7f8c8d", wraplength=500)
    instructions.pack(pady=10)
    
    # Initial stats load
    refresh_main_view()

# Main app window
root = tk.Tk()
data = load_data()
ensure_img_folder()

setup_main_window()

root.mainloop()