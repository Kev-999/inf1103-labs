def display_all(inventory):
    print("\nCurrent Inventory")
    print("--------------------------------")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['quantity']}")
    print("--------------------------------")

if __name__ == "__main__":
    inventory = [
        {"id": "P001", "name": "Laptop", "price": 1200.00, "quantity": 15},
        {"id": "P002", "name": "Mouse", "price": 25.50, "quantity": 40},
        {"id": "P003", "name": "Keyboard", "price": 45.00, "quantity": 25}
    ]
    
    print("Inventory initialized with 3 products.")
    display_all(inventory)