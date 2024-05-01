# interface.py
import tkinter as tk

class AgentGUI:
    def __init__(self, master):
        self.master = master
        master.title("SPADE Client Agents Control")
        # master.attributes('-fullscreen', True)

        # Set the initial size of the window to 1000x500 pixels
        master.geometry('1000x300')

        # Create a frame on the left side of the window to hold client widgets
        self.clients_frame = tk.Frame(master, bg='white')
        self.clients_frame.pack(side="left", fill="both", expand=True, padx=(10, 5), pady=10)

        # Create a frame on the right side of the window for the Stock Manager
        self.stock_manager_frame = tk.Frame(master, bg='gray')
        self.stock_manager_frame.pack(side="right", fill="both", expand=True, padx=(5, 10), pady=10)

    def add_client(self):
        label = tk.Label(self.clients_frame, text="C", font=("Helvetica", 32), fg="blue")
        label.pack() # Pack widgets from top to bottom

    def add_stock_manager(self):
        # This method creates a label for the Stock Manager in the right frame
        label = tk.Label(self.stock_manager_frame, text="SM", font=("Helvetica", 32), fg="red")
        label.pack()  # Pack widgets from top to bottom        


