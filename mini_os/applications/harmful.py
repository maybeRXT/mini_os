import os

def create_subprocess_file():
    subprocess_folder = "subprocess"
    os.makedirs(subprocess_folder, exist_ok=True)
    
    harmful_file_path = os.path.join(subprocess_folder, "harmful.py")
    with open(harmful_file_path, "w") as f:
        f.write("print('You need to delete harmful.py in subprocess folder')")
    
    print("Harmful file created in subprocess folder.")

def main():
    create_subprocess_file()
    print("You need to delete harmful.py in subprocess folder")

if __name__ == "__main__":
    main()
