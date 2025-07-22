const express = require("express");
const cors = require("cors");
const bodyParser = require("body-parser");
const app = express();
const routes = require("./routes");

app.use(cors());
app.use(bodyParser.json());

app.use("/api", routes);

const PORT = 3000;
app.listen(PORT, () => {
  console.log(`🚀 伺服器啟動：http://localhost:${PORT}`);
});
