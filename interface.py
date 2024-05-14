import tkinter as tk
from tkinter import ttk, PhotoImage
import config  # Import the configuration file

def main_menu():
    def start_application():
        # Update the configuration variables based on the inputs
        config.CLIENTS = int(client_var.get())
        config.DELIVERYMAN = int(delivery_var.get())
        config.LOCATION = location_var.get()  # Save the entered location
        
        # Optionally, you could also print these values or log them to ensure they're set
        print(f"Configuration set - LOCATION: {config.LOCATION}, CLIENTS: {config.CLIENTS}, DELIVERYMAN: {config.DELIVERYMAN}")
        print(f"Starting at {config.LOCATION} with {config.DELIVERYMAN} delivery personnel and {config.CLIENTS} clients.")

    # Initialize the main window
    root = tk.Tk()
    root.title("eBUY")
    root.configure(bg='#ADD8E6')  # Light blue background

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('TLabel', background='#ADD8E6', font=('Helvetica', 16))
    style.configure('TButton', background='#e5383b', foreground='white', font=('Helvetica', 14, 'bold'))
    style.configure('TSpinbox', font=('Helvetica', 14))
    style.configure('TEntry', font=('Helvetica', 14))

    # Loading the logo
    logo = PhotoImage(file="eBUY.png")
    logo_label = ttk.Label(root, image=logo)
    logo_label.pack(pady=10)

    # Configuring the location entry
    location_label = ttk.Label(root, text="Enter your Location:")
    location_label.pack(pady=(20, 0))
    location_var = tk.StringVar()
    location_entry = ttk.Entry(root, textvariable=location_var, width=30)
    location_entry.pack()

    # Configuring the client selection
    client_label = ttk.Label(root, text="Select number of Clients:")
    client_label.pack(pady=(20, 0))
    client_var = tk.StringVar()
    client_spinbox = ttk.Spinbox(root, from_=1, to=100, textvariable=client_var, width=10)
    client_spinbox.pack()

    # Configuring the delivery personnel selection
    delivery_label = ttk.Label(root, text="Select number of Deliveryman:")
    delivery_label.pack(pady=(20, 0))
    delivery_var = tk.StringVar()
    delivery_spinbox = ttk.Spinbox(root, from_=1, to=100, textvariable=delivery_var, width=10)
    delivery_spinbox.pack()

    # Configuring the start button
    start_button = ttk.Button(root, text="START", command=start_application)
    start_button.pack(pady=20)

    # Centering the window
    root.update_idletasks()  # Update internal states
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')

    # Start the main event loop
    root.mainloop()
