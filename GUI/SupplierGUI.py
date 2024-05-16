import tkinter as tk
from threading import Thread

class SupplierGUI:
    def __init__(self, master, agent):
        self.agent = agent
        self.window = tk.Toplevel(master)
        self.window.title(f"Supplier Agent: {agent.jid}")
        
        # Add widgets to display information
        self.info_text = tk.Text(self.window, height=10, width=50)
        self.info_text.pack()
        self.update_info()

    def update_info(self):
        # Example update method to display the agent's position
        pos = self.agent.position
        self.info_text.insert(tk.END, f"CHEGUEI")
        self.info_text.see(tk.END)
        self.window.after(1000, self.update_info)  # update every second

def start_supplier_gui(agent):
    root = tk.Tk()
    app = SupplierGUI(root, agent)
    root.mainloop()
