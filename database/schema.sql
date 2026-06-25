-- ═══════════════════════════════════════════════════════════════
--  Digital Restaurant – schema.sql
--  GKSS Richfield Bryanston · Exam Prep Workshop
--  Databases Module: Schema Design, Normalisation (3NF), SQL Queries
-- ═══════════════════════════════════════════════════════════════

-- ──────────────────────────────────────────────────────────────
--  SECTION 1: CREATE TABLES (3NF Normalised Schema)
-- ──────────────────────────────────────────────────────────────

-- Drop existing tables (safe re-run)
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS reservations;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS menu_items;
DROP TABLE IF EXISTS categories;
DROP TABLE IF EXISTS tables;
DROP TABLE IF EXISTS staff;

-- Categories – lookup table (1NF: atomic values only)
CREATE TABLE categories (
    category_id   INTEGER PRIMARY KEY AUTOINCREMENT,
    name          TEXT NOT NULL UNIQUE,   -- e.g. 'Starter', 'Main', 'Dessert', 'Drink'
    description   TEXT
);

-- Menu Items (2NF: all non-key fields depend on full PK)
CREATE TABLE menu_items (
    item_id        INTEGER PRIMARY KEY AUTOINCREMENT,
    name           TEXT    NOT NULL,
    category_id    INTEGER NOT NULL,
    price          REAL    NOT NULL CHECK (price >= 0),
    description    TEXT    DEFAULT '',
    is_available   INTEGER DEFAULT 1,     -- 1 = available, 0 = not available (SQLite has no BOOLEAN)
    is_vegetarian  INTEGER DEFAULT 0,
    is_vegan       INTEGER DEFAULT 0,
    allergens      TEXT    DEFAULT '',    -- comma-separated: "gluten, dairy, nuts"
    FOREIGN KEY (category_id) REFERENCES categories(category_id)
);

-- Restaurant Tables
CREATE TABLE tables (
    table_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    table_number   INTEGER NOT NULL UNIQUE,
    capacity       INTEGER NOT NULL,
    location       TEXT    DEFAULT 'Indoor'  -- 'Indoor', 'Outdoor', 'Private Room'
);

-- Staff (3NF: no transitive dependencies)
CREATE TABLE staff (
    staff_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name     TEXT    NOT NULL,
    last_name      TEXT    NOT NULL,
    role           TEXT    NOT NULL,       -- 'Waiter', 'Chef', 'Manager', 'Host'
    email          TEXT    UNIQUE,
    phone          TEXT
);

-- Customers
CREATE TABLE customers (
    customer_id    INTEGER PRIMARY KEY AUTOINCREMENT,
    first_name     TEXT    NOT NULL,
    last_name      TEXT    NOT NULL,
    email          TEXT    UNIQUE,
    phone          TEXT,
    loyalty_points INTEGER DEFAULT 0,
    created_at     TEXT    DEFAULT (datetime('now'))
);

-- Reservations
CREATE TABLE reservations (
    reservation_id INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id    INTEGER NOT NULL,
    table_id       INTEGER NOT NULL,
    staff_id       INTEGER,               -- which staff member took the reservation
    party_size     INTEGER NOT NULL,
    date_time      TEXT    NOT NULL,      -- ISO format: 'YYYY-MM-DD HH:MM'
    status         TEXT    DEFAULT 'confirmed',  -- 'confirmed', 'seated', 'cancelled', 'no-show'
    special_notes  TEXT    DEFAULT '',
    created_at     TEXT    DEFAULT (datetime('now')),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (table_id)    REFERENCES tables(table_id),
    FOREIGN KEY (staff_id)    REFERENCES staff(staff_id)
);

-- Orders (one per table visit)
CREATE TABLE orders (
    order_id       INTEGER PRIMARY KEY AUTOINCREMENT,
    customer_id    INTEGER NOT NULL,
    table_id       INTEGER NOT NULL,
    staff_id       INTEGER,
    status         TEXT    DEFAULT 'pending',
    -- status options: 'pending', 'confirmed', 'preparing', 'ready', 'served', 'cancelled'
    notes          TEXT    DEFAULT '',
    created_at     TEXT    DEFAULT (datetime('now')),
    served_at      TEXT,
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id),
    FOREIGN KEY (table_id)    REFERENCES tables(table_id),
    FOREIGN KEY (staff_id)    REFERENCES staff(staff_id)
);

-- Order Items – the junction table linking Orders ↔ Menu Items
-- This resolves the many-to-many relationship (3NF)
CREATE TABLE order_items (
    order_item_id  INTEGER PRIMARY KEY AUTOINCREMENT,
    order_id       INTEGER NOT NULL,
    item_id        INTEGER NOT NULL,
    quantity       INTEGER NOT NULL CHECK (quantity >= 1),
    unit_price     REAL    NOT NULL,      -- price at time of order (prices can change later)
    special_request TEXT   DEFAULT '',
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (item_id)  REFERENCES menu_items(item_id)
);


-- ──────────────────────────────────────────────────────────────
--  SECTION 2: SEED DATA – Categories
-- ──────────────────────────────────────────────────────────────

INSERT INTO categories (name, description) VALUES
    ('Starter',  'Appetisers and small plates to begin the meal'),
    ('Main',     'Main course dishes'),
    ('Dessert',  'Sweet treats and desserts'),
    ('Drink',    'Beverages – alcoholic and non-alcoholic');


-- ──────────────────────────────────────────────────────────────
--  SECTION 3: SEED DATA – Menu Items (South African themed)
-- ──────────────────────────────────────────────────────────────

-- Starters (category_id = 1)
INSERT INTO menu_items (name, category_id, price, description, is_vegetarian) VALUES
    ('Vetkoek with Mince',       1,  45.00, 'Deep-fried dough filled with spiced mince',               0),
    ('Peri-Peri Chicken Wings',  1,  89.00, 'Crispy wings with house peri-peri sauce, 6 pcs',          0),
    ('Chakalaka Spring Rolls',   1,  65.00, 'Crispy rolls filled with chakalaka relish',               1),
    ('Boerewors Bites',          1,  72.00, 'Grilled mini boerewors with two dipping sauces',          0),
    ('Umngqusho Soup',           1,  55.00, 'Warm samp and bean soup with sour cream',                 1);

-- Mains (category_id = 2)
INSERT INTO menu_items (name, category_id, price, description, is_vegetarian) VALUES
    ('Bunny Chow (Mutton)',      2, 119.00, 'Traditional Durban bunny chow with mutton curry',         0),
    ('Bunny Chow (Veg)',         2,  95.00, 'Durban bunny chow with spiced vegetables',                1),
    ('Chakalaka Burger',         2, 105.00, 'Beef patty, chakalaka, cheddar, brioche bun, fries',     0),
    ('Boerewors Roll',           2,  85.00, 'Classic SA street food with tomato and onion relish',     0),
    ('Pap & Wors',               2,  95.00, 'Pap, boerewors, tomato relish, side salad',              0),
    ('Durban Prawn Curry',       2, 189.00, 'Spicy Durban prawn curry with rice and roti',             0),
    ('Chicken Schnitzel',        2, 135.00, 'Crumbed chicken breast, chips, coleslaw',                 0),
    ('Vegetarian Bobotie',       2,  98.00, 'Cape Malay bobotie with lentils, yellow rice, chutney',  1),
    ('Grilled Kingklip',         2, 215.00, 'Line fish, lemon butter sauce, seasonal vegetables',      0),
    ('Braai Platter (2 pax)',    2, 299.00, 'Chops, boerewors, chicken, pap, garlic bread',           0);

-- Desserts (category_id = 3)
INSERT INTO menu_items (name, category_id, price, description, is_vegetarian) VALUES
    ('Malva Pudding',            3,  58.00, 'Warm malva pudding, vanilla custard or ice cream',        1),
    ('Koeksister',               3,  38.00, 'Two syrup-soaked plaited doughnuts',                     1),
    ('Milk Tart',                3,  45.00, 'Traditional melktert with cinnamon dusting',              1),
    ('Amarula Cheesecake',       3,  72.00, 'Baked cheesecake with Amarula cream, chocolate crumb',   1),
    ('Peppermint Crisp Tart',    3,  52.00, 'Classic South African no-bake tart',                      1);

-- Drinks (category_id = 4)
INSERT INTO menu_items (name, category_id, price, description, is_vegetarian, is_vegan) VALUES
    ('Rooibos Iced Tea',         4,  35.00, 'Sweetened rooibos, lemon, fresh mint',                   1, 1),
    ('Mango Lassi',              4,  42.00, 'Fresh mango, yoghurt, cardamom',                          1, 0),
    ('Craft Lager (500ml)',      4,  58.00, 'Local craft lager on tap',                                1, 1),
    ('Springbokkies',            4,  45.00, 'Layered crème de menthe and Amarula shot',                1, 0),
    ('Still Water (750ml)',      4,  22.00, 'Chilled still water',                                     1, 1),
    ('Sparkling Water (750ml)',  4,  25.00, 'Chilled sparkling water',                                 1, 1),
    ('Cape Winelands Red',       4,  85.00, 'Glass of house Cabernet Sauvignon',                       1, 1),
    ('Cape Winelands White',     4,  85.00, 'Glass of house Chenin Blanc',                             1, 1),
    ('Amarula on Ice',           4,  65.00, 'Amarula cream liqueur served over ice',                   1, 0),
    ('Freshly Squeezed OJ',      4,  38.00, 'Orange juice, freshly pressed',                           1, 1);


-- ──────────────────────────────────────────────────────────────
--  SECTION 4: SEED DATA – Tables, Staff, Customers, Orders
-- ──────────────────────────────────────────────────────────────

INSERT INTO tables (table_number, capacity, location) VALUES
    (1, 2, 'Indoor'), (2, 4, 'Indoor'), (3, 4, 'Indoor'),
    (4, 6, 'Indoor'), (5, 6, 'Outdoor'), (6, 4, 'Outdoor'),
    (7, 8, 'Outdoor'), (8, 2, 'Bar'), (9, 4, 'Indoor'),
    (10, 10, 'Private Room');

INSERT INTO staff (first_name, last_name, role, email, phone) VALUES
    ('Sipho',   'Dlamini',  'Manager', 'sipho@ubuntukitchen.co.za',   '0821110001'),
    ('Lerato',  'Mokoena',  'Waiter',  'lerato@ubuntukitchen.co.za',  '0821110002'),
    ('Thabo',   'Nkosi',    'Waiter',  'thabo@ubuntukitchen.co.za',   '0821110003'),
    ('Zanele',  'Khumalo',  'Chef',    'zanele@ubuntukitchen.co.za',  '0821110004'),
    ('Pieter',  'van Wyk',  'Chef',    'pieter@ubuntukitchen.co.za',  '0821110005');

INSERT INTO customers (first_name, last_name, email, phone, loyalty_points) VALUES
    ('Alice',   'Dlamini',  'alice@example.co.za',  '0821234567', 120),
    ('Bob',     'Ndlovu',   'bob@example.co.za',    '0739876543',  45),
    ('Carol',   'Mokoena',  'carol@example.co.za',  '0611234567', 310),
    ('David',   'Park',     'david@example.co.za',  '0829991234',  80),
    ('Amara',   'Okafor',   'amara@example.co.za',  '0741112222', 200),
    ('Zara',    'Williams', 'zara@example.co.za',   '0831234567',  15);

INSERT INTO orders (customer_id, table_id, staff_id, status, created_at, served_at) VALUES
    (1, 4, 2, 'served',  '2026-06-20 12:15', '2026-06-20 13:05'),
    (2, 7, 3, 'served',  '2026-06-20 13:00', '2026-06-20 13:50'),
    (3, 2, 2, 'served',  '2026-06-21 19:30', '2026-06-21 20:25'),
    (4, 5, 3, 'served',  '2026-06-21 20:00', '2026-06-21 21:00'),
    (5, 9, 2, 'served',  '2026-06-22 12:45', '2026-06-22 13:30'),
    (1, 1, 3, 'served',  '2026-06-22 19:00', '2026-06-22 20:00'),
    (6, 6, 2, 'pending', '2026-06-27 10:00', NULL);

INSERT INTO order_items (order_id, item_id, quantity, unit_price) VALUES
    -- Order 1 (Alice): Vetkoek, Bunny Chow Mutton, Malva Pudding, Rooibos x2
    (1, 1,  1,  45.00),
    (1, 6,  1, 119.00),
    (1, 16, 1,  58.00),
    (1, 21, 2,  35.00),
    -- Order 2 (Bob): Boerewors Roll x2, Craft Lager x2, Koeksister x2
    (2, 9,  2,  85.00),
    (2, 23, 2,  58.00),
    (2, 17, 2,  38.00),
    -- Order 3 (Carol): Peri-Peri Wings, Durban Prawn Curry, Amarula Cheesecake, Cape White x2
    (3, 2,  1,  89.00),
    (3, 11, 1, 189.00),
    (3, 19, 1,  72.00),
    (3, 28, 2,  85.00),
    -- Order 4 (David): Chakalaka Burger, Pap & Wors, Milk Tart, Craft Lager
    (4, 8,  1, 105.00),
    (4, 10, 1,  95.00),
    (4, 18, 1,  45.00),
    (4, 23, 1,  58.00),
    -- Order 5 (Amara): Veg Bunny Chow, Veg Bobotie, Peppermint Crisp, Rooibos, Mango Lassi
    (5, 7,  1,  95.00),
    (5, 13, 1,  98.00),
    (5, 20, 1,  52.00),
    (5, 21, 1,  35.00),
    (5, 22, 1,  42.00),
    -- Order 6 (Alice again): Braai Platter, Cape Red x2, Malva Pudding x2
    (6, 15, 1, 299.00),
    (6, 27, 2,  85.00),
    (6, 16, 2,  58.00),
    -- Order 7 (Zara, pending): Chicken Schnitzel, Still Water
    (7, 12, 1, 135.00),
    (7, 25, 1,  22.00);

INSERT INTO reservations (customer_id, table_id, staff_id, party_size, date_time, status, special_notes) VALUES
    (1, 4, 2, 2, '2026-06-27 12:00', 'confirmed', 'Birthday – please arrange a candle'),
    (3, 10, 3, 8, '2026-06-27 19:00', 'confirmed', 'Corporate dinner – quiet room please'),
    (5, 5, 2, 4, '2026-06-28 13:00', 'confirmed', 'Vegetarian guests');


-- ──────────────────────────────────────────────────────────────
--  SECTION 5: USEFUL SQL QUERIES FOR EXAM PRACTICE
-- ──────────────────────────────────────────────────────────────

-- Query 1: View full menu with category names
SELECT
    m.item_id,
    c.name        AS category,
    m.name        AS dish,
    m.price,
    CASE WHEN m.is_vegetarian = 1 THEN 'Yes' ELSE 'No' END AS vegetarian
FROM menu_items m
JOIN categories c ON m.category_id = c.category_id
WHERE m.is_available = 1
ORDER BY c.name, m.price;

-- Query 2: Top 5 most ordered dishes
SELECT
    mi.name         AS dish,
    SUM(oi.quantity) AS total_ordered
FROM order_items oi
JOIN menu_items mi ON oi.item_id = mi.item_id
GROUP BY mi.name
ORDER BY total_ordered DESC
LIMIT 5;

-- Query 3: Total revenue per order (subtotal before VAT)
SELECT
    o.order_id,
    c.first_name || ' ' || c.last_name  AS customer,
    o.status,
    SUM(oi.quantity * oi.unit_price)    AS subtotal,
    ROUND(SUM(oi.quantity * oi.unit_price) * 1.15, 2) AS total_with_vat
FROM orders o
JOIN customers c      ON o.customer_id = c.customer_id
JOIN order_items oi   ON o.order_id = oi.order_id
GROUP BY o.order_id
ORDER BY o.order_id;

-- Query 4: All vegetarian dishes under R100
SELECT name, price
FROM menu_items
WHERE is_vegetarian = 1
  AND price < 100
  AND is_available = 1
ORDER BY price;

-- Query 5: Revenue by category
SELECT
    cat.name        AS category,
    COUNT(oi.order_item_id) AS items_sold,
    SUM(oi.quantity * oi.unit_price) AS revenue
FROM order_items oi
JOIN menu_items mi  ON oi.item_id = mi.item_id
JOIN categories cat ON mi.category_id = cat.category_id
JOIN orders o       ON oi.order_id = o.order_id
WHERE o.status = 'served'
GROUP BY cat.name
ORDER BY revenue DESC;

-- Query 6: Customers who have ordered more than once
SELECT
    c.first_name || ' ' || c.last_name AS customer,
    COUNT(o.order_id) AS order_count,
    SUM(oi.quantity * oi.unit_price) AS total_spent
FROM customers c
JOIN orders o       ON c.customer_id = o.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'served'
GROUP BY c.customer_id
HAVING COUNT(o.order_id) > 1
ORDER BY total_spent DESC;

-- Query 7: Which staff member generated the most revenue?
SELECT
    s.first_name || ' ' || s.last_name AS staff_member,
    s.role,
    COUNT(o.order_id)  AS orders_served,
    SUM(oi.quantity * oi.unit_price) AS total_revenue
FROM staff s
JOIN orders o       ON s.staff_id = o.staff_id
JOIN order_items oi ON o.order_id = oi.order_id
WHERE o.status = 'served'
GROUP BY s.staff_id
ORDER BY total_revenue DESC;

-- Query 8: Find available tables for a party of 4
SELECT table_number, capacity, location
FROM tables
WHERE capacity >= 4
ORDER BY capacity;

-- Query 9: Average dish price per category
SELECT
    c.name AS category,
    ROUND(AVG(m.price), 2) AS avg_price,
    MIN(m.price) AS cheapest,
    MAX(m.price) AS most_expensive
FROM menu_items m
JOIN categories c ON m.category_id = c.category_id
GROUP BY c.name;

-- Query 10: Today's pending orders
SELECT
    o.order_id,
    t.table_number,
    c.first_name || ' ' || c.last_name AS customer,
    o.status,
    o.created_at
FROM orders o
JOIN tables t    ON o.table_id = t.table_id
JOIN customers c ON o.customer_id = c.customer_id
WHERE o.status != 'served'
  AND o.status != 'cancelled'
ORDER BY o.created_at;