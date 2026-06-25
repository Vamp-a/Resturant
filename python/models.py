"""
Digital Restaurant – models.py
GKSS Richfield Bryanston · Exam Prep Workshop
OOP Module: Core Classes
"""

from datetime import datetime
from typing import Optional


# ─────────────────────────────────────────
#  MENU ITEM
# ─────────────────────────────────────────
class MenuItem:
    """Represents a single dish on the menu."""

    def __init__(self, item_id: int, name: str, category: str,
                 price: float, description: str = "", available: bool = True):
        self.item_id = item_id
        self.name = name
        self.category = category   # e.g. "Starter", "Main", "Dessert", "Drink"
        self.price = price
        self.description = description
        self.available = available

    def apply_discount(self, percent: float) -> float:
        """Return discounted price without changing the original."""
        if not (0 < percent <= 100):
            raise ValueError("Discount must be between 1 and 100 percent.")
        return round(self.price * (1 - percent / 100), 2)

    def __repr__(self):
        status = "✓" if self.available else "✗"
        return f"[{status}] {self.name} ({self.category}) – R{self.price:.2f}"


# ─────────────────────────────────────────
#  MENU
# ─────────────────────────────────────────
class Menu:
    """Collection of MenuItems. Supports searching, filtering, sorting."""

    def __init__(self, restaurant_name: str):
        self.restaurant_name = restaurant_name
        self._items: list[MenuItem] = []

    def add_item(self, item: MenuItem):
        self._items.append(item)
        print(f"  Added: {item.name}")

    def remove_item(self, item_id: int) -> bool:
        for i, item in enumerate(self._items):
            if item.item_id == item_id:
                removed = self._items.pop(i)
                print(f"  Removed: {removed.name}")
                return True
        return False

    def find_by_name(self, name: str) -> Optional[MenuItem]:
        name = name.lower()
        for item in self._items:
            if name in item.name.lower():
                return item
        return None

    def filter_by_category(self, category: str) -> list[MenuItem]:
        return [i for i in self._items if i.category.lower() == category.lower()]

    def sort_by_price(self, ascending: bool = True) -> list[MenuItem]:
        return sorted(self._items, key=lambda i: i.price, reverse=not ascending)

    def available_items(self) -> list[MenuItem]:
        return [i for i in self._items if i.available]

    def display(self):
        print(f"\n{'═'*50}")
        print(f"  {self.restaurant_name} – MENU")
        print(f"{'═'*50}")
        categories = sorted(set(i.category for i in self._items))
        for cat in categories:
            print(f"\n  {cat.upper()}")
            print(f"  {'─'*40}")
            for item in self.filter_by_category(cat):
                avail = "" if item.available else " [UNAVAILABLE]"
                print(f"  {item.item_id:>3}. {item.name:<28} R{item.price:>7.2f}{avail}")
        print(f"{'═'*50}\n")


# ─────────────────────────────────────────
#  CUSTOMER
# ─────────────────────────────────────────
class Customer:
    """Represents a restaurant customer."""

    def __init__(self, customer_id: int, name: str, email: str, phone: str = ""):
        self.customer_id = customer_id
        self.name = name
        self.email = email
        self.phone = phone
        self.order_history: list[int] = []   # stores order IDs

    def add_to_history(self, order_id: int):
        self.order_history.append(order_id)

    def __repr__(self):
        return f"Customer({self.customer_id}: {self.name}, {self.email})"


# ─────────────────────────────────────────
#  ORDER LINE ITEM
# ─────────────────────────────────────────
class OrderItem:
    """A menu item plus quantity inside an order."""

    def __init__(self, menu_item: MenuItem, quantity: int):
        if quantity < 1:
            raise ValueError("Quantity must be at least 1.")
        self.menu_item = menu_item
        self.quantity = quantity

    @property
    def subtotal(self) -> float:
        return round(self.menu_item.price * self.quantity, 2)

    def __repr__(self):
        return f"{self.quantity}x {self.menu_item.name} = R{self.subtotal:.2f}"


# ─────────────────────────────────────────
#  ORDER
# ─────────────────────────────────────────
class Order:
    """
    Represents a customer order.
    Demonstrates encapsulation, computed properties, and state management.
    """

    VAT_RATE = 0.15          # 15% VAT
    SERVICE_CHARGE = 0.10    # 10% service charge

    STATUS_OPTIONS = ["pending", "confirmed", "preparing", "ready", "served", "cancelled"]

    def __init__(self, order_id: int, customer: Customer, table_number: int):
        self.order_id = order_id
        self.customer = customer
        self.table_number = table_number
        self._items: list[OrderItem] = []
        self._status = "pending"
        self.created_at = datetime.now()
        self.notes: str = ""

    # ── Status management ──
    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, new_status: str):
        if new_status not in self.STATUS_OPTIONS:
            raise ValueError(f"Invalid status. Choose from: {self.STATUS_OPTIONS}")
        self._status = new_status
        print(f"  Order #{self.order_id} status → {new_status.upper()}")

    # ── Item management ──
    def add_item(self, menu_item: MenuItem, quantity: int = 1):
        if not menu_item.available:
            raise ValueError(f"{menu_item.name} is not available.")
        # If item already in order, increase quantity
        for oi in self._items:
            if oi.menu_item.item_id == menu_item.item_id:
                oi.quantity += quantity
                return
        self._items.append(OrderItem(menu_item, quantity))

    def remove_item(self, item_id: int) -> bool:
        for i, oi in enumerate(self._items):
            if oi.menu_item.item_id == item_id:
                self._items.pop(i)
                return True
        return False

    # ── Calculations ──
    @property
    def subtotal(self) -> float:
        return round(sum(oi.subtotal for oi in self._items), 2)

    @property
    def vat_amount(self) -> float:
        return round(self.subtotal * self.VAT_RATE, 2)

    @property
    def service_charge_amount(self) -> float:
        return round(self.subtotal * self.SERVICE_CHARGE, 2)

    @property
    def total(self) -> float:
        return round(self.subtotal + self.vat_amount + self.service_charge_amount, 2)

    # ── Receipt ──
    def print_receipt(self):
        print(f"\n{'═'*46}")
        print(f"  THE DIGITAL RESTAURANT")
        print(f"  Receipt – Order #{self.order_id}")
        print(f"  Table {self.table_number} | {self.created_at.strftime('%Y-%m-%d %H:%M')}")
        print(f"  Customer: {self.customer.name}")
        print(f"{'─'*46}")
        for oi in self._items:
            print(f"  {str(oi.quantity) + 'x':<4} {oi.menu_item.name:<28} R{oi.subtotal:>7.2f}")
        print(f"{'─'*46}")
        print(f"  {'Subtotal':<35} R{self.subtotal:>7.2f}")
        print(f"  {'VAT (15%)':<35} R{self.vat_amount:>7.2f}")
        print(f"  {'Service Charge (10%)':<35} R{self.service_charge_amount:>7.2f}")
        print(f"{'─'*46}")
        print(f"  {'TOTAL':<35} R{self.total:>7.2f}")
        if self.notes:
            print(f"\n  Notes: {self.notes}")
        print(f"{'═'*46}\n")

    def __repr__(self):
        return f"Order(#{self.order_id}, Table {self.table_number}, {self.status}, R{self.total:.2f})"


# ─────────────────────────────────────────
#  RESTAURANT
# ─────────────────────────────────────────
class Restaurant:
    """
    Top-level class. Owns the menu, customers, and all orders.
    Demonstrates composition and aggregation.
    """

    def __init__(self, name: str, address: str):
        self.name = name
        self.address = address
        self.menu = Menu(name)
        self._customers: dict[int, Customer] = {}
        self._orders: dict[int, Order] = {}
        self._next_order_id = 1001
        self._next_customer_id = 1

    def register_customer(self, name: str, email: str, phone: str = "") -> Customer:
        cust = Customer(self._next_customer_id, name, email, phone)
        self._customers[cust.customer_id] = cust
        self._next_customer_id += 1
        return cust

    def place_order(self, customer: Customer, table_number: int) -> Order:
        order = Order(self._next_order_id, customer, table_number)
        self._orders[order.order_id] = order
        self._next_order_id += 1
        customer.add_to_history(order.order_id)
        return order

    def get_order(self, order_id: int) -> Optional[Order]:
        return self._orders.get(order_id)

    def active_orders(self) -> list[Order]:
        return [o for o in self._orders.values()
                if o.status not in ("served", "cancelled")]

    def total_revenue(self) -> float:
        return round(sum(
            o.total for o in self._orders.values() if o.status == "served"
        ), 2)

    def top_ordered_items(self, n: int = 5) -> list[tuple]:
        counts: dict[str, int] = {}
        for order in self._orders.values():
            for oi in order._items:
                counts[oi.menu_item.name] = counts.get(oi.menu_item.name, 0) + oi.quantity
        sorted_items = sorted(counts.items(), key=lambda x: x[1], reverse=True)
        return sorted_items[:n]