def load_orders():
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            orders = []
            for line in lines:
                # Remove whitespace and split by comma
                parts = line.strip().split(",")
                if len(parts) == 3:
                    # Store as a list: [ID, Name, Quantity]
                    orders.append([parts[0], parts[1], int(parts[2])])
            return orders
    except FileNotFoundError:
        # Return an empty list if the file doesn't exist yet
        return []

def get_valid_quantity():
    while True:
        user_input = input("Enter Quantity: ")
        try:
            amount = int(user_input)
            if amount < 0:
                print("Please enter a positive number.")
            else:
                return amount
        except ValueError:
            print("Invalid input. Please enter a number.")

orders = load_orders()

print("Current Orders:")
print()
for order in orders:
    print(f"{order[0]}, {order[1]}, {order[2]}")

print()

# Get New Order Input
product_name = input("Enter Product Name: ")
quantity = get_valid_quantity()

# Generate New Order ID
if orders:
    last_id = int(orders[-1][0])
    new_id = str(last_id + 1)
else:
    new_id = "1001"

# Add the new order to the list (Tracking History)
new_order = [new_id, product_name, quantity]
orders.append(new_order)

# Display New Order Added
print()
print("New Order Added:")
print(f"{new_id},{product_name},{quantity}")