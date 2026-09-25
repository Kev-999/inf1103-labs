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

# --- Main Program (Phase A) ---
orders = load_orders()

print("Current Orders:")
print()
for order in orders:
    print(f"{order[0]}, {order[1]}, {order[2]}")