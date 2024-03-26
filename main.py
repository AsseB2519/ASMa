import time
from spade import quit_spade

# from Agents.manager import ManagerAgent
# from Agents.taxi import TaxiAgent
# from Agents.customer import CustomerAgent

XMPP_SERVER = 'laptop-ci4qet97'
PASSWORD = 'NOPASSWORD'

MAX_TAXIS = 5  # limit number of taxis
MAX_CUSTOMERS = 100  # limit number of customers

if __name__ == '__main__':

    # Create agents instances
    manager_jid = 'manager@' + XMPP_SERVER
    manager_agent = ManagerAgent(manager_jid, PASSWORD)

    # Start Manager_agent and verify if its ready
    res_manager = manager_agent.start(auto_register=True)
    res_manager.result()

    # Initialize list to save all active Agents in list
    taxi_agents_list = []
    customer_agents_list = []

    # wait for Manager agent to be prepared
    time.sleep(1)

    # Connect Taxi Agents and start them
    for i in range(1, MAX_TAXIS + 1):
        taxi_jid = 'taxi{}@'.format(str(i)) + XMPP_SERVER
        taxi_agent = TaxiAgent(taxi_jid, PASSWORD)

        # store manager_jid in the Taxi Agent knowledge base
        taxi_agent.set('service_contact', manager_jid)

        res_taxi = taxi_agent.start(auto_register=True)
        #res_taxi.result()
        taxi_agents_list.append(taxi_agent)

    # wait for Taxi agents to be prepared
    time.sleep(1)

    # Connect Customer Agents and start them
    for i in range(1, MAX_CUSTOMERS + 1):

        # Sleep 1 second for each x=10 customer agents added
        if i % 10 == 0:
            time.sleep(1)

        customer_jid = 'customer{}@'.format(str(i)) + XMPP_SERVER
        customer_agent = CustomerAgent(customer_jid, PASSWORD)

        # store manager_jid in the Customer Agent knowledge base
        customer_agent.set('service_contact', manager_jid)

        res_agent = customer_agent.start(auto_register=True)
        res_agent.result()
        customer_agents_list.append(customer_agent)

    # Handle interruption of all agents
    while manager_agent.is_alive():
        try:
            time.sleep(1)
        except KeyboardInterrupt:
            # stop all customer Agents
            for customer_agent in customer_agents_list:
                customer_agent.stop()

            # stop all taxi Agents
            for taxi_agent in taxi_agents_list:
                taxi_agent.stop()

            # stop manager agent
            break
    print('Agents finished')

    # finish all the agents and behaviors running in your process
    quit_spade()
