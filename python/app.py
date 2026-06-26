"""
Digital Restaurant – app.py
GKSS Richfield Bryanston · Exam Prep Workshop

Run:
    python db_runner.py    ← build the database first (once)
    python app.py          ← start the server
    open http://localhost:5000
"""

from flask import Flask, jsonify, request, send_file
import sqlite3

app = Flask(__name__)
DB_PATH = "restaurant.db"


# ─────────────────────────────────────────
#  DB HELPER
# ─────────────────────────────────────────
def get_db() -> sqlite3.Connection:
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row          # rows behave like dicts
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


# ─────────────────────────────────────────
#  SERVE FRONTEND
#  GET /  →  index.html
# ─────────────────────────────────────────
@app.route('/')
def index():
    return send_file('C:/Users/user/Documents/GitHub/Resturant/web/index.html')


# ─────────────────────────────────────────
#  MENU
#  GET /api/menu  →  JSON array of all available items
#  Called by loadMenu() in app.js on page load
# ─────────────────────────────────────────
@app.route('/api/menu')
def get_menu():
    with get_db() as conn:
        rows = conn.execute("""
            SELECT
                m.item_id                        AS id,
                m.name,
                LOWER(c.name)                    AS cat,
                m.price,
                m.description                    AS desc,
                CAST(m.is_vegetarian AS INTEGER) AS veg,
                0                                AS hot
            FROM menu_items m
            JOIN categories c ON m.category_id = c.category_id
            WHERE m.is_available = 1
            ORDER BY c.category_id, m.price
        """).fetchall()
    return jsonify([dict(r) for r in rows])


# ─────────────────────────────────────────
#  ORDERS
#  POST /api/orders
#  Body: { customer_id, table_id, notes, items: [{item_id, quantity, unit_price}] }
#  Called by placeOrder() in app.js
# ─────────────────────────────────────────
@app.route('/api/orders', methods=['POST'])
def create_order():
    data     = request.get_json()
    notes    = data.get('notes', '')
    items    = data.get('items', [])

    if not items:
        return jsonify({'error': 'Order has no items'}), 400

    with get_db() as conn:

        # Guarantee a walk-in guest customer exists (id=1)
        # so orders always have a valid customer_id even without a login system
        guest = conn.execute(
            "SELECT customer_id FROM customers WHERE customer_id = 1"
        ).fetchone()

        if not guest:
            conn.execute(
                """INSERT INTO customers (customer_id, first_name, last_name, email, phone)
                   VALUES (1, 'Walk-in', 'Guest', 'guest@ubuntukitchen.co.za', '0000000000')"""
            )

        # Guarantee table 1 exists
        table = conn.execute(
            "SELECT table_id FROM tables WHERE table_id = 1"
        ).fetchone()

        if not table:
            conn.execute(
                "INSERT INTO tables (table_id, table_number, capacity, location) VALUES (1, 1, 4, 'Indoor')"
            )

        cur = conn.execute(
            "INSERT INTO orders (customer_id, table_id, status, notes) VALUES (1, 1, 'pending', ?)",
            (notes,)
        )
        order_id = cur.lastrowid

        for item in items:
            conn.execute(
                """INSERT INTO order_items (order_id, item_id, quantity, unit_price)
                   VALUES (?, ?, ?, ?)""",
                (order_id, item['item_id'], item['quantity'], item['unit_price'])
            )
        conn.commit()

    print(f"  ✓ Order #{order_id} saved – {len(items)} item(s)")
    return jsonify({'order_id': order_id, 'status': 'pending'}), 201


# ─────────────────────────────────────────
#  RESERVATIONS
#  POST /api/reservations
#  Body: { firstName, lastName, email, phone, date, time, guests, occasion, notes }
#  Called by submitReservation() in app.js after validation passes
#  Auto creates a new customer record if the email is not already in the DB
# ─────────────────────────────────────────
@app.route('/api/reservations', methods=['POST'])
def create_reservation():
    data  = request.get_json()
    email = data['email']

    with get_db() as conn:

        # Find or create the customer
        existing = conn.execute(
            "SELECT customer_id FROM customers WHERE email = ?", (email,)
        ).fetchone()

        if existing:
            customer_id = existing['customer_id']
        else:
            cur = conn.execute(
                "INSERT INTO customers (first_name, last_name, email, phone) VALUES (?, ?, ?, ?)",
                (data['firstName'], data['lastName'], email, data['phone'])
            )
            customer_id = cur.lastrowid

        # Pick the smallest table that fits the party
        guests_raw = str(data.get('guests', '2'))
        capacity   = int(guests_raw) if guests_raw.isdigit() else 2
        table = conn.execute(
            "SELECT table_id FROM tables WHERE capacity >= ? ORDER BY capacity LIMIT 1",
            (capacity,)
        ).fetchone()
        table_id = table['table_id'] if table else 1

        # Merge occasion tag into notes
        occasion = data.get('occasion', '')
        notes    = data.get('notes',    '')
        if occasion and occasion.lower() not in ('none', ''):
            notes = f"[{occasion}] {notes}".strip()

        cur = conn.execute(
            """INSERT INTO reservations
               (customer_id, table_id, party_size, date_time, status, special_notes)
               VALUES (?, ?, ?, ?, 'confirmed', ?)""",
            (customer_id, table_id, guests_raw, f"{data['date']} {data['time']}", notes)
        )
        conn.commit()
        reservation_id = cur.lastrowid

    return jsonify({'reservation_id': reservation_id, 'status': 'confirmed'}), 201


# ─────────────────────────────────────────
#  ANALYTICS
#  GET /api/analytics  →  top items, revenue, breakdown by category
# ─────────────────────────────────────────
@app.route('/api/analytics')
def get_analytics():
    with get_db() as conn:

        top_items = conn.execute("""
            SELECT mi.name, SUM(oi.quantity) AS total
            FROM order_items oi
            JOIN menu_items mi ON oi.item_id = mi.item_id
            GROUP BY mi.name
            ORDER BY total DESC
            LIMIT 5
        """).fetchall()

        revenue = conn.execute("""
            SELECT ROUND(SUM(oi.quantity * oi.unit_price), 2) AS total
            FROM order_items oi
            JOIN orders o ON oi.order_id = o.order_id
            WHERE o.status = 'served'
        """).fetchone()

        by_category = conn.execute("""
            SELECT cat.name AS category,
                   SUM(oi.quantity) AS items_sold,
                   ROUND(SUM(oi.quantity * oi.unit_price), 2) AS revenue
            FROM order_items oi
            JOIN menu_items mi  ON oi.item_id    = mi.item_id
            JOIN categories cat ON mi.category_id = cat.category_id
            JOIN orders o       ON oi.order_id    = o.order_id
            WHERE o.status = 'served'
            GROUP BY cat.name
            ORDER BY revenue DESC
        """).fetchall()

    return jsonify({
        'top_items':     [dict(r) for r in top_items],
        'total_revenue': revenue['total'] if revenue['total'] else 0,
        'by_category':   [dict(r) for r in by_category],
    })


# ─────────────────────────────────────────
#  START
# ─────────────────────────────────────────
if __name__ == '__main__':
    print("\n  Ubuntu Kitchen – Flask API")
    print("  Open: http://localhost:5000\n")
    app.run(debug=True, port=5000)
