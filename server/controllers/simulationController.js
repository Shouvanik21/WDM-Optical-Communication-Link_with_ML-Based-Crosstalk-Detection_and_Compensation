const Simulation = require("../models/Simulation");

const { runPythonSimulation } = require("../services/simulationService");

const runSimulation = async (req, res) => {
  try {
    console.log("Starting Python WDM simulation...");

    const simulationData = await runPythonSimulation();

    const simulation = await Simulation.create(simulationData);

    console.log("Python simulation completed successfully.");

    res.status(201).json({
      success: true,
      message: "WDM simulation completed successfully",
      data: simulation,
    });
  } catch (error) {
    console.error("Simulation Error:", error.message);

    res.status(500).json({
      success: false,
      message: "WDM simulation failed",
      error: error.message,
    });
  }
};

const getSimulations = async (req, res) => {
  try {
    const simulations = await Simulation.find().sort({
      createdAt: -1,
    });

    if (simulations.length == 0) {
      return res.staus(404).json({
        success: false,
        message: "No simulation found",
      });
    }

    res.status(200).json({
      success: true,
      count: simulations.length,
      data: simulations,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch simulations",
      error: error.message,
    });
  }
};

const getLatestSimulation = async (req, res) => {
  try {
    const simulation = await Simulation.findOne().sort({
      createdAt: -1,
    });

    if (!simulation) {
      return res.status(404).json({
        success: false,
        message: "No simulation found",
      });
    }

    res.status(200).json({
      success: true,
      data: simulation,
    });
  } catch (error) {
    res.status(500).json({
      success: false,
      message: "Failed to fetch latest simulation",
      error: error.message,
    });
  }
};

module.exports = {
  runSimulation,
  getSimulations,
  getLatestSimulation,
};
