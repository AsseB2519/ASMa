import tkinter as tk
from threading import Thread

class App:
    def __init__(self, root):
        self.root = root
        self.text = tk.Text(root, height=20, width=50)
        self.text.pack()
        self.print_to_gui("GUI initialized...")

    def print_to_gui(self, message):
        self.text.insert(tk.END, message + "\n")
        self.text.see(tk.END)

def run_gui():
    root = tk.Tk()
    app = App(root)
    root.mainloop()

# Run the GUI in a separate thread
gui_thread = Thread(target=run_gui)
gui_thread.daemon = True
gui_thread.start()
