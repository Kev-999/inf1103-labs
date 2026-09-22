failed_attempts = 0


def get_valid_input():
    global failed_attempts

    while True:
        user_input = input("Enter stock quantity (or 'quit' to finish): ")

        if user_input.lower() == "quit":
            return "quit"

        if user_input.isdigit():
            return int(user_input)

        failed_attempts += 1
        print("Invalid input. Please enter a positive integer or 'quit'.")


def process_delivery(current_total, new_value):
    new_total = current_total + new_value
    return new_total


def calculate_tax(amount):
    tax = amount * 0.10
    return tax


def generate_report(total_units, failed_attempts):
    print("\n--- Final Report ---")
    print("Total Units Processed:", total_units)
    print("Total Deliveries Processed:", deliveries_processed)
    print("Number of Failed/Rejected Entries:", failed_attempts)


# Main program
inventory = 0
deliveries_processed = 0

while True:
    value = get_valid_input()

    if value == "quit":
        break

    inventory = process_delivery(inventory, value)

    tax = calculate_tax(value)

    deliveries_processed += 1

    print("Delivery:", value)
    print("Tax (10%):", tax)
    print("Current Total:", inventory)


generate_report(inventory, failed_attempts)