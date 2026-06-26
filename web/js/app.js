/**
 * Digital Restaurant – app.js
 * GKSS Richfield Bryanston · Exam Prep Workshop
 *
 * Place this file in:  static/app.js
 *
 * In index.html, DELETE the entire <script>...</script> block and
 * replace it with this single line just before </body>:
 *
 *   <script src="/static/app.js"></script>
 */


// ─────────────────────────────────────────
//  MENU DATA
//  Starts empty. Filled from the database
//  via GET /api/menu when the page loads.
// ─────────────────────────────────────────
let MENU = [];


// ─────────────────────────────────────────
//  LOAD MENU FROM API
//  Fetches live data from Flask → SQLite.
//  Replaces the old hardcoded MENU array.
// ─────────────────────────────────────────
async function loadMenu() {
  try {
    const res = await fetch('/api/menu');
    if (!res.ok) throw new Error(`Server returned ${res.status}`);
    MENU = await res.json();
    renderMenu();
    renderCart();
  } catch (err) {
    document.getElementById('menuGrid').innerHTML = `
      <p style="color:#e07070; padding:1.5rem; grid-column:1/-1;">
        ⚠️ Could not load menu. Is the Flask server running?<br/>
        <small style="opacity:0.7">${err.message}</small>
      </p>`;
  }
}


// ─────────────────────────────────────────
//  RENDER MENU
//  Builds the menu grid from the MENU array.
//  Called after loadMenu() resolves.
// ─────────────────────────────────────────
function renderMenu() {
  const grid = document.getElementById('menuGrid');
  grid.innerHTML = MENU.map(item => `
    <div class="menu-card" data-cat="${item.cat}" id="card-${item.id}">
      <div>
        <div class="menu-card-header">
          <div class="menu-card-name">${item.name}</div>
          <div class="menu-card-price">R${parseFloat(item.price).toFixed(2)}</div>
        </div>
        <div class="menu-card-desc">${item.desc}</div>
        <div style="display:flex;gap:6px;margin-bottom:0.8rem;">
          ${item.veg ? '<span class="badge badge-veg">🌿 Veg</span>' : ''}
          ${item.hot ? '<span class="badge badge-hot">🌶️ Spicy</span>' : ''}
        </div>
      </div>
      <button class="add-to-order" onclick="addToCart(${item.id})">+ Add to Order</button>
    </div>
  `).join('');
}


// ─────────────────────────────────────────
//  FILTER MENU BY CATEGORY (tab buttons)
// ─────────────────────────────────────────
function filterMenu(cat, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.menu-card').forEach(card => {
    card.classList.toggle('hidden', cat !== 'all' && card.dataset.cat !== cat);
  });
}


// ─────────────────────────────────────────
//  CART
//  { itemId: quantity }
// ─────────────────────────────────────────
const cart = {};
let cartCollapsed = false;

function addToCart(id) {
  cart[id] = (cart[id] || 0) + 1;
  renderCart();
  showToast(`${MENU.find(m => m.id === id).name} added!`);
}

function changeQty(id, delta) {
  cart[id] = (cart[id] || 0) + delta;
  if (cart[id] <= 0) delete cart[id];
  renderCart();
}

function renderCart() {
  const ids    = Object.keys(cart);
  const badge  = document.getElementById('cartBadge');
  const items  = document.getElementById('cartItems');
  const footer = document.getElementById('cartFooter');
  const totals = document.getElementById('cartTotals');

  const totalQty = ids.reduce((s, id) => s + cart[id], 0);
  badge.textContent = totalQty === 0
    ? '0 items'
    : `${totalQty} item${totalQty > 1 ? 's' : ''}`;

  if (ids.length === 0) {
    items.innerHTML = '<div class="cart-empty">Your order is empty.<br/>Add dishes from the menu above.</div>';
    footer.style.display = 'none';
    return;
  }

  items.innerHTML = ids.map(id => {
    const item = MENU.find(m => m.id == id);
    const sub  = item.price * cart[id];
    return `
      <div class="cart-item">
        <div class="cart-item-name">${item.name}</div>
        <div class="cart-item-qty">
          <button class="qty-btn" onclick="changeQty(${id}, -1)">−</button>
          <span>${cart[id]}</span>
          <button class="qty-btn" onclick="changeQty(${id}, +1)">+</button>
        </div>
        <div class="cart-item-price">R${sub.toFixed(2)}</div>
      </div>`;
  }).join('');

  const subtotal = ids.reduce((s, id) => s + MENU.find(m => m.id == id).price * cart[id], 0);
  const vat      = subtotal * 0.15;
  const service  = subtotal * 0.10;
  const total    = subtotal + vat + service;

  totals.innerHTML = `
    <div class="total-line"><span>Subtotal</span>       <span>R${subtotal.toFixed(2)}</span></div>
    <div class="total-line"><span>VAT (15%)</span>      <span>R${vat.toFixed(2)}</span></div>
    <div class="total-line"><span>Service (10%)</span>  <span>R${service.toFixed(2)}</span></div>
    <div class="total-line grand"><span>TOTAL</span>    <span>R${total.toFixed(2)}</span></div>
  `;
  footer.style.display = 'block';
}

function toggleCart() {
  cartCollapsed = !cartCollapsed;
  document.getElementById('cartSidebar').classList.toggle('collapsed', cartCollapsed);
}


// ─────────────────────────────────────────
//  PLACE ORDER
//  POSTs the cart to POST /api/orders.
//  Flask saves each item to order_items.
// ─────────────────────────────────────────
async function placeOrder() {
  const items = Object.keys(cart).map(id => ({
    item_id:    parseInt(id),
    quantity:   cart[id],
    unit_price: MENU.find(m => m.id == id).price,
  }));

  try {
    const res = await fetch('/api/orders', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        customer_id: 1,   // placeholder – replace with real auth later
        table_id:    1,
        notes:       '',
        items,
      }),
    });

    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    const data = await res.json();
    showToast(`Order #${data.order_id} sent to the kitchen! 🍳`);
    Object.keys(cart).forEach(k => delete cart[k]);
    renderCart();

  } catch (err) {
    showToast('Could not place order – check the server.');
    console.error('placeOrder error:', err);
  }
}


// ─────────────────────────────────────────
//  TOAST NOTIFICATION
// ─────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}


// ─────────────────────────────────────────
//  FORM VALIDATION HELPER
// ─────────────────────────────────────────
function validate(id, errId, condition, msg) {
  const el  = document.getElementById(id);
  const err = document.getElementById(errId);
  if (!condition(el.value)) {
    el.classList.add('error');
    err.textContent = msg;
    return false;
  }
  el.classList.remove('error');
  err.textContent = '';
  return true;
}


// ─────────────────────────────────────────
//  SUBMIT RESERVATION
//  Validates the form, then POSTs to
//  POST /api/reservations.
//  Flask finds or creates the customer
//  and inserts the reservation row.
// ─────────────────────────────────────────
async function submitReservation() {
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('date').min = today;

  // All validation runs first – nothing is sent if any field fails
  let valid = true;
  valid &= validate('firstName', 'firstNameErr', v => v.trim().length >= 2,                  'Please enter your first name.');
  valid &= validate('lastName',  'lastNameErr',  v => v.trim().length >= 2,                  'Please enter your last name.');
  valid &= validate('email',     'emailErr',     v => /\S+@\S+\.\S+/.test(v),                'Please enter a valid email.');
  valid &= validate('phone',     'phoneErr',     v => /^\d{10}$/.test(v.replace(/\s/g, '')), 'Enter a 10-digit SA phone number.');
  valid &= validate('date',      'dateErr',      v => v && v >= today,                        'Please select a future date.');
  valid &= validate('time',      'timeErr',      v => v !== '',                               'Please select a time.');
  valid &= validate('guests',    'guestsErr',    v => v !== '',                               'Please select number of guests.');

  if (!valid) return;

  const payload = {
    firstName: document.getElementById('firstName').value.trim(),
    lastName:  document.getElementById('lastName').value.trim(),
    email:     document.getElementById('email').value.trim(),
    phone:     document.getElementById('phone').value.trim(),
    date:      document.getElementById('date').value,
    time:      document.getElementById('time').value,
    guests:    document.getElementById('guests').value,
    occasion:  document.getElementById('occasion').value,
    notes:     document.getElementById('notes').value.trim(),
  };

  try {
    const res = await fetch('/api/reservations', {
      method:  'POST',
      headers: { 'Content-Type': 'application/json' },
      body:    JSON.stringify(payload),
    });

    if (!res.ok) throw new Error(`Server returned ${res.status}`);

    // Show success UI
    document.getElementById('reservationForm').style.display = 'none';
    document.querySelector('.btn-submit').style.display      = 'none';
    document.getElementById('successMsg').style.display      = 'block';

  } catch (err) {
    showToast('Reservation failed – check the server.');
    console.error('submitReservation error:', err);
  }
}


// ─────────────────────────────────────────
//  INIT
//  loadMenu() fetches /api/menu, then
//  calls renderMenu() and renderCart().
// ─────────────────────────────────────────
loadMenu();
