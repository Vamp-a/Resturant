"""
Digital Restaurant – data_structures.py
GKSS Richfield Bryanston · Exam Prep Workshop
Data Structures: Arrays, Linked Lists, Stacks, Queues, HashMaps
All framed in restaurant context.
"""

from collections import deque


# ─────────────────────────────────────────
#  STACK – The Kitchen Order Stack
#  Orders pile up; the most recent is on top.
#  LIFO: Last In, First Out
# ─────────────────────────────────────────
class OrderStack:
    """
    Kitchen receives tickets. Each new ticket goes on top.
    Chef takes from the top (e.g. most urgent ticket).
    LIFO = Last In, First Out
    """
    def __init__(self):
        self._stack: list = []

    def push(self, order_ticket: str):
        """Add new order ticket to the top."""
        self._stack.append(order_ticket)
        print(f"  Ticket added: {order_ticket}")

    def pop(self) -> str:
        """Remove and return the top ticket."""
        if self.is_empty():
            raise IndexError("Kitchen stack is empty – no orders!")
        ticket = self._stack.pop()
        print(f"  Preparing: {ticket}")
        return ticket

    def peek(self) -> str:
        """Look at the top ticket without removing it."""
        if self.is_empty():
            raise IndexError("Stack is empty.")
        return self._stack[-1]

    def is_empty(self) -> bool:
        return len(self._stack) == 0

    def size(self) -> int:
        return len(self._stack)

    def display(self):
        print(f"\n  Kitchen Stack (top → bottom):")
        for ticket in reversed(self._stack):
            print(f"    [{ticket}]")


# ─────────────────────────────────────────
#  QUEUE – The Waiting Customer Queue
#  FIFO: First In, First Out
#  Customers wait in a line; first to arrive is first served.
# ─────────────────────────────────────────
class CustomerQueue:
    """
    Customers join the back of the queue.
    The host seats the customer at the front first.
    FIFO = First In, First Out
    """
    def __init__(self):
        self._queue: deque = deque()

    def enqueue(self, customer_name: str):
        """Customer joins the back of the waiting list."""
        self._queue.append(customer_name)
        print(f"  {customer_name} added to waiting list. Position: {len(self._queue)}")

    def dequeue(self) -> str:
        """Seat the next customer (from the front)."""
        if self.is_empty():
            raise IndexError("No customers waiting.")
        customer = self._queue.popleft()
        print(f"  Seating: {customer}")
        return customer

    def peek(self) -> str:
        """Who is next without removing them?"""
        if self.is_empty():
            raise IndexError("Queue is empty.")
        return self._queue[0]

    def is_empty(self) -> bool:
        return len(self._queue) == 0

    def size(self) -> int:
        return len(self._queue)

    def display(self):
        print(f"\n  Waiting List (front → back):")
        for i, name in enumerate(self._queue, 1):
            print(f"    {i}. {name}")


# ─────────────────────────────────────────
#  HASH MAP (Dictionary) – Menu Lookup Table
#  O(1) average lookup time
# ─────────────────────────────────────────
class MenuHashMap:
    """
    Fast menu lookup using Python's dict (hash map under the hood).
    Key = dish name (lowercased) → Value = price
    Why hash maps? Searching by name is O(1) instead of O(n).
    """

    def __init__(self):
        self._map: dict[str, float] = {}

    def add(self, name: str, price: float):
        self._map[name.lower()] = price

    def get_price(self, name: str) -> float | None:
        return self._map.get(name.lower())

    def update_price(self, name: str, new_price: float) -> bool:
        key = name.lower()
        if key in self._map:
            self._map[key] = new_price
            return True
        return False

    def remove(self, name: str) -> bool:
        key = name.lower()
        if key in self._map:
            del self._map[key]
            return True
        return False

    def all_items(self) -> list[tuple]:
        return sorted(self._map.items(), key=lambda x: x[1])


# ─────────────────────────────────────────
#  LINKED LIST – Order History per Table
# ─────────────────────────────────────────
class OrderNode:
    """A single node in the linked list."""
    def __init__(self, order_id: int, dish: str, price: float):
        self.order_id = order_id
        self.dish = dish
        self.price = price
        self.next: "OrderNode | None" = None

    def __repr__(self):
        return f"Order({self.order_id}: {self.dish}, R{self.price:.2f})"


class TableOrderHistory:
    """
    Singly linked list storing all orders placed at a table.
    Demonstrates manual pointer management (for exam understanding).
    """

    def __init__(self, table_number: int):
        self.table_number = table_number
        self.head: OrderNode | None = None
        self._size = 0

    def append(self, order_id: int, dish: str, price: float):
        """Add a new order to the end of the history."""
        new_node = OrderNode(order_id, dish, price)
        if self.head is None:
            self.head = new_node
        else:
            current = self.head
            while current.next is not None:
                current = current.next
            current.next = new_node
        self._size += 1

    def total_spent(self) -> float:
        total = 0.0
        current = self.head
        while current:
            total += current.price
            current = current.next
        return round(total, 2)

    def display(self):
        print(f"\n  Table {self.table_number} Order History:")
        current = self.head
        while current:
            arrow = " → " if current.next else ""
            print(f"    [{current.dish} R{current.price:.2f}]{arrow}", end="")
            current = current.next
        print(f"\n  Total spent: R{self.total_spent():.2f}")

    def __len__(self):
        return self._size


# ─────────────────────────────────────────
#  DEMO
# ─────────────────────────────────────────
if __name__ == "__main__":

    print("\n=== KITCHEN ORDER STACK (LIFO) ===")
    stack = OrderStack()
    stack.push("Table 3 – Bunny Chow")
    stack.push("Table 7 – Prawn Curry")
    stack.push("Table 1 – Boerewors Roll")
    stack.display()
    stack.pop()
    stack.display()

    print("\n=== CUSTOMER WAITING QUEUE (FIFO) ===")
    queue = CustomerQueue()
    queue.enqueue("Sipho Nkosi")
    queue.enqueue("Lerato Dlamini")
    queue.enqueue("Marco van der Berg")
    queue.display()
    queue.dequeue()
    queue.display()

    print("\n=== MENU HASH MAP (O(1) lookup) ===")
    menu_map = MenuHashMap()
    menu_map.add("Malva Pudding", 58.00)
    menu_map.add("Bunny Chow", 119.00)
    menu_map.add("Peri-Peri Chicken Wings", 89.00)
    print(f"  Bunny Chow price: R{menu_map.get_price('Bunny Chow'):.2f}")
    menu_map.update_price("Malva Pudding", 62.00)
    print(f"  Malva Pudding (updated): R{menu_map.get_price('malva pudding'):.2f}")
    print("  All items:")
    for name, price in menu_map.all_items():
        print(f"    {name:<35} R{price:.2f}")

    print("\n=== TABLE ORDER HISTORY (LINKED LIST) ===")
    history = TableOrderHistory(table_number=5)
    history.append(1001, "Vetkoek with Mince",    45.00)
    history.append(1002, "Durban Prawn Curry",   189.00)
    history.append(1003, "Amarula Cheesecake",    72.00)
    history.append(1004, "Cape Winelands White",  85.00)
    history.display()