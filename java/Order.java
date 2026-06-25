// ═══════════════════════════════════════════════════════════════
//  Digital Restaurant – Order.java
//  GKSS Richfield Bryanston · Exam Prep Workshop
//  OOP Module: Composition, ArrayList, Method chaining concepts
// ═══════════════════════════════════════════════════════════════
package digitalrestaurant;

import java.time.LocalDateTime;
import java.time.format.DateTimeFormatter;
import java.util.ArrayList;
import java.util.List;

public class Order {

    // ── Constants ─────────────────────────────────────────────
    public static final double VAT_RATE            = 0.15;
    public static final double SERVICE_CHARGE_RATE = 0.10;

    // ── Inner class: OrderItem (composition) ──────────────────
    public static class OrderItem {
        private final MenuItem menuItem;
        private int quantity;

        public OrderItem(MenuItem menuItem, int quantity) {
            if (quantity < 1) throw new IllegalArgumentException("Quantity must be >= 1.");
            this.menuItem = menuItem;
            this.quantity = quantity;
        }

        public MenuItem  getMenuItem() { return menuItem;  }
        public int       getQuantity() { return quantity;  }
        public void      addQuantity(int n) { quantity += n; }

        public double getSubtotal() {
            return Math.round(menuItem.getPrice() * quantity * 100.0) / 100.0;
        }

        @Override
        public String toString() {
            return String.format("%dx %-30s R%7.2f",
                    quantity, menuItem.getName(), getSubtotal());
        }
    }

    // ── Fields ────────────────────────────────────────────────
    private final int           orderId;
    private final String        customerName;
    private final int           tableNumber;
    private final List<OrderItem> items;
    private       String        status;
    private final LocalDateTime createdAt;
    private       String        notes;

    // ── Constructor ───────────────────────────────────────────
    public Order(int orderId, String customerName, int tableNumber) {
        this.orderId      = orderId;
        this.customerName = customerName;
        this.tableNumber  = tableNumber;
        this.items        = new ArrayList<>();
        this.status       = "pending";
        this.createdAt    = LocalDateTime.now();
        this.notes        = "";
    }

    // ── Item management ───────────────────────────────────────
    public void addItem(MenuItem item, int quantity) {
        if (!item.isAvailable())
            throw new IllegalStateException(item.getName() + " is not available.");
        // Check if already in order
        for (OrderItem oi : items) {
            if (oi.getMenuItem().getItemId() == item.getItemId()) {
                oi.addQuantity(quantity);
                return;
            }
        }
        items.add(new OrderItem(item, quantity));
    }

    public void addItem(MenuItem item) { addItem(item, 1); }

    public boolean removeItem(int itemId) {
        return items.removeIf(oi -> oi.getMenuItem().getItemId() == itemId);
    }

    // ── Calculations ──────────────────────────────────────────
    public double getSubtotal() {
        return Math.round(items.stream()
                .mapToDouble(OrderItem::getSubtotal)
                .sum() * 100.0) / 100.0;
    }

    public double getVatAmount() {
        return Math.round(getSubtotal() * VAT_RATE * 100.0) / 100.0;
    }

    public double getServiceCharge() {
        return Math.round(getSubtotal() * SERVICE_CHARGE_RATE * 100.0) / 100.0;
    }

    public double getTotal() {
        return Math.round((getSubtotal() + getVatAmount() + getServiceCharge()) * 100.0) / 100.0;
    }

    // ── Getters & Setters ─────────────────────────────────────
    public int           getOrderId()      { return orderId;      }
    public String        getCustomerName() { return customerName; }
    public int           getTableNumber()  { return tableNumber;  }
    public String        getStatus()       { return status;       }
    public List<OrderItem> getItems()      { return items;        }

    public void setStatus(String status) {
        String[] valid = {"pending","confirmed","preparing","ready","served","cancelled"};
        for (String s : valid) { if (s.equals(status)) { this.status = status; return; } }
        throw new IllegalArgumentException("Invalid status: " + status);
    }

    public void setNotes(String notes) { this.notes = notes; }

    // ── Receipt ───────────────────────────────────────────────
    public void printReceipt() {
        String line  = "═".repeat(48);
        String dline = "─".repeat(48);
        DateTimeFormatter fmt = DateTimeFormatter.ofPattern("yyyy-MM-dd HH:mm");

        System.out.println("\n" + line);
        System.out.println("  THE DIGITAL RESTAURANT");
        System.out.printf ("  Receipt – Order #%d%n", orderId);
        System.out.printf ("  Table %d | %s%n", tableNumber, createdAt.format(fmt));
        System.out.printf ("  Customer: %s%n", customerName);
        System.out.println(dline);
        for (OrderItem oi : items) {
            System.out.println("  " + oi);
        }
        System.out.println(dline);
        System.out.printf ("  %-36s R%7.2f%n", "Subtotal",         getSubtotal());
        System.out.printf ("  %-36s R%7.2f%n", "VAT (15%)",        getVatAmount());
        System.out.printf ("  %-36s R%7.2f%n", "Service (10%)",    getServiceCharge());
        System.out.println(dline);
        System.out.printf ("  %-36s R%7.2f%n", "TOTAL",            getTotal());
        if (!notes.isEmpty()) System.out.printf("\n  Notes: %s%n", notes);
        System.out.println(line + "\n");
    }

    @Override
    public String toString() {
        return String.format("Order(#%d, Table %d, %s, R%.2f)",
                orderId, tableNumber, status, getTotal());
    }
}