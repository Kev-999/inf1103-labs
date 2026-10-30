import json
import os

class Product:
    
    def __init__(self, product_id, name, price, stock):
        self.__product_id = product_id
        self.__name = name
        self.__price = price
        self.__stock = stock

    
    def get_product_id(self):
        return self.__product_id

    def get_name(self):
        return self.__name

    def get_price(self):
        return self.__price

    def get_stock(self):
        return self.__stock

    def update_stock(self, quantity):
        self.__stock += quantity

    def display_information(self):
        print(f"ID: {self.__product_id} | Name: {self.__name} | "
              f"Price: ${self.__price:.2f} | Stock: {self.__stock}")

    def to_dict(self):
        return {
            "product_id": self.__product_id,
            "name": self.__name,
            "price": self.__price,
            "stock": self.__stock,
        }

class Inventory:

    def __init__(self):
        self.__products = []

    def add_product(self, product):
        self.__products.append(product)

    def search_product(self, keyword):
        keyword = keyword.strip().lower()
        return [
            p for p in self.__products
            if keyword in p.get_product_id().lower() or keyword in p.get_name().lower()
        ]

    def display_all(self):
        if not self.__products:
            print("The inventory is empty.")
            return
        print("=" * 52)
        for product in self.__products:
            product.display_information()
        print("=" * 52)

    def get_all_products(self):
        return self.__products


DATA_FILE = "inventory.json"


def load_inventory():
    inventory = Inventory()
    if os.path.exists(DATA_FILE):
        try:
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
            for item in data:
                product = Product(
                    item["product_id"],
                    item["name"],
                    item["price"],
                    item["stock"],
                )
                inventory.add_product(product)
            print(f"Loaded {len(data)} product(s) from {DATA_FILE}.")
        except (json.JSONDecodeError, KeyError, OSError):
            print(f"Warning: could not read {DATA_FILE}. "
                  "Starting with an empty inventory.")
    else:
        print(f"{DATA_FILE} not found. Starting with an empty inventory.")
    return inventory


def save_inventory(inventory):
    data = [product.to_dict() for product in inventory.get_all_products()]
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)
    print(f"Inventory saved to {DATA_FILE} ({len(data)} product(s)).")


def read_price():
    while True:
        try:
            return float(input("Price: "))
        except ValueError:
            print("Invalid price. Please enter a number.")


def read_stock():
    while True:
        try:
            return int(input("Stock quantity: "))
        except ValueError:
            print("Invalid stock. Please enter an integer.")


def add_product_flow(inventory):
    print("--- Add a new product ---")
    product_id = input("Product ID: ").strip()
    name = input("Name: ").strip()
    price = read_price()
    stock = read_stock()
    product = Product(product_id, name, price, stock)
    inventory.add_product(product)
    print(f"Product '{name}' added.")


def update_stock_flow(inventory):
    print("--- Update stock ---")
    keyword = input("Enter product ID or name to search: ").strip()
    matches = inventory.search_product(keyword)
    if not matches:
        print("No matching product found.")
        return

    product = matches[0]
    if len(matches) > 1:
        for i, p in enumerate(matches, 1):
            print(f"{i}. ", end="")
            p.display_information()
        try:
            choice = int(input("Multiple matches. Choose a number: "))
            product = matches[choice - 1]
        except (ValueError, IndexError):
            print("Invalid choice. Cancelled.")
            return

    quantity = read_stock()
    product.update_stock(quantity)
    print("Stock updated:")
    product.display_information()


def search_flow(inventory):
    keyword = input("Enter product ID or name to search: ").strip()
    matches = inventory.search_product(keyword)
    if not matches:
        print("No matching product found.")
    else:
        for product in matches:
            product.display_information()


def display_menu():
    print("\n===== Inventory Management System =====")
    print("1. Display all products")
    print("2. Add a product")
    print("3. Update stock")
    print("4. Search for a product")
    print("5. Save inventory")
    print("6. Exit")
    print("=======================================")


def main():
    inventory = load_inventory()

    while True:
        display_menu()
        choice = input("Enter your choice (1-6): ").strip()

        if choice == "1":
            inventory.display_all()
        elif choice == "2":
            add_product_flow(inventory)
        elif choice == "3":
            update_stock_flow(inventory)
        elif choice == "4":
            search_flow(inventory)
        elif choice == "5":
            save_inventory(inventory)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print("Invalid choice. Please enter a number from 1 to 6.")


if __name__ == "__main__":
    main()

