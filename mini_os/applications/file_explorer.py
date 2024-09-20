import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import os
import shutil

class FileExplorer:
    def __init__(self, root):
        self.root = root
        self.root.title("File Explorer")
        self.root.geometry("800x600")
        
        self.current_path = os.path.expanduser("~")
        self.create_widgets()
        self.load_directory(self.current_path)
    
    def create_widgets(self):
        self.tree = ttk.Treeview(self.root, columns=("Name", "Type", "Size"), show="headings")
        self.tree.heading("Name", text="Name")
        self.tree.heading("Type", text="Type")
        self.tree.heading("Size", text="Size")
        self.tree.pack(expand=True, fill="both")
        
        self.tree.bind("<Double-1>", self.on_double_click)
        
        self.menu = tk.Menu(self.root, tearoff=0)
        self.menu.add_command(label="Open", command=self.open_item)
        self.menu.add_command(label="Delete", command=self.delete_item)
        self.menu.add_command(label="Rename", command=self.rename_item)
        self.menu.add_command(label="Copy", command=self.copy_item)
        self.menu.add_command(label="Move", command=self.move_item)
        self.menu.add_command(label="Properties", command=self.view_properties)
        self.menu.add_command(label="Create New File", command=self.create_new_file)
        self.menu.add_command(label="Create New Folder", command=self.create_new_folder)
        self.menu.add_command(label="Sort", command=self.sort_items)
        self.menu.add_command(label="Refresh", command=self.refresh_directory)
        self.menu.add_command(label="Open with Default Application", command=self.open_with_default_application)
        self.menu.add_command(label="Show Hidden Files", command=self.toggle_hidden_files)
        
        self.root.bind("<Button-3>", self.show_context_menu)
    
    def load_directory(self, path):
        self.tree.delete(*self.tree.get_children())
        try:
            for item in os.listdir(path):
                item_path = os.path.join(path, item)
                if os.path.isdir(item_path):
                    item_type = "Folder"
                    item_size = ""
                else:
                    item_type = "File"
                    item_size = os.path.getsize(item_path)
                self.tree.insert("", "end", values=(item, item_type, item_size))
            self.current_path = path
            self.root.title(f"File Explorer - {path}")
        except PermissionError:
            messagebox.showerror("Error", "Permission denied")
    
    def on_double_click(self, event):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_type = self.tree.item(item, "values")[1]
        
        if item_type == "Folder":
            current_path = os.path.join(self.current_path, item_name)
            self.load_directory(current_path)
    
    def open_item(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_type = self.tree.item(item, "values")[1]
        
        if item_type == "Folder":
            current_path = os.path.join(self.current_path, item_name)
            self.load_directory(current_path)
        else:
            os.startfile(os.path.join(self.current_path, item_name))
    
    def delete_item(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        
        if os.path.isdir(item_path):
            os.rmdir(item_path)
        else:
            os.remove(item_path)
        
        self.tree.delete(item)
    
    def rename_item(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        
        new_name = simpledialog.askstring("Rename", "Enter new name:")
        if new_name:
            new_path = os.path.join(self.current_path, new_name)
            os.rename(item_path, new_path)
            self.tree.item(item, values=(new_name, self.tree.item(item, "values")[1], self.tree.item(item, "values")[2]))
    
    def copy_item(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        
        destination = filedialog.askdirectory(title="Select Destination")
        if destination:
            shutil.copy(item_path, destination)
            messagebox.showinfo("Copy", f"Copied {item_name} to {destination}")
    
    def move_item(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        
        destination = filedialog.askdirectory(title="Select Destination")
        if destination:
            shutil.move(item_path, destination)
            self.tree.delete(item)
            messagebox.showinfo("Move", f"Moved {item_name} to {destination}")
    
    def view_properties(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        
        properties = f"Name: {item_name}\nPath: {item_path}\n"
        if os.path.isdir(item_path):
            properties += "Type: Folder\n"
        else:
            properties += f"Type: File\nSize: {os.path.getsize(item_path)} bytes\n"
        
        messagebox.showinfo("Properties", properties)
    
    def create_new_file(self):
        filename = simpledialog.askstring("New File", "Enter file name:")
        if filename:
            filepath = os.path.join(self.current_path, filename)
            with open(filepath, "w") as f:
                f.write("")
            self.load_directory(self.current_path)
    
    def create_new_folder(self):
        foldername = simpledialog.askstring("New Folder", "Enter folder name:")
        if foldername:
            folderpath = os.path.join(self.current_path, foldername)
            os.makedirs(folderpath, exist_ok=True)
            self.load_directory(self.current_path)
    
    def sort_items(self):
        items = [(self.tree.item(child, "values")[0], child) for child in self.tree.get_children()]
        items.sort()
        for index, (name, child) in enumerate(items):
            self.tree.move(child, "", index)
    
    def refresh_directory(self):
        self.load_directory(self.current_path)
    
    def open_with_default_application(self):
        item = self.tree.selection()[0]
        item_name = self.tree.item(item, "values")[0]
        item_path = os.path.join(self.current_path, item_name)
        os.startfile(item_path)
    
    def toggle_hidden_files(self):
        self.show_hidden = not getattr(self, 'show_hidden', False)
        self.load_directory(self.current_path)
    
    def show_context_menu(self, event):
        self.menu.post(event.x_root, event.y_root)

if __name__ == "__main__":
    root = tk.Tk()
    app = FileExplorer(root)
    root.mainloop()