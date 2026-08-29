const express = require("express");
const cors = require("cors");
const dotenv = require("dotenv");
dotenv.config();

const connectDB = require("./config/db");
const simulationRoutes = require("./routes/simulationRoutes");

const app = express();

connectDB();
app.use(cors());
app.use(express.json());

app.get("/", (req, res) => {
  res.json({
    message: "WDM Optical Communication API is running",
  });
});

app.use("/api/auth", simulationRoutes);

const PORT = process.env.PORT || 5000;

app.listen(PORT, () => {
  console.log(`Server is running on port ${PORT}`);
});
