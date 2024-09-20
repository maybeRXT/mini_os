import tkinter as tk
from tkinter import messagebox
import webbrowser

class CustomBrowser:
    def __init__(self, root):
        self.root = root
        self.root.title("CustomBrowser")
        self.root.geometry("800x600")
        
        self.create_widgets()
    
    def create_widgets(self):
        # Title label
        title_label = tk.Label(self.root, text="CustomBrowser", font=("Arial", 24))
        title_label.pack(pady=20)
        
        # Search bar
        self.search_var = tk.StringVar()
        search_entry = tk.Entry(self.root, textvariable=self.search_var, font=("Arial", 16), width=50)
        search_entry.pack(pady=10)
        
        # Search button
        search_button = tk.Button(self.root, text="Search", font=("Arial", 16), command=self.perform_search)
        search_button.pack(pady=10)
    
    def perform_search(self):
        query = self.search_var.get()
        if query:
            url = f"https://www.google.com/search?q={query}"
            webbrowser.open(url)
        else:
            messagebox.showwarning("Input Error", "Please enter a search query.")

if __name__ == "__main__":
    root = tk.Tk()
    app = CustomBrowser(root)
    root.mainloop()
