// ═══════════════════════════════════════════════════════════════
//  Digital Restaurant – MenuItem.java
//  GKSS Richfield Bryanston · Exam Prep Workshop
//  OOP Module: Encapsulation, Getters, Setters, Constructors
// ═══════════════════════════════════════════════════════════════
package digitalrestaurant;

public class MenuItem {

    // ── Fields (private = encapsulation) ──────────────────────
    private int    itemId;
    private String name;
    private String category;
    private double price;
    private String description;
    private boolean available;

    // ── Constructors ──────────────────────────────────────────
    public MenuItem(int itemId, String name, String category, double price) {
        this(itemId, name, category, price, "", true);
    }

    public MenuItem(int itemId, String name, String category,
                    double price, String description, boolean available) {
        this.itemId      = itemId;
        this.name        = name;
        this.category    = category;
        setPrice(price);  // use setter for validation
        this.description = description;
        this.available   = available;
    }

    // ── Getters ───────────────────────────────────────────────
    public int     getItemId()      { return itemId;      }
    public String  getName()        { return name;        }
    public String  getCategory()    { return category;    }
    public double  getPrice()       { return price;       }
    public String  getDescription() { return description; }
    public boolean isAvailable()    { return available;   }

    // ── Setters (with validation) ──────────────────────────────
    public void setPrice(double price) {
        if (price < 0) throw new IllegalArgumentException("Price cannot be negative.");
        this.price = Math.round(price * 100.0) / 100.0;
    }

    public void setAvailable(boolean available) {
        this.available = available;
    }

    public void setDescription(String description) {
        this.description = description;
    }

    // ── Business logic ────────────────────────────────────────
    public double applyDiscount(double percent) {
        if (percent <= 0 || percent > 100)
            throw new IllegalArgumentException("Discount must be between 1 and 100.");
        return Math.round(price * (1 - percent / 100) * 100.0) / 100.0;
    }

    // ── toString ──────────────────────────────────────────────
    @Override
    public String toString() {
        String status = available ? "✓" : "✗";
        return String.format("[%s] %s (%s) – R%.2f", status, name, category, price);
    }
}