"""
Digital Restaurant – db_runner.py
GKSS Richfield Bryanston · Exam Prep Workshop
Databases Module: Run this to create and query the restaurant database.
Uses Python's built-in sqlite3 – no extra installs needed.
"""

import sqlite3
import os

DB_PATH = "restaurant.db"
SCHEMA_PATH = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")


def get_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row   # Rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def build_database():
    """Read schema.sql and execute it to create + populate the database."""
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"  Old database removed.")

    with get_connection() as conn:
        schema_path = os.path.join(os.path.dirname(__file__), "..", "database", "schema.sql")
        with open(schema_path, "r") as f:
            sql = f.read()

        # Split on semicolons but skip comment blocks
        statements = [s.strip() for s in sql.split(";") if s.strip() and not s.strip().startswith("--")]
        for stmt in statements:
            try:
                conn.execute(stmt)
            except Exception as e:
                # Skip SELECT queries (they can't run in executescript)
                if "SELECT" not in stmt.upper():
                    print(f"  Warning: {e}")
        conn.commit()
    print(f"  Database created: {DB_PATH}\n")


def run_query(conn: sqlite3.Connection, title: str, sql: str):
    print(f"\n{'═'*60}")
    print(f"  {title}")
    print(f"{'─'*60}")
    cursor = conn.execute(sql)
    rows = cursor.fetchall()
    if rows:
        # Print column headers
        headers = [desc[0] for desc in cursor.description]
        col_widths = [max(len(h), max(len(str(r[h])) for r in rows)) for h in headers]
        header_row = "  " + "  ".join(h.ljust(col_widths[i]) for i, h in enumerate(headers))
        print(header_row)
        print("  " + "─" * (sum(col_widths) + len(headers) * 2))
        for row in rows:
            print("  " + "  ".join(str(row[h]).ljust(col_widths[i]) for i, h in enumerate(headers)))
    else:
        print("  (no results)")
    return rows


def main():
    print("\n" + "="*60)
    print("  DIGITAL RESTAURANT – Database Demo")
    print("  GKSS Richfield Bryanston – Exam Prep Workshop")
    print("="*60 + "\n")

    build_database()

    with get_connection() as conn:

        run_query(conn, "FULL MENU (available items)", """
            SELECT m.item_id, c.name AS category, m.name AS dish,
                   printf('R%.2f', m.price) AS price,
                   CASE WHEN m.is_vegetarian=1 THEN 'Veg' ELSE '' END AS veg
            FROM menu_items m
            JOIN categories c ON m.category_id = c.category_id
            WHERE m.is_available = 1
            ORDER BY c.name, m.price
        """)

        run_query(conn, "TOP 5 MOST ORDERED DISHES", """
            SELECT mi.name AS dish, SUM(oi.quantity) AS total_ordered
            FROM order_items oi
            JOIN menu_items mi ON oi.item_id = mi.item_id
            GROUP BY mi.name
            ORDER BY total_ordered DESC
            LIMIT 5
        """)

        run_query(conn, "ORDER TOTALS (subtotal + 15% VAT)", """
            SELECT o.order_id,
                   c.first_name || ' ' || c.last_name AS customer,
                   o.status,
                   printf('R%.2f', SUM(oi.quantity * oi.unit_price)) AS subtotal,
                   printf('R%.2f', SUM(oi.quantity * oi.unit_price) * 1.15) AS total_incl_vat
            FROM orders o
            JOIN customers c    ON o.customer_id = c.customer_id
            JOIN order_items oi ON o.order_id    = oi.order_id
            GROUP BY o.order_id
            ORDER BY o.order_id
        """)

        run_query(conn, "VEGETARIAN DISHES UNDER R100", """
            SELECT name, printf('R%.2f', price) AS price
            FROM menu_items
            WHERE is_vegetarian = 1 AND price < 100 AND is_available = 1
            ORDER BY price
        """)

        run_query(conn, "REVENUE BY CATEGORY (served orders)", """
            SELECT cat.name AS category,
                   SUM(oi.quantity) AS items_sold,
                   printf('R%.2f', SUM(oi.quantity * oi.unit_price)) AS revenue
            FROM order_items oi
            JOIN menu_items mi  ON oi.item_id   = mi.item_id
            JOIN categories cat ON mi.category_id = cat.category_id
            JOIN orders o       ON oi.order_id   = o.order_id
            WHERE o.status = 'served'
            GROUP BY cat.name
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC
        """)

        run_query(conn, "REPEAT CUSTOMERS + TOTAL SPENT", """
            SELECT c.first_name || ' ' || c.last_name AS customer,
                   COUNT(DISTINCT o.order_id) AS visits,
                   printf('R%.2f', SUM(oi.quantity * oi.unit_price)) AS total_spent
            FROM customers c
            JOIN orders o       ON c.customer_id = o.customer_id
            JOIN order_items oi ON o.order_id    = oi.order_id
            WHERE o.status = 'served'
            GROUP BY c.customer_id
            HAVING COUNT(DISTINCT o.order_id) > 1
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC
        """)

        run_query(conn, "STAFF PERFORMANCE (revenue generated)", """
            SELECT s.first_name || ' ' || s.last_name AS staff,
                   s.role,
                   COUNT(DISTINCT o.order_id) AS orders_served,
                   printf('R%.2f', SUM(oi.quantity * oi.unit_price)) AS revenue
            FROM staff s
            JOIN orders o       ON s.staff_id = o.staff_id
            JOIN order_items oi ON o.order_id = oi.order_id
            WHERE o.status = 'served'
            GROUP BY s.staff_id
            ORDER BY SUM(oi.quantity * oi.unit_price) DESC
        """)

        run_query(conn, "AVERAGE PRICE BY CATEGORY", """
            SELECT c.name AS category,
                   printf('R%.2f', AVG(m.price)) AS avg_price,
                   printf('R%.2f', MIN(m.price)) AS cheapest,
                   printf('R%.2f', MAX(m.price)) AS most_expensive
            FROM menu_items m
            JOIN categories c ON m.category_id = c.category_id
            GROUP BY c.name
        """)

    print(f"\n{'═'*60}")
    print(f"  All queries complete. Database saved to: {DB_PATH}")
    print(f"  Open with: sqlite3 {DB_PATH}  OR  DB Browser for SQLite")
    print(f"{'═'*60}\n")


if __name__ == "__main__":
    main()