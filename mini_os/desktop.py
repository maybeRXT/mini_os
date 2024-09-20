import tkinter as tk
from tkinter import Menu, Toplevel, simpledialog
import os
import time
import subprocess

subprocess.Popen(["python", "base.py"])

class DesktopApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Mini OS Desktop")
        self.root.geometry("650x450")
        
        self.running_apps = {}
        
        self.create_taskbar()
        self.update_clock()
        self.create_context_menu()
        
        self.root.bind("<Button-3>", self.show_context_menu)
    
    def create_taskbar(self):
        self.taskbar = tk.Frame(self.root, bg="grey", height=30)
        self.taskbar.pack(side="bottom", fill="x")
        
        start_button = tk.Button(self.taskbar, text="Start", command=self.show_menu)
        start_button.pack(side="left")
        
        self.clock_label = tk.Label(self.taskbar, text="", bg="grey")
        self.clock_label.pack(side="right")
    
    def update_clock(self):
        current_time = time.strftime("%H:%M:%S")
        self.clock_label.config(text=current_time)
        self.root.after(1000, self.update_clock)
    
    def show_menu(self):
        menu = Menu(self.root, tearoff=0)
        
        # Applications menu
        applications_menu = Menu(menu, tearoff=0)
        self.populate_menu(applications_menu, "applications")
        menu.add_cascade(label="Applications", menu=applications_menu)
        
        # Storage menu
        storage_menu = Menu(menu, tearoff=0)
        self.populate_menu(storage_menu, "storage")
        menu.add_cascade(label="Storage", menu=storage_menu)
        
        menu.post(self.root.winfo_pointerx(), self.root.winfo_pointery())
    
    def populate_menu(self, menu, path):
        items = os.listdir(path)
        if items:
            for item in items:
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    submenu = Menu(menu, tearoff=0)
                    self.populate_menu(submenu, item_path)
                    menu.add_cascade(label=item, menu=submenu)
                else:
                    menu.add_command(label=item, command=lambda p=item_path: self.open_file(p))
        else:
            menu.add_command(label="No files in this folder", state="disabled")
    
    def open_file(self, filepath):
        if filepath.endswith(".py"):
            self.create_app_window(filepath)
        else:
            print(f"Cannot open file type: {filepath}")
    
    def create_app_window(self, filepath):
        app_window = Toplevel(self.root)
        app_window.title(filepath)
        app_window.geometry("800x600")
        
        # Window controls
        control_frame = tk.Frame(app_window, bg="lightgrey", height=30)
        control_frame.pack(side="top", fill="x")
        
        close_button = tk.Button(control_frame, text="X", command=lambda: self.close_app_window(filepath, app_window))
        close_button.pack(side="right")
        
        minimize_button = tk.Button(control_frame, text="_", command=lambda: self.minimize_window(app_window))
        minimize_button.pack(side="right")
        
        fullscreen_button = tk.Button(control_frame, text="[ ]", command=lambda: self.fullscreen_window(app_window))
        fullscreen_button.pack(side="right")
        
        # Add to running apps
        self.running_apps[filepath] = app_window
        self.update_taskbar()
        
        # Run the application
        subprocess.Popen(["python", filepath])
    
    def close_app_window(self, filepath, window):
        window.destroy()
        del self.running_apps[filepath]
        self.update_taskbar()
    
    def minimize_window(self, window):
        window.iconify()
    
    def fullscreen_window(self, window):
        if window.attributes('-fullscreen'):
            window.attributes('-fullscreen', False)
        else:
            window.attributes('-fullscreen', True)
    
    def update_taskbar(self):
        for widget in self.taskbar.winfo_children():
            if isinstance(widget, tk.Button) and widget.cget("text") != "Start":
                widget.destroy()
        
        for filepath in self.running_apps:
            app_button = tk.Button(self.taskbar, text=os.path.basename(filepath), command=lambda p=filepath: self.focus_app_window(p))
            app_button.pack(side="left")
    
    def focus_app_window(self, filepath):
        window = self.running_apps.get(filepath)
        if window:
            window.deiconify()
            window.lift()
    
    def create_context_menu(self):
        self.context_menu = Menu(self.root, tearoff=0)
        self.context_menu.add_command(label="New Text File", command=self.create_new_text_file)
        self.context_menu.add_command(label="New Folder", command=self.create_new_folder)
    
    def show_context_menu(self, event):
        self.context_menu.post(event.x_root, event.y_root)
    
    def create_new_text_file(self):
        filename = simpledialog.askstring("New Text File", "Enter file name:")
        if filename:
            filepath = os.path.join("storage", f"{filename}.txt")
            with open(filepath, "w") as f:
                f.write("")
            print(f"Created new text file: {filepath}")
    
    def create_new_folder(self):
        foldername = simpledialog.askstring("New Folder", "Enter folder name:")
        if foldername:
            folderpath = os.path.join("storage", foldername)
            os.makedirs(folderpath, exist_ok=True)
            print(f"Created new folder: {folderpath}")

if __name__ == "__main__":
    root = tk.Tk()
    app = DesktopApp(root)
    root.mainloop()
