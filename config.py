import random

# Initialize the variables; they can be set dynamically later
WAREHOUSE_X = 0
WAREHOUSE_Y = 0
WAREHOUSE = 3142022268

SUPPLIER_X = 0
SUPPLIER_Y = 0
SUPPLIER = 210962203

LOCATION = None

NEIGH = None
EDGES = None
NODES = None
NEIGHB = None
EDGESB = None
NODESB = None

CLIENTS = None
DELIVERYMAN = None

GRAPH = None
GRAPH_BIKE = None

CLIENT_LIST = []
DELIVERYMAN_LIST = []

FILE_PATH = 'Classes/dics/nodes.txt'

def random_node_selection(file_path):
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract node numbers from each line
    node_numbers = [int(line.strip().split(' ')[1]) for line in lines]

    # Randomly select a node number
    selected_node = random.choice(node_numbers)
    return selected_node