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

CLIENTS = 1

FILE_PATH = 'Classes/dics/nodes.txt'

def get_integer_input(prompt):
    while True:
        try:
            # Try to convert the input to an integer
            value = int(input(prompt))
            return value
        except ValueError:
            # If conversion fails, prompt the user again
            print("Invalid input. Please enter an integer.")

def get_string_input(prompt):
    while True:
        try:
            # Get input from the user
            value = input(prompt)
            return value
        except Exception as e:
            # Handle exceptions
            print("Error:", e)

def random_node_selection(file_path):
    # Open the file and read all lines
    with open(file_path, 'r') as file:
        lines = file.readlines()

    # Extract node numbers from each line
    node_numbers = [int(line.strip().split(' ')[1]) for line in lines]

    # Randomly select a node number
    selected_node = random.choice(node_numbers)
    return selected_node