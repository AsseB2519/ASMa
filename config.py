# Initialize the variables; they can be set dynamically later
WAREHOUSE_X = 0
WAREHOUSE_Y = 0
WAREHOUSE = 3142022268

SUPPLIER_X = 20
SUPPLIER_Y = 20

def get_integer_input(prompt):
    while True:
        try:
            # Try to convert the input to an integer
            value = int(input(prompt))
            return value
        except ValueError:
            # If conversion fails, prompt the user again
            print("Invalid input. Please enter an integer.")