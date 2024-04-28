# Initialize the variables; they can be set dynamically later
WAREHOUSE_X = None
WAREHOUSE_Y = None

def get_integer_input(prompt):
    while True:
        try:
            # Try to convert the input to an integer
            value = int(input(prompt))
            return value
        except ValueError:
            # If conversion fails, prompt the user again
            print("Invalid input. Please enter an integer.")