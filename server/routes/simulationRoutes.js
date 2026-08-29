const express = require("express");
const router = express.Router();

const {
  runSimulation,
  getSimulations,
  getLatestSimulation,
} = require("../controllers/simulationController");

router.post("/runsimulation", runSimulation);
router.get("/getsimulations", getSimulations);
router.get("/getlatestsimulation", getLatestSimulation);

module.exports = router;
