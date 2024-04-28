import time
import config
from spade import quit_spade

from Agents.Client import ClientAgent
from Agents.Deliveryman import DeliverymanAgent
from Agents.StockManager import StockManagerAgent
from Agents.DeliverymanManager import DeliverymanManagerAgent
from Agents.Supplier import SupplierAgent

XMPP_SERVER = 'laptop-ci4qet97'
PASSWORD = 'NOPASSWORD'

MAX_DELIVERYMAN = 2  # limit number of deliveryman
MAX_CLIENTS = 1  # limit number of clients

if __name__ == '__main__':

    print("""
                    ooooooooo.   ooooooooo.     .oooooo.    oooooooooooo ooooo  .oooooo..o 
                    `888   `Y88. `888   `Y88.  d8P'  `Y8b  d'""""""d888' `888' d8P'    `Y8 
                    888   .d88'  888   .d88' 888      888       .888P    888  Y88bo.      
                    888ooo88P'   888ooo88P'  888      888      d888'     888   `"Y8888o.  
                    888          888`88b.    888      888    .888P       888       `"Y88b 
                    888          888  `88b.  `88b    d88'   d888'    .P  888  oo     .d8P 
                    o888o        o888o  o888o  `Y8bood8P'  .8888888888P  o888o 8""88888P'  
    """)
    
    # config.WAREHOUSE_X = config.get_integer_input("Enter the location of the Warehouse: X = ")
    # config.WAREHOUSE_Y = config.get_integer_input("Enter the location of the Warehouse: Y = ")

    # config.SUPPLIER_X = config.get_integer_input("Enter the location of the Warehouse: X = ")
    # config.SUPPLIER_Y = config.get_integer_input("Enter the location of the Warehouse: Y = ")

    deliverymanmanager_jid = 'deliverymanmanager@' + XMPP_SERVER
    deliverymanmanager_agent = DeliverymanManagerAgent(deliverymanmanager_jid, PASSWORD)

    # Start Deliveryman Manager and verify if its ready
    res_deliverymanmanager = deliverymanmanager_agent.start(auto_register=True)
    res_deliverymanmanager.result()

    supplier_jid = 'supplier@' + XMPP_SERVER
    supplier_agent = SupplierAgent(supplier_jid, PASSWORD)

    # Start Supplier and verify if its ready
    res_supplier = supplier_agent.start(auto_register=True)
    res_supplier.result()

    stockmanager_jid = 'stockmanager@' + XMPP_SERVER
    stockmanager_agent = StockManagerAgent(stockmanager_jid, PASSWORD)

    stockmanager_agent.set('deliveryman_contact', deliverymanmanager_jid)
    stockmanager_agent.set('supplier_contact', supplier_jid)

    # Start Stock Manager and verify if its ready
    res_stockmanager = stockmanager_agent.start(auto_register=True)
    res_stockmanager.result() 

    # Initialize list to save all active Agents in list
    client_list = []
    deliveryman_list = []

    # wait for Manager agent to be prepared
    time.sleep(1)

    # Connect Deliveryman Agents and start them
    for i in range(1, MAX_DELIVERYMAN + 1):
        deliveryman_jid = 'deliveryman{}@'.format(str(i)) + XMPP_SERVER
        deliveryman_agent = DeliverymanAgent(deliveryman_jid, PASSWORD)

        # store manager_jid in the Deliveryman Agent knowledge base
        deliveryman_agent.set('deliveryman_contact', deliverymanmanager_jid)

        res_deliveryman = deliveryman_agent.start(auto_register=True)
        res_deliveryman.result()
        deliveryman_list.append(deliveryman_agent)

    time.sleep(1)

    # Connect Client Agents and start them
    for i in range(1, MAX_CLIENTS + 1):

        # Sleep 1 second for each x=10 Client agents added
        if i % 10 == 0:
            time.sleep(1)

        client_jid = 'client{}@'.format(str(i)) + XMPP_SERVER
        client_agent = ClientAgent(client_jid, PASSWORD)

        # store manager_jid in the Client Agent knowledge base
        client_agent.set('stockmanager_contact', stockmanager_jid)

        res_client = client_agent.start(auto_register=True)
        res_client.result()
        client_list.append(client_agent)

    # Handle interruption of all agents
    while stockmanager_agent.is_alive() and deliveryman_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # stop all Client Agents
            for client_agent in client_list:
                client_agent.stop()

            # stop all Delivery Agents
            for deliveryman_agent in deliveryman_list:
                deliveryman_agent.stop()

            # stop manager agent
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()
