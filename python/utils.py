"""
Digital Restaurant – utils.py
GKSS Richfield Bryanston · Exam Prep Workshop
Functions Module: Calculations, Sorting, Debugging Exercises
"""

from typing import Any

# ─────────────────────────────────────────────────────────────
#  SECTION 1: BILL CALCULATION FUNCTIONS
#  These are the core exam-relevant functions
# ─────────────────────────────────────────────────────────────

VAT_RATE = 0.15
SERVICE_CHARGE_RATE = 0.10


def calculate_subtotal(items: list[dict]) -> float:
    """
    Calculate subtotal from a list of order items.
    Each item is a dict: {"name": str, "price": float, "qty": int}

    Example:
        items = [
            {"name": "Burger", "price": 89.99, "qty": 2},
            {"name": "Coke",   "price": 22.50, "qty": 1},
        ]
        calculate_subtotal(items) → 202.48
    """
    total = 0.0
    for item in items:
        total += item["price"] * item["qty"]
    return round(total, 2)


def calculate_vat(subtotal: float, rate: float = VAT_RATE) -> float:
    """Return the VAT amount for a given subtotal."""
    return round(subtotal * rate, 2)


def calculate_service_charge(subtotal: float, rate: float = SERVICE_CHARGE_RATE) -> float:
    """Return the service charge amount."""
    return round(subtotal * rate, 2)


def calculate_total_bill(items: list[dict],
                         include_vat: bool = True,
                         include_service: bool = True) -> dict:
    """
    Full bill breakdown.
    Returns a dict with subtotal, vat, service_charge, and total.
    """
    subtotal = calculate_subtotal(items)
    vat = calculate_vat(subtotal) if include_vat else 0.0
    service = calculate_service_charge(subtotal) if include_service else 0.0
    total = round(subtotal + vat + service, 2)

    return {
        "subtotal": subtotal,
        "vat": vat,
        "service_charge": service,
        "total": total,
    }


def apply_discount(price: float, percent: float) -> float:
    """
    Apply a percentage discount to a price.
    Raises ValueError for invalid percentages.
    """
    if not (0 < percent <= 100):
        raise ValueError(f"Discount must be between 1 and 100, got {percent}.")
    return round(price * (1 - percent / 100), 2)


def split_bill(total: float, people: int) -> float:
    """Divide the bill equally among a number of people."""
    if people < 1:
        raise ValueError("Must split among at least 1 person.")
    return round(total / people, 2)


def format_currency(amount: float, symbol: str = "R") -> str:
    """Format a float as a currency string."""
    return f"{symbol}{amount:,.2f}"


# ─────────────────────────────────────────────────────────────
#  SECTION 2: MENU SORTING ALGORITHMS
#  Implements Bubble Sort, Selection Sort, and built-in sort
#  for comparison – great for algorithms exam topic
# ─────────────────────────────────────────────────────────────

def bubble_sort_by_price(menu_items: list[dict]) -> list[dict]:
    """
    Bubble Sort – O(n²) time complexity.
    Sorts menu items by price ascending.
    Each item: {"name": str, "price": float}
    """
    items = [item.copy() for item in menu_items]  # don't mutate original
    n = len(items)
    for i in range(n):
        for j in range(0, n - i - 1):
            if items[j]["price"] > items[j + 1]["price"]:
                items[j], items[j + 1] = items[j + 1], items[j]
    return items


def selection_sort_by_price(menu_items: list[dict]) -> list[dict]:
    """
    Selection Sort – O(n²) time complexity.
    Finds the minimum price and moves it to the front each pass.
    """
    items = [item.copy() for item in menu_items]
    n = len(items)
    for i in range(n):
        min_idx = i
        for j in range(i + 1, n):
            if items[j]["price"] < items[min_idx]["price"]:
                min_idx = j
        items[i], items[min_idx] = items[min_idx], items[i]
    return items


def builtin_sort_by_price(menu_items: list[dict], ascending: bool = True) -> list[dict]:
    """
    Python built-in sort (Timsort) – O(n log n).
    Best for real use; use bubble/selection for exam illustrations.
    """
    return sorted(menu_items, key=lambda x: x["price"], reverse=not ascending)


def sort_menu_by_category_then_price(menu_items: list[dict]) -> list[dict]:
    """Sort by category alphabetically, then by price ascending within each category."""
    return sorted(menu_items, key=lambda x: (x["category"], x["price"]))


# ─────────────────────────────────────────────────────────────
#  SECTION 3: SEARCH FUNCTIONS
# ─────────────────────────────────────────────────────────────

def linear_search(menu_items: list[dict], name: str) -> dict | None:
    """
    Linear Search – O(n).
    Looks through every item. Good when data is unsorted.
    """
    name_lower = name.lower()
    for item in menu_items:
        if name_lower in item["name"].lower():
            return item
    return None


def filter_by_price_range(menu_items: list[dict],
                           min_price: float,
                           max_price: float) -> list[dict]:
    """Return items whose price falls within [min_price, max_price]."""
    return [item for item in menu_items
            if min_price <= item["price"] <= max_price]


def filter_by_category(menu_items: list[dict], category: str) -> list[dict]:
    """Return all items matching the given category (case-insensitive)."""
    return [item for item in menu_items
            if item.get("category", "").lower() == category.lower()]


# ─────────────────────────────────────────────────────────────
#  SECTION 4: VALIDATION HELPERS
# ─────────────────────────────────────────────────────────────

def is_valid_email(email: str) -> bool:
    """Basic email validation (no external libraries)."""
    return "@" in email and "." in email.split("@")[-1]


def is_valid_phone(phone: str) -> bool:
    """Check if phone number has 10 digits (SA format)."""
    digits = "".join(c for c in phone if c.isdigit())
    return len(digits) == 10


def is_valid_table_number(number: int, max_tables: int = 20) -> bool:
    return 1 <= number <= max_tables


# ─────────────────────────────────────────────────────────────
#  SECTION 5: DEBUGGING EXERCISE FUNCTIONS
#  These contain deliberate bugs for the "Kitchen Chaos" activity.
#  Students must find and fix each bug.
# ─────────────────────────────────────────────────────────────

# BUG 1: Wrong operator (should multiply, not add)
def buggy_calculate_subtotal(items):
    total = 0
    for item in items:
        total += item["price"] + item["qty"]   # BUG: + should be *
    return total

# FIXED:
def fixed_calculate_subtotal(items):
    total = 0
    for item in items:
        total += item["price"] * item["qty"]   # FIXED
    return total


# BUG 2: Off-by-one error in loop
def buggy_get_top_items(items, n):
    result = []
    for i in range(n + 1):   # BUG: range(n+1) goes one too far → IndexError
        result.append(items[i])
    return result

# FIXED:
def fixed_get_top_items(items, n):
    result = []
    for i in range(n):        # FIXED: range(n)
        result.append(items[i])
    return result


# BUG 3: Missing return statement
def buggy_apply_discount(price, percent):
    discounted = price * (1 - percent / 100)
    # BUG: no return → function returns None silently

# FIXED:
def fixed_apply_discount(price, percent):
    discounted = price * (1 - percent / 100)
    return round(discounted, 2)   # FIXED


# BUG 4: Division by zero not handled
def buggy_split_bill(total, people):
    return total / people   # BUG: crashes if people = 0

# FIXED:
def fixed_split_bill(total, people):
    if people == 0:
        raise ValueError("Cannot split among 0 people.")
    return round(total / people, 2)


# ─────────────────────────────────────────────────────────────
#  SECTION 6: CODE GOLF – MENU SORTER
#  Reference solution (full clarity) vs. compact version
# ─────────────────────────────────────────────────────────────

# Verbose (exam-friendly, easy to read):
def sort_menu_verbose(items):
    sorted_items = sorted(items, key=lambda item: item["price"])
    return sorted_items

# Compact (Code Golf style – 1 liner):
sort_menu_compact = lambda items: sorted(items, key=lambda i: i["price"])


# ─────────────────────────────────────────────────────────────
#  DEMO
# ─────────────────────────────────────────────────────────────

if __name__ == "__main__":
    sample_order = [
        {"name": "Bunny Chow",       "price": 89.00, "qty": 2},
        {"name": "Chakalaka Burger", "price": 105.00, "qty": 1},
        {"name": "Rooibos Iced Tea", "price": 35.00, "qty": 3},
    ]

    print("=== BILL CALCULATION ===")
    bill = calculate_total_bill(sample_order)
    for key, val in bill.items():
        print(f"  {key.replace('_', ' ').title():<20} {format_currency(val)}")

    print("\n=== SPLIT BILL (4 people) ===")
    print(f"  Each person pays: {format_currency(split_bill(bill['total'], 4))}")

    menu_flat = [
        {"name": "Vetkoek",          "category": "Starter",  "price": 45.00},
        {"name": "Boerewors Roll",   "category": "Main",     "price": 75.00},
        {"name": "Malva Pudding",    "category": "Dessert",  "price": 55.00},
        {"name": "Bunny Chow",       "category": "Main",     "price": 89.00},
        {"name": "Koeksister",       "category": "Dessert",  "price": 38.00},
    ]

    print("\n=== SORTED BY PRICE (Bubble Sort) ===")
    for item in bubble_sort_by_price(menu_flat):
        print(f"  {item['name']:<25} R{item['price']:.2f}")

    print("\n=== SORTED BY CATEGORY THEN PRICE ===")
    for item in sort_menu_by_category_then_price(menu_flat):
        print(f"  {item['category']:<10} {item['name']:<25} R{item['price']:.2f}")