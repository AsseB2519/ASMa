import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk, PhotoImage
import time
import threading
import config
from Classes import Graph
from spade import quit_spade
from Classes import Location
from MainPage import main_menu
from Agents.Client import ClientAgent
from Agents.Deliveryman import DeliverymanAgent
from Agents.StockManager import StockManagerAgent
from Agents.DeliverymanManager import DeliverymanManagerAgent
from Agents.Supplier import SupplierAgent
from PIL import Image, ImageTk
import sys

XMPP_SERVER = 'laptop-ci4qet97'
PASSWORD = 'NOPASSWORD'

class Logger:
    def __init__(self, text_widget):
        self.text_widget = text_widget

    def write(self, message):
        self.text_widget.insert(tk.END, message)
        self.text_widget.see(tk.END)

    def flush(self):
        pass  # Needed for file-like object interface

def setup_tkinter_window():
    root = tk.Tk()
    root.title("eBUY")
    root.configure(bg='#ADD8E6')

    # Set the icon for the window
    icon = tk.PhotoImage(file='eBUY.png')
    root.iconphoto(False, icon)

    # Apply a theme
    style = ttk.Style(root)
    style.theme_use("clam")

    # Load and resize the logo
    logo_image = Image.open("eBUY.png")
    logo_image = logo_image.resize((150, 75), Image.LANCZOS)  # Resize the image to 100x100 pixels
    logo = ImageTk.PhotoImage(logo_image)

    # Add logo in the center
    # logo = tk.PhotoImage(file="eBUY.png")
    logo_label = ttk.Label(root, image=logo, background='#ADD8E6')
    logo_label.image = logo  # Keep a reference to avoid garbage collection
    logo_label.pack(pady=10)

    header = ttk.Label(root, text="Agent Terminal", font=("Helvetica", 13, "bold"), background='#ADD8E6')
    header.pack(pady=10)

    log_frame = ttk.Frame(root, padding="10")
    log_frame.pack(expand=True, fill=tk.BOTH)

    log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10))
    log_text.pack(expand=True, fill=tk.BOTH)

    # Centering the window
    root.update_idletasks()  # Update internal states
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f'+{x}+{y}')
    
    return root, log_text

# def setup_tkinter_window():
#     root = tk.Tk()
#     root.title("eBUY")

#     # Apply a theme
#     style = ttk.Style(root)
#     style.theme_use("clam")

#     # Add header
#     header = ttk.Label(root, text="eBUY Agent Terminal", font=("Helvetica", 16, "bold"))
#     header.pack(pady=10)

#     log_frame = ttk.Frame(root, padding="10")
#     log_frame.pack(expand=True, fill=tk.BOTH)

#     log_text = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD, font=("Consolas", 10))
#     log_text.pack(expand=True, fill=tk.BOTH)
    
#     return root, log_text

def start_agents():
    # Your existing main function content goes here
    # config.LOCATION = "Sabrosa"
    # config.CLIENTS = 1
    # config.DELIVERYMAN = 2
    MAX_CLIENTS = config.CLIENTS
    MAX_DELIVERYMAN = config.DELIVERYMAN

    print("Calculating the Graph...")
    neigh, edges, nodes, neighb, edgesb, nodesb = Location.run(config.LOCATION)

    config.NEIGH = neigh
    config.EDGES = edges
    config.NODES = nodes
    config.NEIGHB = neighb
    config.EDGESB = edgesb
    config.NODESB = nodesb

    config.GRAPH = Graph.Grafo(config.NODES, config.NEIGH, config.EDGES)
    config.GRAPH_BIKE = Graph.Grafo(config.NODESB, config.NEIGHB, config.EDGESB)

    config.SUPPLIER = config.random_node_selection(config.FILE_PATH)
    config.WAREHOUSE = config.random_node_selection(config.FILE_PATH)

    deliverymanmanager_jid = 'deliverymanmanager@' + XMPP_SERVER
    deliverymanmanager_agent = DeliverymanManagerAgent(deliverymanmanager_jid, PASSWORD)

    res_deliverymanmanager = deliverymanmanager_agent.start(auto_register=True)
    res_deliverymanmanager.result()

    supplier_jid = 'supplier@' + XMPP_SERVER
    supplier_agent = SupplierAgent(supplier_jid, PASSWORD)

    res_supplier = supplier_agent.start(auto_register=True)
    res_supplier.result()

    stockmanager_jid = 'stockmanager@' + XMPP_SERVER
    stockmanager_agent = StockManagerAgent(stockmanager_jid, PASSWORD)

    stockmanager_agent.set('deliveryman_contact', deliverymanmanager_jid)
    stockmanager_agent.set('supplier_contact', supplier_jid)

    res_stockmanager = stockmanager_agent.start(auto_register=True)
    res_stockmanager.result()

    deliverymanmanager_agent.set('stock_contact', stockmanager_jid)

    client_list = []
    deliveryman_list = []

    time.sleep(1)

    for i in range(1, MAX_DELIVERYMAN + 1):
        deliveryman_jid = 'deliveryman{}@'.format(str(i)) + XMPP_SERVER
        deliveryman_agent = DeliverymanAgent(deliveryman_jid, PASSWORD)

        deliveryman_agent.set('deliveryman_contact', deliverymanmanager_jid)

        res_deliveryman = deliveryman_agent.start(auto_register=True)
        res_deliveryman.result()
        deliveryman_list.append(deliveryman_agent)

    time.sleep(1)

    for i in range(1, MAX_CLIENTS + 1):
        client_jid = 'client{}@'.format(str(i)) + XMPP_SERVER
        client_agent = ClientAgent(client_jid, PASSWORD)

        client_agent.set('stockmanager_contact', stockmanager_jid)

        res_client = client_agent.start(auto_register=True)
        res_client.result()
        client_list.append(client_agent)

    while stockmanager_agent.is_alive() and deliveryman_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            for client_agent in client_list:
                client_agent.stop()

            for deliveryman_agent in deliveryman_list:
                deliveryman_agent.stop()
            break
    print('Agents finished')

    quit_spade()

def on_closing(root):
    root.quit()
    sys.exit()

def main():

    main_menu()

    root, log_text = setup_tkinter_window()
    logger = Logger(log_text)
    
    # Redirect print statements to the logger
    import sys
    sys.stdout = logger

    # Start agent initialization in a separate thread
    agent_thread = threading.Thread(target=start_agents)
    agent_thread.start()

    # Bind the closing event to ensure the terminal stops when the window is closed
    # root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root))

    root.mainloop()

if __name__ == '__main__':
    main()
