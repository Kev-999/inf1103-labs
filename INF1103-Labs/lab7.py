from abc import ABC, abstractmethod
import json
import os

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass


class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int):
        self.product_id = product_id
        self.name = name
        self.price = price
        self.stock_quantity = stock_quantity

    def update_stock(self, change: int):
        self.stock_quantity += change

    def display_information(self):
        print(f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock_quantity}")

    @abstractmethod
    def get_fulfilment_info(self):
        pass


class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, weight: float):
        super().__init__(product_id, name, price, stock_quantity)
        self.weight = weight

    def display_information(self):
        super().display_information()
        print(f"  Weight: {self.weight} kg")

    def get_fulfilment_info(self):
        return "This product requires physical shipping."

    def calculate_shipping_cost(self):
        # simple rule: $2.5 per kg
        return round(self.weight * 2.5, 2)


class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, download_size: float):
        super().__init__(product_id, name, price, stock_quantity)
        self.download_size = download_size

    def display_information(self):
        super().display_information()
        print(f"  Download size: {self.download_size} MB")

    def get_fulfilment_info(self):
        return "This product will be delivered via digital download."


class Inventory:
    def __init__(self):
        self.products = {}  # key: product_id, value: Product object

    def add_product(self, product: Product):
        self.products[product.product_id] = product

    def display_all_products(self):
        if not self.products:
            print("Inventory is empty.")
            return
        for p in self.products.values():
            p.display_information()
            print(f"  Fulfilment: {p.get_fulfilment_info()}")
            if isinstance(p, CanBeShipped):
                print(f"  Shipping cost: ${p.calculate_shipping_cost():.2f}")
            print("-" * 50)

    def update_product_stock(self, pid: str, delta: int):
        if pid in self.products:
            self.products[pid].update_stock(delta)
            return True
        return False

    def search_product(self, pid: str):
        return self.products.get(pid)

    def save_to_json(self, filename="inventory3.json"):
        data_list = []
        for p in self.products.values():
            base = {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock_quantity": p.stock_quantity
            }
            if isinstance(p, PhysicalProduct):
                base["type"] = "physical"
                base["weight"] = p.weight
            elif isinstance(p, DigitalProduct):
                base["type"] = "digital"
                base["download_size"] = p.download_size
            data_list.append(base)
        with open(filename, "w") as f:
            json.dump(data_list, f, indent=2)

    def load_from_json(self, filename="inventory.json"):
        if not os.path.exists(filename):
            return
        with open(filename, "r") as f:
            data_list = json.load(f)
        self.products.clear()
        for item in data_list:
            if item["type"] == "physical":
                prod = PhysicalProduct(
                    item["product_id"],
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    item["weight"]
                )
            elif item["type"] == "digital":
                prod = DigitalProduct(
                    item["product_id"],
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    item["download_size"]
                )
            else:
                continue
            self.add_product(prod)


def main():
    inv = Inventory()
    inv.load_from_json()
    while True:
        print("\n===== Inventory Management System =====")
        print("1. Add new product")
        print("2. Display all products")
        print("3. Update stock quantity")
        print("4. Search product by ID")
        print("5. Save inventory to JSON")
        print("6. Load inventory from JSON")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            pid = input("Product ID: ")
            name = input("Product name: ")
            price = float(input("Price: "))
            stock = int(input("Stock quantity: "))
            print("\nProduct type:")
            print("1 - Physical Product")
            print("2 - Digital Product")
            t = input("Select type (1/2): ")
            if t == "1":
                w = float(input("Weight (kg): "))
                new_p = PhysicalProduct(pid, name, price, stock, w)
            elif t == "2":
                ds = float(input("Download size (MB): "))
                new_p = DigitalProduct(pid, name, price, stock, ds)
            else:
                print("Invalid type.")
                continue
            inv.add_product(new_p)
            print("Product added.")

        elif choice == "2":
            inv.display_all_products()

        elif choice == "3":
            pid = input("Enter product ID to adjust stock: ")
            delta = int(input("Stock change (+add / -remove): "))
            ok = inv.update_product_stock(pid, delta)
            print("Stock updated." if ok else "Product not found.")

        elif choice == "4":
            pid = input("Search product ID: ")
            found = inv.search_product(pid)
            if found:
                found.display_information()
                print(f"Fulfilment info: {found.get_fulfilment_info()}")
            else:
                print("Not found.")

        elif choice == "5":
            inv.save_to_json()
            print("Saved to inventory.json")

        elif choice == "6":
            inv.load_from_json()
            print("Loaded from inventory.json")

        elif choice == "0":
            inv.save_to_json()
            print("Exiting. Inventory saved.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    main()