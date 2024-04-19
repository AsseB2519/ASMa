import time
from spade import quit_spade

from Agents.Client import ClientAgent
from Agents.Deliveryman import DeliverymanAgent
from Agents.Manager import ManagerAgent
from Agents.StockManager import StockManagerAgent
from Agents.DeliverymanManager import DeliverymanManagerAgent


XMPP_SERVER = 'laptop-ci4qet97'
PASSWORD = 'NOPASSWORD'

MAX_DELIVERYMAN = 1  # limit number of deliveryman
MAX_CLIENTS = 1  # limit number of clients

if __name__ == '__main__':
    deliverymanmanager_jid = 'deliverymanmanager@' + XMPP_SERVER
    deliverymanmanager_agent = DeliverymanManagerAgent(deliverymanmanager_jid, PASSWORD)

    # Start Deliveryman Manager and verify if its ready
    res_deliverymanmanager = deliverymanmanager_agent.start(auto_register=True)
    res_deliverymanmanager.result()

    stockmanager_jid = 'stockmanager@' + XMPP_SERVER
    stockmanager_agent = StockManagerAgent(stockmanager_jid, PASSWORD)

    stockmanager_agent.set('deliveryman_contact', deliverymanmanager_jid)

    # Start Stock Manager and verify if its ready
    res_stockmanager = stockmanager_agent.start(auto_register=True)
    res_stockmanager.result()

    # Create agents instances
    manager_jid = 'manager@' + XMPP_SERVER
    manager_agent = ManagerAgent(manager_jid, PASSWORD)
    manager_agent.set('stock_contact', stockmanager_jid)
    manager_agent.set('deliveryman_contact', deliverymanmanager_jid)

    stockmanager_agent.set('service_contact', manager_jid)

    deliverymanmanager_agent.set('service_contact', manager_jid)

    # Start Manager_agent and verify if its ready
    res_manager = manager_agent.start(auto_register=True)
    res_manager.result()

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
        deliveryman_agent.set('service_contact', manager_jid)

        res_deliveryman = deliveryman_agent.start(auto_register=True)
        res_deliveryman.result()
        deliveryman_list.append(deliveryman_agent)

    # wait for Taxi agents to be prepared
    time.sleep(1)

    # Connect Client Agents and start them
    for i in range(1, MAX_CLIENTS + 1):

        # Sleep 1 second for each x=10 Client agents added
        if i % 10 == 0:
            time.sleep(1)

        client_jid = 'client{}@'.format(str(i)) + XMPP_SERVER
        client_agent = ClientAgent(client_jid, PASSWORD)

        # store manager_jid in the Client Agent knowledge base
        client_agent.set('service_contact', manager_jid)

        res_client = client_agent.start(auto_register=True)
        res_client.result()
        client_list.append(client_agent)

    # Handle interruption of all agents
    while manager_agent.is_alive():
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
