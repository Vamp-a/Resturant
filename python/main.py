"""
Digital Restaurant – main.py
GKSS Richfield Bryanston · Exam Prep Workshop
Run this file to see the full restaurant system in action.
"""

from models import Restaurant, MenuItem
from utils import format_currency


def seed_menu(restaurant: Restaurant):
    """Populate the restaurant menu with South African-inspired dishes."""
    items = [
        # Starters
        MenuItem(1,  "Vetkoek with Mince",        "Starter",  45.00, "Deep-fried dough filled with spiced mince"),
        MenuItem(2,  "Peri-Peri Chicken Wings",   "Starter",  89.00, "Crispy wings with house peri-peri sauce"),
        MenuItem(3,  "Chakalaka Spring Rolls",    "Starter",  65.00, "Crispy rolls filled with chakalaka relish"),
        MenuItem(4,  "Boerewors Bites",           "Starter",  72.00, "Grilled mini boerewors with dipping sauces"),

        # Mains
        MenuItem(5,  "Bunny Chow (Mutton)",       "Main",    119.00, "Traditional Durban bunny chow"),
        MenuItem(6,  "Chakalaka Burger",          "Main",    105.00, "Beef patty, chakalaka, cheddar, brioche bun"),
        MenuItem(7,  "Boerewors Roll",            "Main",     85.00, "Classic South African street food"),
        MenuItem(8,  "Pap & Wors",               "Main",     95.00, "Pap, boerewors, tomato relish"),
        MenuItem(9,  "Durban Prawn Curry",        "Main",    189.00, "Spicy Durban prawn curry, rice, roti"),
        MenuItem(10, "Chicken Schnitzel",         "Main",    135.00, "Crumbed chicken, chips, coleslaw"),
        MenuItem(11, "Vegetarian Bobotie",        "Main",     98.00, "Cape Malay bobotie, yellow rice, chutney"),
        MenuItem(12, "Grilled Kingklip",          "Main",    215.00, "Line fish, lemon butter, seasonal veg"),

        # Desserts
        MenuItem(13, "Malva Pudding",             "Dessert",  58.00, "Warm malva, vanilla custard or ice cream"),
        MenuItem(14, "Koeksister",                "Dessert",  38.00, "Syrup-soaked plaited doughnuts"),
        MenuItem(15, "Milk Tart",                "Dessert",  45.00, "Traditional melktert, cinnamon dusting"),
        MenuItem(16, "Amarula Cheesecake",        "Dessert",  72.00, "Baked cheesecake with Amarula cream"),

        # Drinks
        MenuItem(17, "Rooibos Iced Tea",          "Drink",    35.00, "Sweetened rooibos, lemon, mint"),
        MenuItem(18, "Springbokkies",             "Drink",    45.00, "Layered green crème de menthe & Amarula"),
        MenuItem(19, "Craft Lager (500ml)",       "Drink",    58.00, "Local craft lager on tap"),
        MenuItem(20, "Mango Lassi",               "Drink",    42.00, "Fresh mango, yoghurt, cardamom"),
        MenuItem(21, "Still Water (750ml)",       "Drink",    22.00, "Chilled still water"),
        MenuItem(22, "Sparkling Water (750ml)",   "Drink",    25.00, "Chilled sparkling water"),
        MenuItem(23, "Cape Winelands Red",        "Drink",    85.00, "Glass of house red wine"),
        MenuItem(24, "Cape Winelands White",      "Drink",    85.00, "Glass of house white wine"),
    ]
    for item in items:
        restaurant.menu.add_item(item)


def run_demo():
    print("\n" + "="*60)
    print("  THE DIGITAL RESTAURANT – System Demo")
    print("  GKSS Richfield Bryanston – Exam Prep Workshop")
    print("="*60 + "\n")

    # ── 1. Create restaurant ──
    resto = Restaurant("Ubuntu Kitchen", "14 Innovation Ave, Bryanston")

    # ── 2. Build the menu ──
    print("Loading menu...")
    seed_menu(resto)
    resto.menu.display()

    # ── 3. Register customers ──
    print("Registering customers...")
    alice = resto.register_customer("Alice Dlamini", "alice@example.co.za", "0821234567")
    bob   = resto.register_customer("Bob Ndlovu",   "bob@example.co.za",   "0739876543")
    carol = resto.register_customer("Carol Mokoena","carol@example.co.za", "0611234567")

    # ── 4. Place orders ──
    print("\nPlacing orders...\n")

    # Alice's order
    order1 = resto.place_order(alice, table_number=4)
    order1.add_item(resto.menu.find_by_name("Vetkoek"), 1)
    order1.add_item(resto.menu.find_by_name("Bunny Chow"), 1)
    order1.add_item(resto.menu.find_by_name("Malva Pudding"), 1)
    order1.add_item(resto.menu.find_by_name("Rooibos Iced Tea"), 2)
    order1.notes = "No coriander in the bunny chow please."
    order1.status = "confirmed"
    order1.status = "preparing"
    order1.status = "served"
    order1.print_receipt()

    # Bob's order
    order2 = resto.place_order(bob, table_number=7)
    order2.add_item(resto.menu.find_by_name("Boerewors Roll"), 2)
    order2.add_item(resto.menu.find_by_name("Craft Lager"), 2)
    order2.add_item(resto.menu.find_by_name("Koeksister"), 2)
    order2.status = "confirmed"
    order2.status = "served"
    order2.print_receipt()

    # Carol's order
    order3 = resto.place_order(carol, table_number=2)
    order3.add_item(resto.menu.find_by_name("Peri-Peri Chicken Wings"), 1)
    order3.add_item(resto.menu.find_by_name("Durban Prawn Curry"), 1)
    order3.add_item(resto.menu.find_by_name("Amarula Cheesecake"), 1)
    order3.add_item(resto.menu.find_by_name("Cape Winelands White"), 2)
    order3.status = "confirmed"
    order3.print_receipt()

    # ── 5. Analytics ──
    print(f"\n{'='*46}")
    print(f"  RESTAURANT ANALYTICS")
    print(f"{'─'*46}")
    print(f"  Total Revenue (served orders): {format_currency(resto.total_revenue())}")
    print(f"  Active Orders:                 {len(resto.active_orders())}")
    print(f"\n  Top Ordered Items:")
    for name, qty in resto.top_ordered_items(5):
        print(f"    {name:<30} {qty} ordered")
    print(f"{'='*46}\n")

    # ── 6. Menu sorting demo ──
    print("Menu sorted cheapest → most expensive:")
    for item in resto.menu.sort_by_price(ascending=True)[:5]:
        print(f"  {item.name:<35} {format_currency(item.price)}")

    print("\nMenu sorted most expensive → cheapest:")
    for item in resto.menu.sort_by_price(ascending=False)[:5]:
        print(f"  {item.name:<35} {format_currency(item.price)}")


if __name__ == "__main__":
    run_demo()