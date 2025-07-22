const express = require("express");
const router = express.Router();
const db = require("./db");

router.post("/orders", (req, res) => {
  const orders = req.body;

  if (!Array.isArray(orders) || orders.length === 0) {
    return res.status(400).json({ error: "訂單資料錯誤" });
  }

  const values = orders.map(o => [o.product, o.quantity, o.price, o.subtotal]);

  const sql = "INSERT INTO orders (product, quantity, price, subtotal) VALUES ?";
  db.query(sql, [values], (err, result) => {
    if (err) return res.status(500).json({ error: "寫入失敗", err });
    res.json({ message: "訂單已儲存", inserted: result.affectedRows });
  });
});

module.exports = router;
