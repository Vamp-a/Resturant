import csv
import os

# ════════════════════════════════════════════════════════════════
#  SECTION 1: THE MESSY DATA (Denormalised - Violates 1NF)
# ════════════════════════════════════════════════════════════════
# Each row has repeating groups: Dish1, Price1, Qty1, Dish2, Price2...
# This violates 1NF because there are multiple values in one row.

messy_orders = [
    {
        "OrderID": 1001,
        "Customer": "Alice",
        "Date": "2026-06-20",
        "Dish1": "Vetkoek", "Price1": 45.00, "Qty1": 1,
        "Dish2": "Bunny Chow", "Price2": 119.00, "Qty2": 1,
        "Dish3": "Malva Pudding", "Price3": 58.00, "Qty3": 1,
        "Dish4": "Rooibos Tea", "Price4": 35.00, "Qty4": 2,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 357.00
    },
    {
        "OrderID": 1002,
        "Customer": "Bob",
        "Date": "2026-06-20",
        "Dish1": "Boerewors Roll", "Price1": 85.00, "Qty1": 2,
        "Dish2": "Craft Lager", "Price2": 58.00, "Qty2": 2,
        "Dish3": "Koeksister", "Price3": 38.00, "Qty3": 2,
        "Dish4": None, "Price4": None, "Qty4": None,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 362.00
    },
    {
        "OrderID": 1003,
        "Customer": "Carol",
        "Date": "2026-06-21",
        "Dish1": "Peri-Peri Wings", "Price1": 89.00, "Qty1": 1,
        "Dish2": "Prawn Curry", "Price2": 189.00, "Qty2": 1,
        "Dish3": "Amarula Cheesecake", "Price3": 72.00, "Qty3": 1,
        "Dish4": "White Wine", "Price4": 85.00, "Qty4": 2,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 520.00
    },
    {
        "OrderID": 1004,
        "Customer": "David",
        "Date": "2026-06-21",
        "Dish1": "Chakalaka Burger", "Price1": 105.00, "Qty1": 1,
        "Dish2": "Pap & Wors", "Price2": 95.00, "Qty2": 1,
        "Dish3": "Milk Tart", "Price3": 45.00, "Qty3": 1,
        "Dish4": "Craft Lager", "Price4": 58.00, "Qty4": 1,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 303.00
    },
    {
        "OrderID": 1005,
        "Customer": "Amara",
        "Date": "2026-06-23",
        "Dish1": "Veg Bunny", "Price1": 95.00, "Qty1": 1,
        "Dish2": "Veg Bobotie", "Price2": 98.00, "Qty2": 1,
        "Dish3": "Peppermint Crisp", "Price3": 52.00, "Qty3": 1,
        "Dish4": "Rooibos Tea", "Price4": 35.00, "Qty4": 1,
        "Dish5": "Mango Lassi", "Price5": 42.00, "Qty5": 1,
        "Total": 322.00
    },
    {
        "OrderID": 1006,
        "Customer": "Alice",
        "Date": "2026-06-22",
        "Dish1": "Braai Platter", "Price1": 299.00, "Qty1": 1,
        "Dish2": "Red Wine", "Price2": 85.00, "Qty2": 2,
        "Dish3": "Malva Pudding", "Price3": 58.00, "Qty3": 2,
        "Dish4": None, "Price4": None, "Qty4": None,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 585.00
    },
    {
        "OrderID": 1007,
        "Customer": "Zara",
        "Date": "2026-06-27",
        "Dish1": "Chicken Schnitzel", "Price1": 135.00, "Qty1": 1,
        "Dish2": "Still Water", "Price2": 22.00, "Qty2": 1,
        "Dish3": None, "Price3": None, "Qty3": None,
        "Dish4": None, "Price4": None, "Qty4": None,
        "Dish5": None, "Price5": None, "Qty5": None,
        "Total": 157.00
    },
]


# ════════════════════════════════════════════════════════════════
#  SECTION 2: CATEGORY GUESSING FUNCTION
# ════════════════════════════════════════════════════════════════
# This assigns each dish to a category. In a real system,
# categories would be stored in a separate lookup table.

def guess_category(dish_name):
    """Determine the category of a dish based on its name."""
    starters = ["Vetkoek", "Peri-Peri", "Chakalaka", "Boerewors Bites", "Umngqusho"]
    mains = ["Bunny Chow", "Burger", "Boerewors Roll", "Pap & Wors", "Prawn Curry",
             "Schnitzel", "Bobotie", "Kingklip", "Braai Platter"]
    desserts = ["Malva", "Koeksister", "Milk Tart", "Cheesecake", "Crisp Tart", "Peppermint"]
    drinks = ["Rooibos", "Mango Lassi", "Lager", "Springbokkies", "Water", "Wine", "OJ"]

    for s in starters:
        if s in dish_name:
            return "Starter"
    for m in mains:
        if m in dish_name:
            return "Main"
    for d in desserts:
        if d in dish_name:
            return "Dessert"
    for d in drinks:
        if d in dish_name:
            return "Drink"
    return "Main"  # default


# ════════════════════════════════════════════════════════════════
#  SECTION 3: NORMALISATION FUNCTION
# ════════════════════════════════════════════════════════════════

def normalise_to_3nf(messy_orders):
    """
    Normalise messy restaurant order data to 3NF.

    Returns a dictionary containing 5 normalised tables:
        - customers:  {customer_id: {name, email, phone}}
        - categories: {category_id: {name, description}}
        - menu_items: {item_id: {name, price, category_id}}
        - orders:     {order_id: {customer_id, order_date, status, notes}}
        - order_items: list of {order_item_id, order_id, item_id, quantity, unit_price}
    """

    # Step 1: Initialise empty structures 
    customers = {}      # customer_id -> {name, email, phone}
    categories = {}     # category_id -> {name, description}
    menu_items = {}     # item_id -> {name, price, category_id}
    orders = {}         # order_id -> {customer_id, order_date, status, notes}
    order_items = []    # list of order item rows

    # Step 2: ID counters 
    next_customer_id = 1
    next_category_id = 1
    next_item_id = 1
    next_order_id = 1
    next_order_item_id = 1

    # Step 3: Helper functions
    def get_customer_id(name):
        """Get existing customer ID or create a new one."""
        nonlocal next_customer_id
        # Search existing customers
        for cid, data in customers.items():
            if data["name"] == name:
                return cid
        # Create new customer
        customers[next_customer_id] = {
            "name": name,
            "email": f"{name.lower()}@example.co.za",
            "phone": ""
        }
        cid = next_customer_id
        next_customer_id += 1
        return cid

    def get_category_id(category_name):
        """Get existing category ID or create a new one."""
        nonlocal next_category_id
        for cat_id, data in categories.items():
            if data["name"] == category_name:
                return cat_id
        categories[next_category_id] = {
            "name": category_name,
            "description": f"{category_name} dishes"
        }
        cat_id = next_category_id
        next_category_id += 1
        return cat_id

    def get_item_id(dish_name, price, category_name="Main"):
        """Get existing menu item ID or create a new one."""
        nonlocal next_item_id
        # Search existing menu items
        for item_id, data in menu_items.items():
            if data["name"] == dish_name:
                return item_id
        # Create new menu item
        cat_id = get_category_id(category_name)
        menu_items[next_item_id] = {
            "name": dish_name,
            "price": price,
            "category_id": cat_id
        }
        item_id = next_item_id
        next_item_id += 1
        return item_id

    # Step 4: Process each order
    for messy in messy_orders:
        # 4a: Get or create customer
        customer_id = get_customer_id(messy["Customer"])

        # 4b: Create the order
        orders[next_order_id] = {
            "customer_id": customer_id,
            "order_date": messy["Date"],
            "status": "served",
            "notes": ""
        }
        order_id = next_order_id
        next_order_id += 1

        # 4c: Process each dish in the order (up to 5 dishes per order)
        for i in range(1, 6):  # Dish1, Dish2, Dish3, Dish4, Dish5
            dish_name = messy.get(f"Dish{i}")
            price = messy.get(f"Price{i}")
            qty = messy.get(f"Qty{i}")

            if dish_name and price is not None and qty:
                # Guess the category
                category = guess_category(dish_name)
                # Get or create menu item
                item_id = get_item_id(dish_name, price, category)
                # Add to order_items
                order_items.append({
                    "order_item_id": next_order_item_id,
                    "order_id": order_id,
                    "item_id": item_id,
                    "quantity": qty,
                    "unit_price": price
                })
                next_order_item_id += 1

    # Step 5: Return all tables
    return {
        "customers": customers,
        "categories": categories,
        "menu_items": menu_items,
        "orders": orders,
        "order_items": order_items
    }


# ════════════════════════════════════════════════════════════════
#  SECTION 4: DISPLAY RESULTS
# ════════════════════════════════════════════════════════════════

def display_results(result):
    """Pretty print all normalised tables."""
    print("\n" + "=" * 70)
    print("  NORMALISED DATA (3NF) - All Tables")
    print("=" * 70)

    print("\n🔹 CUSTOMERS")
    print("-" * 50)
    print(f"  {'ID':<5} {'Name':<15} {'Email':<25}")
    for cid, data in sorted(result["customers"].items()):
        print(f"  {cid:<5} {data['name']:<15} {data['email']:<25}")

    print("\n🔹 CATEGORIES")
    print("-" * 50)
    print(f"  {'ID':<5} {'Name':<15} {'Description':<25}")
    for cat_id, data in sorted(result["categories"].items()):
        print(f"  {cat_id:<5} {data['name']:<15} {data['description']:<25}")

    print("\n🔹 MENU ITEMS")
    print("-" * 50)
    print(f"  {'ID':<5} {'Name':<25} {'Price':<10} {'Category':<10}")
    for item_id, data in sorted(result["menu_items"].items()):
        print(f"  {item_id:<5} {data['name']:<25} R{data['price']:<9.2f} {data['category_id']:<10}")

    print("\n🔹 ORDERS")
    print("-" * 50)
    print(f"  {'Order ID':<10} {'Customer ID':<12} {'Date':<12} {'Status':<10}")
    for order_id, data in sorted(result["orders"].items()):
        print(f"  {order_id:<10} {data['customer_id']:<12} {data['order_date']:<12} {data['status']:<10}")

    print("\n🔹 ORDER ITEMS (First 10 rows)")
    print("-" * 65)
    print(f"  {'Item ID':<10} {'Order ID':<10} {'Menu Item ID':<12} {'Qty':<8} {'Unit Price':<10}")
    for oi in result["order_items"][:10]:
        print(f"  {oi['order_item_id']:<10} {oi['order_id']:<10} {oi['item_id']:<12} {oi['quantity']:<8} R{oi['unit_price']:<9.2f}")
    if len(result["order_items"]) > 10:
        print(f"  ... and {len(result['order_items']) - 10} more rows")


# ════════════════════════════════════════════════════════════════
#  SECTION 5: EXPORT TO CSV
# ════════════════════════════════════════════════════════════════

def export_to_csv(result, folder="normalised_data"):
    """Export each normalised table to a CSV file."""
    os.makedirs(folder, exist_ok=True)

    # 5.1: Customers
    with open(f"{folder}/customers.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["customer_id", "first_name", "last_name", "email", "phone"])
        for cid, data in sorted(result["customers"].items()):
            parts = data["name"].split()
            first = parts[0] if parts else ""
            last = " ".join(parts[1:]) if len(parts) > 1 else ""
            writer.writerow([cid, first, last, data["email"], data["phone"]])

    # 5.2: Categories
    with open(f"{folder}/categories.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["category_id", "name", "description"])
        for cat_id, data in sorted(result["categories"].items()):
            writer.writerow([cat_id, data["name"], data["description"]])

    # 5.3: Menu Items
    with open(f"{folder}/menu_items.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["item_id", "name", "category_id", "price", "description"])
        for item_id, data in sorted(result["menu_items"].items()):
            writer.writerow([item_id, data["name"], data["category_id"], data["price"], ""])

    # 5.4: Orders
    with open(f"{folder}/orders.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_id", "customer_id", "created_at", "status", "notes"])
        for order_id, data in sorted(result["orders"].items()):
            writer.writerow([order_id, data["customer_id"], data["order_date"], data["status"], data["notes"]])

    # 5.5: Order Items
    with open(f"{folder}/order_items.csv", "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["order_item_id", "order_id", "item_id", "quantity", "unit_price"])
        for oi in result["order_items"]:
            writer.writerow([oi["order_item_id"], oi["order_id"], oi["item_id"], oi["quantity"], oi["unit_price"]])

    print(f"\n Exported {len(result['customers'])} customers, {len(result['categories'])} categories, "
          f"{len(result['menu_items'])} menu items, {len(result['orders'])} orders, "
          f"and {len(result['order_items'])} order items to '{folder}/'")
    print(f"   Look inside '{folder}/' for your CSV files.")


# ════════════════════════════════════════════════════════════════
#  SECTION 6: MAIN EXECUTION
# ════════════════════════════════════════════════════════════════

if __name__ == "__main__":
    print("\n" + "=" * 70)
    print("  THE DIGITAL RESTAURANT - DATA NORMALISATION")
    print("  GKSS Richfield Bryanston - Exam Prep Workshop")
    print("  Taking messy, denormalised data → 3NF")
    print("=" * 70)

    print("\n Input: 7 messy orders with repeating groups (Dish1, Dish2, ...)")
    print("   This violates 1NF - each row has multiple values in one field.")

    # Normalise the data
    result = normalise_to_3nf(messy_orders)

    # Display results 
    display_results(result)

    # Export to CSV 
    export_to_csv(result)

    print("\n" + "=" * 70)
    print("  Normalisation complete!")
    print("  Concept: Denormalised (repeating groups) → 1NF → 2NF → 3NF")
    print("  Tables now have no redundancy, no repeating groups.")
    print("=" * 70)