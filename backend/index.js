const express = require("express");
const cors = require("cors");
const multer = require("multer");

const app = express();
const port = 3001;

app.use(cors());
app.use(express.json());

const upload = multer();

app.get("/api/status", (req, res) => {
  res.json({ status: "Backend is running!" });
});

app.get("/api/generate-api-key", (req, res) => {
  const apiKey = "generated-api-key"; // replace with actual key generation logic
  res.json({ apiKey: apiKey });
});

app.post("/api/userQuery", (req, res) => {
  const query = req.body.query;
  // replace with actual query processing logic
  res.json({ response: `Response to the query: ${query}` });
});

app.post("/api/validateLease", upload.single("file"), (req, res) => {
  const leaseText = req.file ? req.file.buffer.toString() : req.body.leaseText;
  // replace with actual lease validation logic
  res.json({ details: `Validated lease text: ${leaseText}` });
});

app.post("/api/log", (req, res) => {
  const query = req.body.query;
  // replace with actual query processing logic
  res.json({ response: `thanks for logging : ${query}` });
});

app.post("/api/feedback", (req, res) => {
  const query = req.body.query;
  // replace with actual query processing logic
  res.json({ response: `feedback response to : ${query}` });
});

app.listen(port, () => {
  console.log(`Backend is running on port ${port}`);
});
