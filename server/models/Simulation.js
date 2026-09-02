const mongoose = require("mongoose");

const simulationSchema = new mongoose.Schema(
  {
    fiberLoss: {
      type: Number,
      required: true,
    },

    dispersion: {
      type: Number,
      required: true,
    },

    snr: {
      type: Number,
      required: true,
    },

    receivedPower: {
      type: Number,
      required: true,
    },

    noiseLevel: {
      type: Number,
      required: true,
    },

    crosstalkDb: {
      type: Number,
      required: true,
    },

    berBefore: {
      type: Number,
      required: true,
    },

    bitErrors: {
      type: Number,
      required: true,
    },

    berAfter: {
      type: Number,
      required: true,
    },

    berImprovement: {
      type: Number,
      required: true,
    },

    severity: {
      type: String,
      enum: ["NORMAL", "WARNING", "CRITICAL"],
      required: true,
    },

    // ==========================================
    // ML Prediction Probabilities
    // ==========================================

    probabilities: {
      NORMAL: {
        type: Number,
        required: true,
      },

      WARNING: {
        type: Number,
        required: true,
      },

      CRITICAL: {
        type: Number,
        required: true,
      },
    },

    // Confidence of the predicted class
    confidence: {
      type: Number,
      required: true,
    },
  },

  {
    timestamps: true,
  },
);

module.exports = mongoose.model("Simulation", simulationSchema);
