import json
import os

INVENTORY_FILE = "inventory.json"

def load_inventory():
    if os.path.exists(INVENTORY_FILE):
        print("inventory.json found.")
        with open(INVENTORY_FILE, "r") as file:
            data = json.load(file)
            print("Inventory loaded successfully.")
            return data.get("inventory", [])
    else:
        print("inventory.json not found. Starting with empty inventory.")
        return []

def display_all(inventory):
    print("\nCurrent Inventory")
    print("--------------------------------")
    for item in inventory:
        print(f"ID: {item['id']} | Name: {item['name']} | Price: ${item['price']:.2f} | Stock: {item['quantity']}")
    print("--------------------------------")

if __name__ == "__main__":
    inventory = load_inventory()
    display_all(inventory)