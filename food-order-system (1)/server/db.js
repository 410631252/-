const mysql = require("mysql");

const db = mysql.createConnection({
  host: "localhost",
  user: "root",
  password: "",       // 請依你的設定調整
  database: "food_order",
});

db.connect((err) => {
  if (err) throw err;
  console.log("✅ MySQL 連線成功！");
});

module.exports = db;
