// ── MENU DATA ──────────────────────────────────────────────
const MENU = [
  {id:1,  name:"Vetkoek with Mince",       cat:"starter", price:45.00,  desc:"Deep-fried dough filled with spiced mince",                  veg:false, hot:false},
  {id:2,  name:"Peri-Peri Chicken Wings",  cat:"starter", price:89.00,  desc:"Crispy wings with house peri-peri sauce, 6 pcs",              veg:false, hot:true},
  {id:3,  name:"Chakalaka Spring Rolls",   cat:"starter", price:65.00,  desc:"Crispy rolls filled with chakalaka relish",                   veg:true,  hot:false},
  {id:4,  name:"Boerewors Bites",          cat:"starter", price:72.00,  desc:"Grilled mini boerewors with two dipping sauces",             veg:false, hot:false},
  {id:5,  name:"Umngqusho Soup",           cat:"starter", price:55.00,  desc:"Warm samp and bean soup with sour cream",                    veg:true,  hot:false},
  {id:6,  name:"Bunny Chow (Mutton)",      cat:"main",    price:119.00, desc:"Traditional Durban bunny chow with mutton curry",             veg:false, hot:true},
  {id:7,  name:"Bunny Chow (Veg)",         cat:"main",    price:95.00,  desc:"Durban bunny chow with spiced vegetables",                   veg:true,  hot:true},
  {id:8,  name:"Chakalaka Burger",         cat:"main",    price:105.00, desc:"Beef patty, chakalaka, cheddar, brioche bun, fries",         veg:false, hot:false},
  {id:9,  name:"Boerewors Roll",           cat:"main",    price:85.00,  desc:"Classic SA street food with tomato and onion relish",        veg:false, hot:false},
  {id:10, name:"Pap & Wors",              cat:"main",    price:95.00,  desc:"Pap, boerewors, tomato relish, side salad",                  veg:false, hot:false},
  {id:11, name:"Durban Prawn Curry",       cat:"main",    price:189.00, desc:"Spicy Durban prawn curry with rice and roti",                veg:false, hot:true},
  {id:12, name:"Chicken Schnitzel",        cat:"main",    price:135.00, desc:"Crumbed chicken breast, chips, coleslaw",                    veg:false, hot:false},
  {id:13, name:"Vegetarian Bobotie",       cat:"main",    price:98.00,  desc:"Cape Malay bobotie with lentils, yellow rice, chutney",     veg:true,  hot:false},
  {id:14, name:"Grilled Kingklip",         cat:"main",    price:215.00, desc:"Line fish, lemon butter sauce, seasonal vegetables",         veg:false, hot:false},
  {id:15, name:"Braai Platter (2 pax)",   cat:"main",    price:299.00, desc:"Chops, boerewors, chicken, pap, garlic bread",              veg:false, hot:false},
  {id:16, name:"Malva Pudding",            cat:"dessert", price:58.00,  desc:"Warm malva pudding, vanilla custard or ice cream",           veg:true,  hot:false},
  {id:17, name:"Koeksister",               cat:"dessert", price:38.00,  desc:"Two syrup-soaked plaited doughnuts",                         veg:true,  hot:false},
  {id:18, name:"Milk Tart",               cat:"dessert", price:45.00,  desc:"Traditional melktert with cinnamon dusting",                 veg:true,  hot:false},
  {id:19, name:"Amarula Cheesecake",       cat:"dessert", price:72.00,  desc:"Baked cheesecake with Amarula cream, chocolate crumb",      veg:true,  hot:false},
  {id:20, name:"Peppermint Crisp Tart",   cat:"dessert", price:52.00,  desc:"Classic South African no-bake tart",                        veg:true,  hot:false},
  {id:21, name:"Rooibos Iced Tea",         cat:"drink",   price:35.00,  desc:"Sweetened rooibos, lemon, fresh mint",                       veg:true,  hot:false},
  {id:22, name:"Mango Lassi",              cat:"drink",   price:42.00,  desc:"Fresh mango, yoghurt, cardamom",                             veg:true,  hot:false},
  {id:23, name:"Craft Lager (500ml)",      cat:"drink",   price:58.00,  desc:"Local craft lager on tap",                                   veg:true,  hot:false},
  {id:24, name:"Springbokkies",            cat:"drink",   price:45.00,  desc:"Layered crème de menthe and Amarula shot",                   veg:true,  hot:false},
  {id:25, name:"Still Water (750ml)",      cat:"drink",   price:22.00,  desc:"Chilled still water",                                        veg:true,  hot:false},
  {id:26, name:"Sparkling Water (750ml)", cat:"drink",   price:25.00,  desc:"Chilled sparkling water",                                    veg:true,  hot:false},
  {id:27, name:"Cape Winelands Red",       cat:"drink",   price:85.00,  desc:"Glass of house Cabernet Sauvignon",                          veg:true,  hot:false},
  {id:28, name:"Cape Winelands White",     cat:"drink",   price:85.00,  desc:"Glass of house Chenin Blanc",                                veg:true,  hot:false},
  {id:29, name:"Amarula on Ice",           cat:"drink",   price:65.00,  desc:"Amarula cream liqueur served over ice",                      veg:true,  hot:false},
  {id:30, name:"Freshly Squeezed OJ",     cat:"drink",   price:38.00,  desc:"Orange juice, freshly pressed",                              veg:true,  hot:false},
];

// ── RENDER MENU ────────────────────────────────────────────
function renderMenu() {
  const grid = document.getElementById('menuGrid');
  grid.innerHTML = MENU.map(item => `
    <div class="menu-card" data-cat="${item.cat}" id="card-${item.id}">
      <div>
        <div class="menu-card-header">
          <div class="menu-card-name">${item.name}</div>
          <div class="menu-card-price">R${item.price.toFixed(2)}</div>
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

function filterMenu(cat, btn) {
  document.querySelectorAll('.tab-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  document.querySelectorAll('.menu-card').forEach(card => {
    card.classList.toggle('hidden', cat !== 'all' && card.dataset.cat !== cat);
  });
}

// ── CART ───────────────────────────────────────────────────
const cart = {};   // { itemId: quantity }
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
  const ids = Object.keys(cart);
  const badge  = document.getElementById('cartBadge');
  const items  = document.getElementById('cartItems');
  const footer = document.getElementById('cartFooter');
  const totals = document.getElementById('cartTotals');

  const totalQty = ids.reduce((s, id) => s + cart[id], 0);
  badge.textContent = totalQty === 0 ? '0 items' : `${totalQty} item${totalQty>1?'s':''}`;

  if (ids.length === 0) {
    items.innerHTML = '<div class="cart-empty">Your order is empty.<br/>Add dishes from the menu above.</div>';
    footer.style.display = 'none';
    return;
  }

  items.innerHTML = ids.map(id => {
    const item = MENU.find(m => m.id == id);
    const sub  = item.price * cart[id];
    return `<div class="cart-item">
      <div class="cart-item-name">${item.name}</div>
      <div class="cart-item-qty">
        <button class="qty-btn" onclick="changeQty(${id}, -1)">−</button>
        <span>${cart[id]}</span>
        <button class="qty-btn" onclick="changeQty(${id}, +1)">+</button>
      </div>
      <div class="cart-item-price">R${sub.toFixed(2)}</div>
    </div>`;
  }).join('');

  const subtotal = ids.reduce((s, id) => s + MENU.find(m=>m.id==id).price * cart[id], 0);
  const vat      = subtotal * 0.15;
  const service  = subtotal * 0.10;
  const total    = subtotal + vat + service;

  totals.innerHTML = `
    <div class="total-line"><span>Subtotal</span><span>R${subtotal.toFixed(2)}</span></div>
    <div class="total-line"><span>VAT (15%)</span><span>R${vat.toFixed(2)}</span></div>
    <div class="total-line"><span>Service (10%)</span><span>R${service.toFixed(2)}</span></div>
    <div class="total-line grand"><span>TOTAL</span><span>R${total.toFixed(2)}</span></div>
  `;
  footer.style.display = 'block';
}

function toggleCart() {
  cartCollapsed = !cartCollapsed;
  document.getElementById('cartSidebar').classList.toggle('collapsed', cartCollapsed);
}

function placeOrder() {
  showToast('Order sent to the kitchen! 🍳');
  Object.keys(cart).forEach(k => delete cart[k]);
  renderCart();
}

// ── TOAST ─────────────────────────────────────────────────
function showToast(msg) {
  const t = document.getElementById('toast');
  t.textContent = msg;
  t.classList.add('show');
  setTimeout(() => t.classList.remove('show'), 2000);
}

// ── RESERVATION VALIDATION ──────────────────────────────
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

function submitReservation() {
  // Set minimum date to today
  const today = new Date().toISOString().split('T')[0];
  document.getElementById('date').min = today;

  let valid = true;
  valid &= validate('firstName', 'firstNameErr', v => v.trim().length >= 2,   'Please enter your first name.');
  valid &= validate('lastName',  'lastNameErr',  v => v.trim().length >= 2,   'Please enter your last name.');
  valid &= validate('email',     'emailErr',     v => /\S+@\S+\.\S+/.test(v), 'Please enter a valid email.');
  valid &= validate('phone',     'phoneErr',     v => /^\d{10}$/.test(v.replace(/\s/g,'')), 'Enter a 10-digit SA phone number.');
  valid &= validate('date',      'dateErr',      v => v && v >= today,         'Please select a future date.');
  valid &= validate('time',      'timeErr',      v => v !== '',                'Please select a time.');
  valid &= validate('guests',    'guestsErr',    v => v !== '',                'Please select number of guests.');

  if (valid) {
    document.getElementById('reservationForm').style.display = 'none';
    document.querySelector('.btn-submit').style.display = 'none';
    document.getElementById('successMsg').style.display = 'block';
  }
}

// ── INIT ───────────────────────────────────────────────────
renderMenu();
renderCart();