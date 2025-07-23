let orders = [];
let editIndex = null;

const menuData = {
  "主餐": [
    { name: "紅燒牛肉麵", price: 130 },
    { name: "雞腿便當", price: 110 },
    { name: "排骨飯", price: 100 },
    { name: "滷肉飯", price: 70 },
    { name: "蔬食炒飯", price: 90 },
    { name: "蕃茄義大利麵", price: 140 },
    { name: "照燒雞排飯", price: 105 },
    { name: "炸豬排定食", price: 150 },
    { name: "咖哩飯", price: 100 },
    { name: "日式壽司便當", price: 130 },
    { name: "三杯雞便當", price: 115 },
    { name: "起司蛋包飯", price: 120 }
  ],
  "湯品": [
    { name: "香菇雞湯", price: 95 },
    { name: "味噌湯", price: 40 }
  ],
  "飲料": [
    { name: "珍珠奶茶", price: 50 },
    { name: "炸雞塊套餐", price: 105 }
  ],
  "小菜": [
    { name: "滷味拼盤", price: 90 },
    { name: "烤雞沙拉", price: 120 },
    { name: "炒泡麵", price: 80 },
    { name: "花雕雞煲", price: 160 }
  ]
};

function switchPage(pageId) {
  document.querySelectorAll(".page").forEach((p) => p.classList.remove("active"));
  document.getElementById(pageId).classList.add("active");
}

function renderMenu() {
  const container = document.getElementById("menuContainer");
  container.innerHTML = "";
  for (const category in menuData) {
    const categoryDiv = document.createElement("div");
    categoryDiv.className = "category";
    categoryDiv.innerHTML = `<h3>${category}</h3>`;
    const menuListDiv = document.createElement("div");
    menuListDiv.className = "menu-list";

    menuData[category].forEach((item) => {
      const itemDiv = document.createElement("div");
      itemDiv.className = "menu-item";
      itemDiv.innerHTML = `
        <div class="menu-item-name">${item.name}</div>
        <div class="menu-item-price">$${item.price}</div>
      `;
      itemDiv.onclick = () => {
        document.getElementById("product").value = item.name;
        document.getElementById("price").value = item.price;
        document.getElementById("quantity").value = 1;
      };
      menuListDiv.appendChild(itemDiv);
    });

    categoryDiv.appendChild(menuListDiv);
    container.appendChild(categoryDiv);
  }
}

function addOrder() {
  const product = document.getElementById("product").value.trim();
  const quantity = parseInt(document.getElementById("quantity").value);
  const price = parseInt(document.getElementById("price").value);

  if (!product || quantity <= 0 || price < 0 || isNaN(price) || isNaN(quantity)) {
    alert("請輸入正確的餐點資訊！");
    return;
  }

  const order = { product, quantity, price, subtotal: quantity * price };

  if (editIndex !== null) {
    orders[editIndex] = order;
    editIndex = null;
  } else {
    orders.push(order);
  }
  renderTable();
  clearInputs();
}

function renderTable() {
  const table = document.getElementById("orderTable");
  table.innerHTML = "";

  let total = 0;

  orders.forEach((item, index) => {
    total += item.subtotal;
    const row = `<tr>
      <td>${item.product}</td>
      <td>${item.quantity}</td>
      <td>$${item.price}</td>
      <td>$${item.subtotal}</td>
      <td>
        <span class="delete-btn" onclick="editOrder(${index})">修改</span> |
        <span class="delete-btn" onclick="deleteOrder(${index})">刪除</span>
      </td>
    </tr>`;
    table.innerHTML += row;
  });

  document.getElementById("total").innerText = `$${total}`;
}

function editOrder(index) {
  const item = orders[index];
  document.getElementById("product").value = item.product;
  document.getElementById("quantity").value = item.quantity;
  document.getElementById("price").value = item.price;
  editIndex = index;
}

function deleteOrder(index) {
  orders.splice(index, 1);
  renderTable();
}

function clearInputs() {
  document.getElementById("product").value = "";
  document.getElementById("quantity").value = 1;
  document.getElementById("price").value = 0;
}

function checkout() {
  if (orders.length === 0) {
    alert("訂單為空！");
    return;
  }

  fetch("http://localhost:3000/api/orders", {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify(orders),
  })
    .then(res => res.json())
    .then(data => {
      alert("訂單已送出！\n" + data.message);
      orders = [];
      renderTable();
    })
    .catch(err => {
      console.error("送出失敗：", err);
      alert("送出訂單失敗！");
    });
}


renderMenu();
