import json
import os

INVENTORY_FILE = "inventory.json"

def load_inventory():
    """Load inventory from JSON file if it exists."""
    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
            print("Inventory loaded successfully.")
            return data.get("inventory", [])
    else:
        print("inventory.json not found. Starting with empty inventory.")
        return []

def save_inventory(inventory):
    """Save inventory to JSON file."""
    with open(INVENTORY_FILE, "w") as file:
        json.dump({"inventory": inventory}, file, indent=4)

def display_all(inventory):
    """Display all products in the inventory."""
    print("\nCurrent Inventory")
    print("--------------------------------")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['quantity']}")
    print("--------------------------------")

def add_product(inventory):
    """Add a new product to the inventory."""
    print("\nAdd New Product")
    product_id = input("Product ID: ")
    name = input("Product Name: ")
    price = float(input("Price: "))
    quantity = int(input("Stock Quantity: "))
    
    new_product = {
        "id": product_id,
        "name": name,
        "price": price,
        "quantity": quantity
    }
    inventory.append(new_product)
    print("\nProduct added successfully!")

def update_stock(inventory):
    """Update the stock quantity of an existing product."""
    print("\nUpdate Stock")
    product_id = input("Enter Product ID: ")
    
    for item in inventory:
        if item["id"] == product_id:
            print("\nProduct Found:")
            print(f"Name: {item['name']}")
            print(f"Current Stock: {item['quantity']}")
            
            new_quantity = int(input("\nNew Stock Quantity: "))
            item["quantity"] = new_quantity
            print("\nStock updated successfully!")
            return
            
    print("\nProduct not found.")

def search_product(inventory):
    """Search for a product by ID."""
    print("\nSearch Product")
    product_id = input("Enter Product ID: ")
    
    for item in inventory:
        if item["id"] == product_id:
            print("\nProduct Found")
            print("--------------------------------")
            print(f"ID: {item['id']}")
            print(f"Name: {item['name']}")
            print(f"Price: ${item['price']:.2f}")
            print(f"Stock: {item['quantity']}")
            print("--------------------------------")
            return
            
    print("\nProduct not found.")

def main():
    inventory = load_inventory()
    
    while True:
        print("\n---------- MENU ----------")
        print("1. Display All Products")
        print("2. Add Product")
        print("3. Update Stock")
        print("4. Search Product")
        print("5. Save Inventory")
        print("6. Exit")
        print("--------------------------")
        
        option = input("\nEnter option: ")
        
        if option == "1":
            display_all(inventory)
        elif option == "2":
            add_product(inventory)
        elif option == "3":
            update_stock(inventory)
        elif option == "4":
            search_product(inventory)
        elif option == "5":
            print("\nSaving inventory...")
            save_inventory(inventory)
            print("Inventory saved successfully to inventory.json.")
        elif option == "6":
            print("\nSaving inventory before exit...")
            save_inventory(inventory)
            print("Inventory saved successfully.")
            print("Thank you for using Inventory Management System.")
            print("Program terminated.")
            break
        else:
            print("\nInvalid option. Please try again.")

if __name__ == "__main__":
    main()