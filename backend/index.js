const express = require("express");
const cors = require("cors");

const app = express();
app.use(cors());
const port = 3001;

app.get("/api/status", (req, res) => {
  res.json({ message: "Backend is running!" });
});

app.listen(port, () => {
  console.log(`Backend listening at http://localhost:${port}`);
});
