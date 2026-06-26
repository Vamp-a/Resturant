// ── RESTAURANT FUNCTIONS – EXAM PRACTICE ──────────────────
// Complete each function below. Test your code using the HTML page.

// ── TASK 1: Calculate Total Bill ──────────────────────────
// Write a function that calculates the total bill including VAT and service charge.
// Parameters: items (array of {name, price}), vatRate (number), serviceRate (number)
// Returns: total (number) with VAT and service added

function calculateTotal(items, vatRate, serviceRate) {
  // Write your code here

  // Step 1: Calculate subtotal
  let subtotal = 0;
  for (let i = 0; i < items.length; i++) {
    subtotal += items[i].price;
  }
  
  // Step 2: Add VAT
  const vat = subtotal * vatRate;
  
  // Step 3: Add service
  const service = subtotal * serviceRate;
  
  // Step 4: Return total
  return subtotal + vat + service;
}
  


// ── TASK 2: Apply Discount ────────────────────────────────
// Write a function that applies a percentage discount to a total.
// Parameters: total (number), discountPercent (number), customerType (string)
// Rules: Regular customers get the discount.
//        VIP customers get an extra 5% off (discount + 5%).
// Returns: discounted total (number)

function applyDiscount(total, discountPercent, customerType) {
  // Write your code here
  
}

// ── TASK 3: Sort Menu by Price ────────────────────────────
// Write a function that sorts a menu array by price.
// Parameters: menu (array of {name, price}), order (string: "asc" or "desc")
// Returns: sorted menu array

function sortMenuByPrice(menu, order) {
  // Write your code here
  
}

// ── TASK 4: Most Popular Dish ─────────────────────────────
// Write a function that finds the most ordered dish.
// Parameters: orders (array of {dish, qty})
// Returns: object {dish: string, totalQty: number}

function mostPopularDish(orders) {
  // Write your code here
  
}

// ── TASK 5: Debug the Broken Function ─────────────────────
// The original function below has errors. Write a fixed version.
// Rename it to "fixedOrderTotal" and fix ALL bugs.

// Original broken code:
// function orderTotal(items) {
//   let total = 0;
//   for (let i = 0; i < items.length; i++) {
//     total = total + items[i].price;
//   }
//   let vat = total * 0.15;
//   let service = total * 0.1;
//   let final = total + vat + service;
//   return final;
// }

// Write your fixed version here:
function fixedOrderTotal(items) {
  // Write your fixed code here
  
}

// ── BONUS: Code Golf Challenge ────────────────────────────
// Write the SHORTEST possible function that calculates total with VAT and service.
// One-liner encouraged! Use arrow functions, reduce(), and chaining.
// Parameters: items (array of {price})
// Returns: total (number) with VAT (15%) and service (10%)

const codeGolfTotal = (items) => {
  // Write your shortest solution here
  
};