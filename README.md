# Digital Restaurant – Ubuntu Kitchen

**GKSS Richfield Bryanston · Exam Prep Workshop**

A full-stack restaurant management system built across five modules: Web Development, OOP, Data Structures, Databases, and Functions. Everything connects through a single Flask API backed by SQLite.

---

## What It Covers

| Module          | File(s)                                  | Topics                                                    |
| --------------- | ---------------------------------------- | --------------------------------------------------------- |
| Web Development | `index.html`,`static/app.js`         | HTML, CSS, DOM, fetch API, async/await                    |
| OOP             | `models.py`,`main.py`                | Classes, encapsulation, composition, state machine        |
| Functions       | `utils.py`                             | Pure functions, sorting algorithms, validation, recursion |
| Data Structures | `data_structures.py`                   | Stack, Queue, Hash Map, Linked List                       |
| Databases       | `database/schema.sql`,`db_runner.py` | 3NF schema design, SQL queries, joins, aggregation        |
| Integration     | `app.py`                               | REST API, Flask routes, connecting frontend to DB         |

---

## Project Structure

```
ubuntu-kitchen/
├── app.py                  ← Flask server – the bridge between frontend and database
├── index.html              ← Restaurant website (HTML + CSS)
├── main.py                 ← OOP demo – run this standalone to see models in action
├── models.py               ← OOP classes: Restaurant, Menu, MenuItem, Order, Customer
├── utils.py                ← Functions: bill calculation, sorting algorithms, validation
├── data_structures.py      ← Stack, Queue, HashMap, Linked List (restaurant context)
├── db_runner.py            ← Builds the database and runs demo SQL queries
├── requirements.txt        ← Python dependencies (just Flask)
├── restaurant.db           ← SQLite database (auto-generated, do not edit manually)
├── static/
│   └── app.js              ← All frontend JavaScript (menu, cart, orders, reservations)
└── database/
    └── schema.sql          ← Database schema (3NF) + seed data
```

---

## Requirements

* Python 3.10 or higher
* Flask (the only external dependency)

```bash
pip install -r requirements.txt
```

---

## Setup and Run

### Step 1 – Build the database

Run this once. It creates `restaurant.db` from `schema.sql` and populates it with seed data.

```bash
python db_runner.py
```

You will see 8 SQL query results printed to the terminal confirming the data is loaded.

### Step 2 – Start the Flask server

```bash
python app.py
```

### Step 3 – Open the site

```
http://localhost:5000
```

---

## Running the Other Modules Standalone

Each file can also run on its own for demo and exam practice purposes.

```bash
# OOP demo – places orders, prints receipts, shows analytics
python main.py

# Functions demo – bill calculations, sorting algorithms
python utils.py

# Data structures demo – stack, queue, hash map, linked list
python data_structures.py

# Database demo – rebuilds DB and runs all 8 SQL queries
python db_runner.py
```

---

## API Reference

All endpoints are served by `app.py` on `http://localhost:5000`.

### `GET /`

Serves `index.html` to the browser.

### `GET /api/menu`

Returns all available menu items from the database as a JSON array.

```json
[
  { "id": 1, "name": "Vetkoek with Mince", "cat": "starter",
    "price": 45.00, "desc": "...", "veg": 1, "hot": 0 },
  ...
]
```

### `POST /api/orders`

Saves a customer order to the database.

**Request body:**

```json
{
  "customer_id": 1,
  "table_id": 1,
  "notes": "No coriander please",
  "items": [
    { "item_id": 1, "quantity": 2, "unit_price": 45.00 }
  ]
}
```

**Response:**

```json
{ "order_id": 8, "status": "pending" }
```

### `POST /api/reservations`

Creates a reservation. Automatically creates a new customer record if the email is not already in the database.

**Request body:**

```json
{
  "firstName": "Sipho", "lastName": "Ndlovu",
  "email": "sipho@example.co.za", "phone": "0821234567",
  "date": "2026-07-15", "time": "19:00",
  "guests": "4", "occasion": "Birthday", "notes": "Window seat please"
}
```

**Response:**

```json
{ "reservation_id": 4, "status": "confirmed" }
```

### `GET /api/analytics`

Returns revenue data and top ordered items from served orders.

```json
{
  "total_revenue": 4821.50,
  "top_items": [ { "name": "Bunny Chow (Mutton)", "total": 5 }, ... ],
  "by_category": [ { "category": "Main", "items_sold": 18, "revenue": 2340.00 }, ... ]
}
```

---

## Database Schema (3NF)

Seven tables. Foreign keys are enforced via `PRAGMA foreign_keys = ON`.

```
categories ──< menu_items ──< order_items >── orders >── customers
                                                │
tables ─────────────────────────────────────>──┘
                                                │
staff ──────────────────────────────────────>──┘

reservations >── customers
reservations >── tables
reservations >── staff
```

---

## How the Pieces Connect

```
Browser (index.html)
    │  HTML rendered, CSS styled
    │
    └── static/app.js
            │  loadMenu()          → GET  /api/menu
            │  placeOrder()        → POST /api/orders
            └  submitReservation() → POST /api/reservations
                                          │
                                      app.py  (Flask)
                                          │  sqlite3
                                      restaurant.db
                                          │  built from
                                      database/schema.sql
```

`main.py` and `db_runner.py` connect directly to the database and models without going through Flask — they are standalone demo scripts, not part of the web application.

---

## Seed Data

`db_runner.py` populates the database with:

* **30 menu items** across 4 categories (Starters, Mains, Desserts, Drinks)
* **10 restaurant tables** (Indoor, Outdoor, Private Room, Bar)
* **5 staff members** (Manager, Waiters, Chefs)
* **6 customers** with loyalty points
* **7 orders** (6 served, 1 pending) with order items
* **3 upcoming reservations**

---

## Bill Calculation Logic

Consistent across `utils.py`, `models.py`, `app.js`, and `schema.sql`:

```
Subtotal  =  sum(item.price × quantity)
VAT       =  subtotal × 15%
Service   =  subtotal × 10%
─────────────────────────────────────────
Total     =  subtotal + VAT + service
```

---

*Built for GKSS Richfield Bryanston – Exam Prep Workshop*
