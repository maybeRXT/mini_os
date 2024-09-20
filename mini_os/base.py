import os
import time
import threading
import subprocess

class BaseSystem:
    def __init__(self):
        self.running = True
        self.setup_directories()
    
    def setup_directories(self):
        directories = [
            "applications",
            "storage",
            "subprocess"
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            print(f"Ensured directory exists: {directory}")
    
    def create_file(self, path, content=""):
        with open(path, "w") as f:
            f.write(content)
        print(f"Created file: {path}")
    
    def create_folder(self, path):
        os.makedirs(path, exist_ok=True)
        print(f"Created folder: {path}")
    
    def delete_file(self, path):
        if os.path.exists(path):
            os.remove(path)
            print(f"Deleted file: {path}")
        else:
            print(f"File not found: {path}")
    
    def delete_folder(self, path):
        if os.path.exists(path):
            os.rmdir(path)
            print(f"Deleted folder: {path}")
        else:
            print(f"Folder not found: {path}")
    
    def list_directory(self, path):
        if os.path.exists(path):
            return os.listdir(path)
        else:
            print(f"Directory not found: {path}")
            return []
    
    def monitor_typing(self):
        while self.running:
            user_input = input("Type something: ")
            print(f"You typed: {user_input}")
            if user_input.lower() == "exit":
                self.running = False
    
    def run_subprocess_scripts(self):
        while self.running:
            for script in os.listdir("subprocess"):
                if script.endswith(".py"):
                    script_path = os.path.join("subprocess", script)
                    subprocess.Popen(["python", script_path])
            time.sleep(10)  # Check every 10 seconds
    
    def start(self):
        threading.Thread(target=self.monitor_typing).start()
        threading.Thread(target=self.run_subprocess_scripts).start()
        print("Base system started and monitoring typing and subprocess folder...")

if __name__ == "__main__":
    base_system = BaseSystem()
    base_system.start()
