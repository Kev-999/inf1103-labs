
# Smart Inventory Auditor

# Initialize inventory to zero
inventory = 0

# Count the number of failed/rejected entries
failed_entries = 0

# Keep asking for stock quantities
while True:

    # Ask the user for a stock quantity
    user_input = input("Enter stock quantity (or 'quit' to exit): ")

    # Check if the user wants to quit
    if user_input.lower() == "quit":
        break

    # Check if the input is a valid number
    if not user_input.isdigit():
        print("Error: Invalid input. Please enter a number.")
        failed_entries += 1
        continue

    # Convert the input from string to integer
    quantity = int(user_input)

    # Reject negative numbers
    if quantity < 0:
        print("Error: Negative numbers are not allowed.")
        failed_entries += 1
        continue

    # Add the quantity to the inventory
    inventory += quantity

    print("Current inventory:", inventory)

    # Check if inventory exceeds 500
    if inventory > 500:
        print("OVERSTOCK ALERT! Inventory exceeds 500 units.")
        break

# Print the final report
print("\n--- Inventory Report ---")
print("Total Units Processed:", inventory)
print("Number of Failed/Rejected Entries:", failed_entries)

