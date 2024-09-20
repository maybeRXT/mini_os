import tkinter as tk
from tkinter import ttk, messagebox
import psutil
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import speedtest
import threading

class NetworkModule:
    def __init__(self, root):
        self.root = root
        self.root.title("Network Module")
        self.root.geometry("800x600")
        
        self.create_tabs()
    
    def create_tabs(self):
        tab_control = ttk.Notebook(self.root)
        
        self.port_usage_tab = ttk.Frame(tab_control)
        self.port_graph_tab = ttk.Frame(tab_control)
        self.speed_test_tab = ttk.Frame(tab_control)
        
        tab_control.add(self.port_usage_tab, text="Port Usage")
        tab_control.add(self.port_graph_tab, text="Port Usage Graph")
        tab_control.add(self.speed_test_tab, text="Network Speed Test")
        
        tab_control.pack(expand=1, fill="both")
        
        self.create_port_usage_tab()
        self.create_port_graph_tab()
        self.create_speed_test_tab()
    
    def create_port_usage_tab(self):
        self.port_tree = ttk.Treeview(self.port_usage_tab, columns=("Port", "Status"), show="headings")
        self.port_tree.heading("Port", text="Port")
        self.port_tree.heading("Status", text="Status")
        self.port_tree.pack(expand=True, fill="both")
        
        self.update_port_usage()
    
    def update_port_usage(self):
        self.port_tree.delete(*self.port_tree.get_children())
        connections = psutil.net_connections()
        for conn in connections:
            self.port_tree.insert("", "end", values=(conn.laddr.port, conn.status))
    
    def create_port_graph_tab(self):
        self.figure = plt.Figure(figsize=(6, 4), dpi=100)
        self.ax = self.figure.add_subplot(111)
        self.canvas = FigureCanvasTkAgg(self.figure, self.port_graph_tab)
        self.canvas.get_tk_widget().pack(expand=True, fill="both")
        
        self.update_port_graph()
    
    def update_port_graph(self):
        connections = psutil.net_connections()
        port_counts = {}
        for conn in connections:
            port = conn.laddr.port
            port_counts[port] = port_counts.get(port, 0) + 1
        
        ports = list(port_counts.keys())
        counts = list(port_counts.values())
        
        self.ax.clear()
        self.ax.bar(ports, counts)
        self.ax.set_title("Port Usage")
        self.ax.set_xlabel("Port")
        self.ax.set_ylabel("Usage Count")
        self.canvas.draw()
    
    def create_speed_test_tab(self):
        self.speed_test_button = tk.Button(self.speed_test_tab, text="Run Speed Test", command=self.run_speed_test)
        self.speed_test_button.pack(pady=20)
        
        self.speed_test_result = tk.Label(self.speed_test_tab, text="")
        self.speed_test_result.pack(pady=20)
    
    def run_speed_test(self):
        self.speed_test_result.config(text="Running speed test...")
        threading.Thread(target=self.perform_speed_test).start()
    
    def perform_speed_test(self):
        st = speedtest.Speedtest()
        st.download()
        st.upload()
        results = st.results.dict()
        
        download_speed = results["download"] / 1_000_000  # Convert to Mbps
        upload_speed = results["upload"] / 1_000_000  # Convert to Mbps
        
        result_text = f"Download Speed: {download_speed:.2f} Mbps\nUpload Speed: {upload_speed:.2f} Mbps"
        self.speed_test_result.config(text=result_text)

if __name__ == "__main__":
    root = tk.Tk()
    app = NetworkModule(root)
    root.mainloop()
