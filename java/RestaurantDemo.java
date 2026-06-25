// ═══════════════════════════════════════════════════════════════
//  Digital Restaurant – RestaurantDemo.java
//  GKSS Richfield Bryanston · Exam Prep Workshop
//  Run this file: javac *.java && java digitalrestaurant.RestaurantDemo
// ═══════════════════════════════════════════════════════════════
package digitalrestaurant;

import java.util.ArrayList;
import java.util.List;

public class RestaurantDemo {

    // ── Build the full menu ────────────────────────────────────
    static List<MenuItem> buildMenu() {
        List<MenuItem> menu = new ArrayList<>();

        // Starters
        menu.add(new MenuItem(1,  "Vetkoek with Mince",        "Starter",  45.00));
        menu.add(new MenuItem(2,  "Peri-Peri Chicken Wings",   "Starter",  89.00));
        menu.add(new MenuItem(3,  "Chakalaka Spring Rolls",    "Starter",  65.00));
        menu.add(new MenuItem(4,  "Boerewors Bites",           "Starter",  72.00));

        // Mains
        menu.add(new MenuItem(5,  "Bunny Chow (Mutton)",       "Main",    119.00));
        menu.add(new MenuItem(6,  "Chakalaka Burger",          "Main",    105.00));
        menu.add(new MenuItem(7,  "Boerewors Roll",            "Main",     85.00));
        menu.add(new MenuItem(8,  "Pap & Wors",               "Main",     95.00));
        menu.add(new MenuItem(9,  "Durban Prawn Curry",        "Main",    189.00));
        menu.add(new MenuItem(10, "Chicken Schnitzel",         "Main",    135.00));
        menu.add(new MenuItem(11, "Vegetarian Bobotie",        "Main",     98.00));
        menu.add(new MenuItem(12, "Grilled Kingklip",          "Main",    215.00));

        // Desserts
        menu.add(new MenuItem(13, "Malva Pudding",             "Dessert",  58.00));
        menu.add(new MenuItem(14, "Koeksister",                "Dessert",  38.00));
        menu.add(new MenuItem(15, "Milk Tart",                "Dessert",  45.00));
        menu.add(new MenuItem(16, "Amarula Cheesecake",        "Dessert",  72.00));

        // Drinks
        menu.add(new MenuItem(17, "Rooibos Iced Tea",          "Drink",    35.00));
        menu.add(new MenuItem(18, "Mango Lassi",               "Drink",    42.00));
        menu.add(new MenuItem(19, "Craft Lager (500ml)",       "Drink",    58.00));
        menu.add(new MenuItem(20, "Cape Winelands Red",        "Drink",    85.00));
        menu.add(new MenuItem(21, "Cape Winelands White",      "Drink",    85.00));
        menu.add(new MenuItem(22, "Still Water (750ml)",       "Drink",    22.00));

        return menu;
    }

    // ── Helper: find item by name ──────────────────────────────
    static MenuItem find(List<MenuItem> menu, String name) {
        String target = name.toLowerCase();
        for (MenuItem m : menu) {
            if (m.getName().toLowerCase().contains(target)) return m;
        }
        throw new RuntimeException("Item not found: " + name);
    }

    // ── Sort menu by price (Bubble Sort for exam) ──────────────
    static List<MenuItem> bubbleSortByPrice(List<MenuItem> menu) {
        List<MenuItem> sorted = new ArrayList<>(menu);
        int n = sorted.size();
        for (int i = 0; i < n - 1; i++) {
            for (int j = 0; j < n - i - 1; j++) {
                if (sorted.get(j).getPrice() > sorted.get(j + 1).getPrice()) {
                    MenuItem temp = sorted.get(j);
                    sorted.set(j, sorted.get(j + 1));
                    sorted.set(j + 1, temp);
                }
            }
        }
        return sorted;
    }

    // ── Display full menu ──────────────────────────────────────
    static void displayMenu(List<MenuItem> menu) {
        String[] categories = {"Starter", "Main", "Dessert", "Drink"};
        System.out.println("\n" + "═".repeat(55));
        System.out.println("  UBUNTU KITCHEN – MENU");
        System.out.println("═".repeat(55));
        for (String cat : categories) {
            System.out.println("\n  " + cat.toUpperCase());
            System.out.println("  " + "─".repeat(45));
            for (MenuItem item : menu) {
                if (item.getCategory().equals(cat)) {
                    System.out.printf("  %3d.  %-30s  R%6.2f%n",
                            item.getItemId(), item.getName(), item.getPrice());
                }
            }
        }
        System.out.println("═".repeat(55) + "\n");
    }

    // ── Main ──────────────────────────────────────────────────
    public static void main(String[] args) {

        System.out.println("\n" + "=".repeat(58));
        System.out.println("  THE DIGITAL RESTAURANT – Java Demo");
        System.out.println("  GKSS Richfield Bryanston – Exam Prep Workshop");
        System.out.println("=".repeat(58));

        List<MenuItem> menu = buildMenu();
        displayMenu(menu);

        // ── Order 1: Alice ────────────────────────────────────
        Order order1 = new Order(1001, "Alice Dlamini", 4);
        order1.addItem(find(menu, "Vetkoek"), 1);
        order1.addItem(find(menu, "Bunny Chow"), 1);
        order1.addItem(find(menu, "Malva Pudding"), 1);
        order1.addItem(find(menu, "Rooibos"), 2);
        order1.setNotes("No coriander please.");
        order1.setStatus("served");
        order1.printReceipt();

        // ── Order 2: Bob ──────────────────────────────────────
        Order order2 = new Order(1002, "Bob Ndlovu", 7);
        order2.addItem(find(menu, "Boerewors Roll"), 2);
        order2.addItem(find(menu, "Craft Lager"), 2);
        order2.addItem(find(menu, "Koeksister"), 2);
        order2.setStatus("served");
        order2.printReceipt();

        // ── Sorting demo ──────────────────────────────────────
        System.out.println("Menu sorted cheapest → most expensive (Bubble Sort):");
        System.out.println("─".repeat(45));
        List<MenuItem> sorted = bubbleSortByPrice(menu);
        for (int i = 0; i < 5; i++) {
            MenuItem m = sorted.get(i);
            System.out.printf("  %-32s R%6.2f%n", m.getName(), m.getPrice());
        }
        System.out.println("  ... (showing top 5 cheapest)");

        // ── OOP concepts summary ──────────────────────────────
        System.out.println("\n" + "═".repeat(55));
        System.out.println("  OOP CONCEPTS DEMONSTRATED:");
        System.out.println("  Encapsulation – private fields with getters/setters");
        System.out.println("  Composition   – Order contains OrderItems (inner class)");
        System.out.println("  Abstraction   – printReceipt() hides calculation detail");
        System.out.println("  Validation    – price, discount, status checked in setters");
        System.out.println("═".repeat(55) + "\n");
    }
}