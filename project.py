import tkinter as tk
from tkinter import messagebox, simpledialog, ttk, filedialog
import json
import os
import uuid
from datetime import datetime
import shutil

#Main app window
root = tk.Tk()
root.title("Lost & Found System")
root.geometry("400x300")

#Label
title_label = tk.Label(root, text="Lost & Found Management System", font=("Arial", 16, "bold"))
title_label.pack(pady=50)

root.mainloop()
