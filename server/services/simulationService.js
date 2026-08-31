const { spawn } = require("child_process");
const path = require("path");

const runPythonSimulation = () => {
  return new Promise((resolve, reject) => {
    const pythonProjectPath = path.resolve(__dirname, "../../python");

    const pythonProcess = spawn("python", ["main.py"], {
      cwd: pythonProjectPath,
    });

    let output = "";
    let errorOutput = "";

    pythonProcess.stdout.on("data", (data) => {
      output += data.toString();
    });

    pythonProcess.stderr.on("data", (data) => {
      errorOutput += data.toString();
    });

    pythonProcess.on("close", (code) => {
      if (code !== 0) {
        return reject(
          new Error(errorOutput || `Python process exited with code ${code}`),
        );
      }

      try {
        const result = parsePythonOutput(output);

        resolve(result);
      } catch (error) {
        reject(error);
      }
    });
  });
};

const parsePythonOutput = (output) => {
  const fiberLossMatch = output.match(/Fiber Loss\s*:\s*([-+]?\d*\.?\d+)/);

  const dispersionMatch = output.match(/Dispersion\s*:\s*([-+]?\d*\.?\d+)/);

  const snrMatch = output.match(/SNR\s*:\s*([-+]?\d*\.?\d+)/);

  const receivedPowerMatch = output.match(
    /Received Power\s*:\s*([-+]?\d*\.?\d+)/,
  );

  const noiseMatch = output.match(/Noise Level\s*:\s*([-+]?\d*\.?\d+)/);

  const crosstalkMatch = output.match(/Crosstalk\s*:\s*([-+]?\d*\.?\d+)/);

  const berMatch = output.match(/BER\s*:\s*([-+]?\d*\.?\d+)/);
  const bitErrorsMatch = output.match(
  /Bit Errors\s*:\s*([-+]?\d+)/
);

  const severityMatch = output.match(
    /Predicted Severity:\s*(NORMAL|WARNING|CRITICAL)/,
  );

  const confidenceMatch = output.match(/CRITICAL\s*:\s*([\d.]+)%/);

  const berBeforeMatch = output.match(/BER Before\s*:\s*([-+]?\d*\.?\d+)/);

  const berAfterMatch = output.match(/BER After\s*:\s*([-+]?\d*\.?\d+)/);

  const improvementMatch = output.match(
    /BER Improvement\s*:\s*([-+]?\d*\.?\d+)%/,
  );

  if (
    !fiberLossMatch ||
    !dispersionMatch ||
    !snrMatch ||
    !crosstalkMatch ||
    !berMatch ||
    !severityMatch ||
    !berBeforeMatch ||
    !berAfterMatch ||
    !improvementMatch
  ) {
    throw new Error("Unable to parse Python simulation output.");
  }

  return {
    fiberLoss: Number(fiberLossMatch[1]),

    dispersion: Number(dispersionMatch[1]),

    snr: Number(snrMatch[1]),

    receivedPower: receivedPowerMatch ? Number(receivedPowerMatch[1]) : 0,

    noiseLevel: noiseMatch ? Number(noiseMatch[1]) : 0,

    crosstalkDb: Number(crosstalkMatch[1]),

    berBefore: Number(berBeforeMatch[1]),

bitErrors: Math.round(Number(berBeforeMatch[1]) * 1000),

    berAfter: Number(berAfterMatch[1]),

    berImprovement: Number(improvementMatch[1]),

    severity: severityMatch[1],

    confidence: confidenceMatch ? Number(confidenceMatch[1]) : 0,
  };
};

module.exports = {
  runPythonSimulation,
};
