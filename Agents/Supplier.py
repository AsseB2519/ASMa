from spade import agent
import config

from Behaviours.TransportSupply import TransportSupply_Behav
from Classes.Position import Position

from colorama import Fore, Style, init

class SupplierAgent(agent.Agent):
    async def setup(self):
        init(autoreset=True)

        print(Fore.WHITE + "Agent {} starting...".format(str(self.jid)))
        print("\033[31mAgent {}\033[0m starting...".format(str(self.jid)))
        # print("Agent {}".format(str(self.jid)) + " starting...")

        self.position = Position(int(config.WAREHOUSE_X), int(config.WAREHOUSE_Y), int(config.WAREHOUSE))

        a = TransportSupply_Behav()
        self.add_behaviour(a)