import tkinter as tk
import config

def setup_gui():
    window = tk.Tk()
    window.title("SPADE Agents Display")

    window.geometry('1200x600')

    # Define labels for agents and arrange them
    label_c = tk.Label(window, text="C", fg="red")
    label_sm = tk.Label(window, text="SM", fg="blue")
    label_dm = tk.Label(window, text="DM", fg="green")
    label_d = tk.Label(window, text="D", fg="black")

    # Positioning the labels
    label_c.grid(row=0, column=0)
    label_sm.grid(row=0, column=1)
    label_dm.grid(row=0, column=2)
    label_d.grid(row=0, column=3)
    
    window.mainloop()

setup_gui()
