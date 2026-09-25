def load_orders():
    try:
        with open("orders.txt", "r") as file:
            lines = file.readlines()
            orders = []
            for line in lines:
                parts = line.strip().split(",")
                if len(parts) == 3:
                    orders.append([parts[0], parts[1], int(parts[2])])
            return orders
    except FileNotFoundError:
        return []

def save_orders(orders):
    with open("orders.txt", "w") as file:
        for order in orders:
            # Write format: ID,Name,Quantity
            file.write(f"{order[0]},{order[1]},{order[2]}\n")

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

# --- Main Program (Phase C) ---
orders = load_orders()

print("Current Orders:")
print()
for order in orders:
    print(f"{order[0]}, {order[1]}, {order[2]}")

print()

product_name = input("Enter Product Name: ")
quantity = get_valid_quantity()

if orders:
    last_id = int(orders[-1][0])
    new_id = str(last_id + 1)
else:
    new_id = "1001"

new_order = [new_id, product_name, quantity]
orders.append(new_order)

print()
print("New Order Added:")
print(f"{new_id},{product_name},{quantity}")

# Save everything to file
save_orders(orders)

print()
print("Order successfully saved to orders.txt")