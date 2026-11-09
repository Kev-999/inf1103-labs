from abc import ABC, abstractmethod
import json
import os

class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost(self):
        pass

class Supplier:
    def __init__(self, supplier_id: str, name: str, contact_email: str):
        self.supplier_id: str = supplier_id
        self.name: str = name
        self.contact_email: str = contact_email

    def display_information(self) -> None:
        print(f"Supplier ID: {self.supplier_id}, Name: {self.name}, Email: {self.contact_email}")

class Product(ABC):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier):
        self.product_id: str = product_id
        self.name: str = name
        self.price: float = price
        self.stock_quantity: int = stock_quantity
        self.supplier: Supplier = supplier

    def update_stock(self, change: int) -> None:
        self.stock_quantity += change

    def display_information(self) -> None:
        print(f"ID: {self.product_id}, Name: {self.name}, Price: ${self.price:.2f}, Stock: {self.stock_quantity}")

    @abstractmethod
    def get_fulfilment_info(self) -> str:
        pass

class PhysicalProduct(Product, CanBeShipped):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, weight: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.weight: float = weight

    def display_information(self) -> None:
        super().display_information()
        print(f"  Weight: {self.weight} kg")

    def get_fulfilment_info(self) -> str:
        return "This product requires physical shipping."

    def calculate_shipping_cost(self) -> float:
        # simple rule: $2.5 per kg
        return round(self.weight * 2.5, 2)

class DigitalProduct(Product):
    def __init__(self, product_id: str, name: str, price: float, stock_quantity: int, supplier: Supplier, download_size: float):
        super().__init__(product_id, name, price, stock_quantity, supplier)
        self.download_size: float = download_size

    def display_information(self) -> None:
        super().display_information()
        print(f"  Download size: {self.download_size} MB")

    def get_fulfilment_info(self) -> str:
        return "This product will be delivered via digital download."

class Inventory:
    def __init__(self):
        self.products: dict[str, Product] = {}  # key: product_id, value: Product object
        self.filename: str = "inventory3.json"

    def add_product(self, product: Product) -> None:
        self.products[product.product_id] = product

    def remove_product(self, product_id: str) -> None:
        if product_id in self.products:
            del self.products[product_id]

    def find_product(self, product_id: str) -> Product | None:
        return self.products.get(product_id)

    def display_all_products(self) -> None:
        if not self.products:
            print("Inventory is empty.")
            return
        for p in self.products.values():
            p.display_information()
            print(f"  Fulfilment: {p.get_fulfilment_info()}")
            if isinstance(p, CanBeShipped):
                print(f"  Shipping cost: ${p.calculate_shipping_cost():.2f}")
            print("-" * 50)

    def update_product_stock(self, pid: str, delta: int) -> bool:
        if pid in self.products:
            self.products[pid].update_stock(delta)
            return True
        return False

    def save_to_json(self) -> None:
        data_list = []
        for p in self.products.values():
            base = {
                "product_id": p.product_id,
                "name": p.name,
                "price": p.price,
                "stock_quantity": p.stock_quantity,
                "supplier_id": p.supplier.supplier_id,
                "supplier_name": p.supplier.name,
                "supplier_email": p.supplier.contact_email
            }
            if isinstance(p, PhysicalProduct):
                base["type"] = "physical"
                base["weight"] = p.weight
            elif isinstance(p, DigitalProduct):
                base["type"] = "digital"
                base["download_size"] = p.download_size
            data_list.append(base)
        with open(self.filename, "w", encoding="utf-8") as f:
            json.dump(data_list, f, indent=2)

    def load_from_json(self) -> None:
        if not os.path.exists(self.filename):
            print(f"Note: {self.filename} not found, starting empty inventory.")
            return
        try:
            with open(self.filename, "r", encoding="utf-8") as f:
                data_list = json.load(f)
        except json.JSONDecodeError:
            print("Error: JSON file corrupted, starting empty inventory.")
            return

        self.products.clear()
        for item in data_list:
            
            sup = Supplier(item["supplier_id"], item["supplier_name"], item["supplier_email"])
            if item["type"] == "physical":
                prod = PhysicalProduct(
                    item["product_id"],
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    sup,
                    item["weight"]
                )
            elif item["type"] == "digital":
                prod = DigitalProduct(
                    item["product_id"],
                    item["name"],
                    item["price"],
                    item["stock_quantity"],
                    sup,
                    item["download_size"]
                )
            else:
                continue
            self.add_product(prod)

class OrderLine:
    def __init__(self, product: Product, quantity: int):
        self.product: Product = product
        self.quantity: int = quantity

    def calculate_subtotal(self) -> float:
        return self.product.price * self.quantity

class Order:
    def __init__(self, order_id: str):
        self.order_id: str = order_id
        self.order_lines: list[OrderLine] = []

    def add_order_line(self, product: Product, quantity: int) -> None:
        
        line = OrderLine(product, quantity)
        self.order_lines.append(line)

    def calculate_total(self) -> float:
        total = 0.0
        for line in self.order_lines:
            total += line.calculate_subtotal()
        return round(total, 2)

def show_product_details(product: Product) -> None:
    product.display_information()
    print(product.get_fulfilment_info())

def main():
    inv = Inventory()
    inv.load_from_json()
    while True:
        print("\n===== Inventory Management System =====")
        print("1. Add new product (NOTE: menu will crash, need supplier object)")
        print("2. Display all products")
        print("3. Update stock quantity")
        print("4. Search product by ID")
        print("5. Save inventory to JSON")
        print("6. Load inventory from JSON")
        print("0. Exit")
        choice = input("Enter your choice: ")

        if choice == "1":
            print("WARNING: This menu cannot create products, need Supplier instance! Use lab test code.")
            continue

        elif choice == "2":
            inv.display_all_products()

        elif choice == "3":
            pid = input("Enter product ID to adjust stock: ")
            delta = int(input("Stock change (+add / -remove): "))
            ok = inv.update_product_stock(pid, delta)
            print("Stock updated." if ok else "Product not found.")

        elif choice == "4":
            pid = input("Search product ID: ")
            found = inv.find_product(pid)
            if found:
                found.display_information()
                print(f"Fulfilment info: {found.get_fulfilment_info()}")
            else:
                print("Not found.")

        elif choice == "5":
            inv.save_to_json()
            print("Saved to inventory3.json")

        elif choice == "6":
            inv.load_from_json()
            print("Loaded from inventory3.json")

        elif choice == "0":
            inv.save_to_json()
            print("Exiting. Inventory saved.")
            break
        else:
            print("Invalid option, try again.")

if __name__ == "__main__":
    
    print("==== Running Lab8 Object Relationship Tests ====")

    
    sup1 = Supplier("S01", "TechSupplier Inc", "contact@techsupplier.com")
    p1 = PhysicalProduct("P01", "Laptop", 999.99, 10, sup1, 2.2)
    p2 = DigitalProduct("D01", "E‑Book", 12.99, 50, sup1, 15.0)

    print("\n-- Product accessing supplier info --")
    p1.supplier.display_information()
    p2.supplier.display_information()

    
    del sup1
    print("\nAfter del sup1 variable, product still can show supplier:")
    p1.supplier.display_information()

    
    inv_a = Inventory()
    inv_b = Inventory()
    inv_a.add_product(p1)
    print("\nBefore remove from inv_a, find:", inv_a.find_product("P01"))
    inv_a.remove_product("P01")
    print("After remove from inv_a, find in inv_a:", inv_a.find_product("P01"))
    print("But p1 object still exists, name =", p1.name)
    inv_b.add_product(p1)
    print("Added same p1 to inv_b, find in inv_b:", inv_b.find_product("P01").name)

    
    ord1 = Order("ORD‑001")
    ord2 = Order("ORD‑002")
    ord1.add_order_line(p1, 2)
    ord1.add_order_line(p2, 1)
    ord2.add_order_line(p1, 1)  

    print(f"\nOrder1 total: ${ord1.calculate_total()}")
    print(f"Order2 total: ${ord2.calculate_total()}")
    print(f"Number of OrderLines ord1:{len(ord1.order_lines)}, ord2:{len(ord2.order_lines)}")

    
    print("\n--- show_product_details LSP test ---")
    show_product_details(p1)
    show_product_details(p2)

    