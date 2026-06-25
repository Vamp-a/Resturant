// ═══════════════════════════════════════════════════════════════
//  Digital Restaurant – restaurant.cpp
//  GKSS Richfield Bryanston · Exam Prep Workshop
//  C++ Module: Classes, Structs, Vectors, References, Pointers
//  Compile: g++ -std=c++17 -o restaurant restaurant.cpp && ./restaurant
// ═══════════════════════════════════════════════════════════════

#include <iostream>
#include <iomanip>
#include <string>
#include <vector>
#include <algorithm>
#include <stdexcept>
#include <sstream>
#include <ctime>

using namespace std;

// ─────────────────────────────────────────────────────────────
//  STRUCT: MenuItemRecord (C-style, exam often asks about structs)
// ─────────────────────────────────────────────────────────────
struct MenuItemRecord {
    int    id;
    string name;
    string category;
    double price;
    bool   available;
};


// ─────────────────────────────────────────────────────────────
//  CLASS: MenuItem (OOP version)
//  Encapsulation, constructor overloading, const methods
// ─────────────────────────────────────────────────────────────
class MenuItem {
private:
    int    m_id;
    string m_name;
    string m_category;
    double m_price;
    string m_description;
    bool   m_available;

public:
    // Default constructor
    MenuItem() : m_id(0), m_price(0.0), m_available(true) {}

    // Parameterised constructor
    MenuItem(int id, const string& name, const string& category,
             double price, const string& desc = "", bool available = true)
        : m_id(id), m_name(name), m_category(category),
          m_description(desc), m_available(available) {
        setPrice(price);
    }

    // Getters (const = doesn't modify object)
    int    getId()          const { return m_id;          }
    string getName()        const { return m_name;        }
    string getCategory()    const { return m_category;    }
    double getPrice()       const { return m_price;       }
    string getDescription() const { return m_description; }
    bool   isAvailable()    const { return m_available;   }

    // Setters with validation
    void setPrice(double price) {
        if (price < 0) throw invalid_argument("Price cannot be negative.");
        m_price = round(price * 100.0) / 100.0;
    }
    void setAvailable(bool avail) { m_available = avail; }

    // Business logic
    double applyDiscount(double percent) const {
        if (percent <= 0 || percent > 100)
            throw invalid_argument("Discount must be 1–100.");
        return round(m_price * (1.0 - percent / 100.0) * 100.0) / 100.0;
    }

    // Overloaded stream operator
    friend ostream& operator<<(ostream& os, const MenuItem& m) {
        os << "[" << (m.m_available ? "✓" : "✗") << "] "
           << left << setw(32) << m.m_name
           << " (" << m.m_category << ")  R"
           << fixed << setprecision(2) << m.m_price;
        return os;
    }
};


// ─────────────────────────────────────────────────────────────
//  CLASS: OrderItem (composition inside Order)
// ─────────────────────────────────────────────────────────────
class OrderItem {
private:
    MenuItem m_menuItem;
    int      m_quantity;

public:
    OrderItem(const MenuItem& item, int qty) : m_menuItem(item) {
        if (qty < 1) throw invalid_argument("Quantity >= 1 required.");
        m_quantity = qty;
    }

    const MenuItem& getMenuItem() const { return m_menuItem; }
    int             getQuantity() const { return m_quantity; }
    void            addQty(int n)       { m_quantity += n;   }

    double getSubtotal() const {
        return round(m_menuItem.getPrice() * m_quantity * 100.0) / 100.0;
    }

    friend ostream& operator<<(ostream& os, const OrderItem& oi) {
        os << setw(2) << oi.m_quantity << "x  "
           << left << setw(30) << oi.m_menuItem.getName()
           << "  R" << fixed << setprecision(2) << oi.getSubtotal();
        return os;
    }
};


// ─────────────────────────────────────────────────────────────
//  CLASS: Order
//  Demonstrates: vector, range-for, references, const methods
// ─────────────────────────────────────────────────────────────
class Order {
public:
    static constexpr double VAT_RATE     = 0.15;
    static constexpr double SERVICE_RATE = 0.10;

private:
    int                 m_orderId;
    string              m_customerName;
    int                 m_tableNumber;
    vector<OrderItem>   m_items;
    string              m_status;
    string              m_notes;

public:
    Order(int id, const string& customerName, int tableNum)
        : m_orderId(id), m_customerName(customerName),
          m_tableNumber(tableNum), m_status("pending") {}

    // Add or update item in order
    void addItem(const MenuItem& item, int qty = 1) {
        if (!item.isAvailable())
            throw runtime_error(item.getName() + " is unavailable.");
        for (auto& oi : m_items) {
            if (oi.getMenuItem().getId() == item.getId()) {
                oi.addQty(qty);
                return;
            }
        }
        m_items.emplace_back(item, qty);
    }

    // Remove item by id
    void removeItem(int itemId) {
        m_items.erase(
            remove_if(m_items.begin(), m_items.end(),
                [itemId](const OrderItem& oi) {
                    return oi.getMenuItem().getId() == itemId;
                }),
            m_items.end()
        );
    }

    // Calculations
    double getSubtotal() const {
        double total = 0.0;
        for (const auto& oi : m_items) total += oi.getSubtotal();
        return round(total * 100.0) / 100.0;
    }
    double getVat()     const { return round(getSubtotal() * VAT_RATE     * 100.0) / 100.0; }
    double getService() const { return round(getSubtotal() * SERVICE_RATE * 100.0) / 100.0; }
    double getTotal()   const { return round((getSubtotal() + getVat() + getService()) * 100.0) / 100.0; }

    void setStatus(const string& status) { m_status = status; }
    void setNotes(const string& notes)   { m_notes  = notes;  }

    // Print receipt
    void printReceipt() const {
        string line  = string(50, '=');
        string dline = string(50, '-');
        cout << "\n" << line << "\n";
        cout << "  THE DIGITAL RESTAURANT\n";
        cout << "  Receipt - Order #" << m_orderId << "\n";
        cout << "  Table " << m_tableNumber << "  |  Customer: " << m_customerName << "\n";
        cout << dline << "\n";
        for (const auto& oi : m_items) {
            cout << "  " << oi << "\n";
        }
        cout << dline << "\n";
        cout << fixed << setprecision(2);
        cout << "  " << left << setw(38) << "Subtotal"         << "R" << getSubtotal() << "\n";
        cout << "  " << left << setw(38) << "VAT (15%)"        << "R" << getVat()      << "\n";
        cout << "  " << left << setw(38) << "Service (10%)"    << "R" << getService()  << "\n";
        cout << dline << "\n";
        cout << "  " << left << setw(38) << "TOTAL"            << "R" << getTotal()    << "\n";
        if (!m_notes.empty()) cout << "\n  Notes: " << m_notes << "\n";
        cout << line << "\n\n";
    }
};


// ─────────────────────────────────────────────────────────────
//  SORTING ALGORITHMS (exam-relevant)
// ─────────────────────────────────────────────────────────────

// Bubble Sort – O(n²)
void bubbleSortByPrice(vector<MenuItem>& items) {
    int n = items.size();
    for (int i = 0; i < n - 1; i++) {
        for (int j = 0; j < n - i - 1; j++) {
            if (items[j].getPrice() > items[j + 1].getPrice()) {
                swap(items[j], items[j + 1]);
            }
        }
    }
}

// Selection Sort – O(n²)
void selectionSortByPrice(vector<MenuItem>& items) {
    int n = items.size();
    for (int i = 0; i < n - 1; i++) {
        int minIdx = i;
        for (int j = i + 1; j < n; j++) {
            if (items[j].getPrice() < items[minIdx].getPrice())
                minIdx = j;
        }
        swap(items[i], items[minIdx]);
    }
}

// Linear Search – O(n)
const MenuItem* linearSearch(const vector<MenuItem>& items, const string& name) {
    for (const auto& item : items) {
        if (item.getName().find(name) != string::npos) return &item;
    }
    return nullptr;
}

// ─────────────────────────────────────────────────────────────
//  MAIN
// ─────────────────────────────────────────────────────────────
int main() {
    cout << "\n" << string(60, '=') << "\n";
    cout << "  THE DIGITAL RESTAURANT – C++ Demo\n";
    cout << "  GKSS Richfield Bryanston – Exam Prep Workshop\n";
    cout << string(60, '=') << "\n";

    // ── Build menu ────────────────────────────────────────────
    vector<MenuItem> menu = {
        MenuItem(1,  "Vetkoek with Mince",       "Starter",  45.00, "Deep-fried dough with spiced mince"),
        MenuItem(2,  "Peri-Peri Chicken Wings",  "Starter",  89.00, "Crispy wings with peri-peri sauce"),
        MenuItem(3,  "Chakalaka Spring Rolls",   "Starter",  65.00, "Crispy rolls with chakalaka"),
        MenuItem(4,  "Bunny Chow (Mutton)",      "Main",    119.00, "Durban bunny chow"),
        MenuItem(5,  "Chakalaka Burger",         "Main",    105.00, "Beef patty, chakalaka, cheddar"),
        MenuItem(6,  "Boerewors Roll",           "Main",     85.00, "Classic SA street food"),
        MenuItem(7,  "Pap & Wors",              "Main",     95.00, "Pap, boerewors, relish"),
        MenuItem(8,  "Durban Prawn Curry",       "Main",    189.00, "Spicy prawn curry"),
        MenuItem(9,  "Grilled Kingklip",         "Main",    215.00, "Line fish, lemon butter"),
        MenuItem(10, "Malva Pudding",            "Dessert",  58.00, "Warm malva, custard"),
        MenuItem(11, "Koeksister",               "Dessert",  38.00, "Syrup-soaked doughnuts"),
        MenuItem(12, "Milk Tart",               "Dessert",  45.00, "Traditional melktert"),
        MenuItem(13, "Rooibos Iced Tea",         "Drink",    35.00, "Rooibos, lemon, mint"),
        MenuItem(14, "Craft Lager (500ml)",      "Drink",    58.00, "Local craft lager"),
        MenuItem(15, "Cape Winelands Red",       "Drink",    85.00, "House red wine"),
    };

    // Display menu
    cout << "\n" << string(55, '=') << "\n  UBUNTU KITCHEN – MENU\n" << string(55, '=') << "\n";
    for (const auto& item : menu) cout << "  " << item << "\n";

    // ── Place an order ────────────────────────────────────────
    Order order1(1001, "Alice Dlamini", 4);
    const MenuItem* vetkoek = linearSearch(menu, "Vetkoek");
    const MenuItem* bunny   = linearSearch(menu, "Bunny Chow");
    const MenuItem* malva   = linearSearch(menu, "Malva Pudding");
    const MenuItem* rooibos = linearSearch(menu, "Rooibos");

    if (vetkoek) order1.addItem(*vetkoek, 1);
    if (bunny)   order1.addItem(*bunny,   1);
    if (malva)   order1.addItem(*malva,   1);
    if (rooibos) order1.addItem(*rooibos, 2);
    order1.setNotes("No coriander please.");
    order1.setStatus("served");
    order1.printReceipt();

    // ── Sorting demo ──────────────────────────────────────────
    vector<MenuItem> menuCopy = menu;
    bubbleSortByPrice(menuCopy);
    cout << "Menu sorted cheapest → most expensive (Bubble Sort):\n";
    cout << string(45, '-') << "\n";
    for (size_t i = 0; i < min((size_t)5, menuCopy.size()); i++) {
        cout << "  " << left << setw(32) << menuCopy[i].getName()
             << "  R" << fixed << setprecision(2) << menuCopy[i].getPrice() << "\n";
    }

    // ── Struct demo ───────────────────────────────────────────
    cout << "\n--- STRUCT DEMO ---\n";
    MenuItemRecord rec = {99, "Umngqusho Soup", "Starter", 55.00, true};
    cout << "Struct item: " << rec.name << "  R" << fixed << setprecision(2) << rec.price << "\n";

    // ── Pointer demo ──────────────────────────────────────────
    cout << "\n--- POINTER DEMO ---\n";
    MenuItem* ptr = &menuCopy[0];
    cout << "Pointer to cheapest item: " << ptr->getName()
         << "  R" << fixed << setprecision(2) << ptr->getPrice() << "\n";
    cout << "Dereference: (*ptr).getName() = " << (*ptr).getName() << "\n";

    cout << "\n" << string(60, '=') << "\n";
    cout << "  C++ Demo complete. Concepts covered:\n";
    cout << "  Classes, Structs, Vectors, Const, Refs, Pointers\n";
    cout << "  Bubble Sort, Selection Sort, Linear Search\n";
    cout << "  Operator Overloading (<<), Constructor Overloading\n";
    cout << string(60, '=') << "\n\n";

    return 0;
}