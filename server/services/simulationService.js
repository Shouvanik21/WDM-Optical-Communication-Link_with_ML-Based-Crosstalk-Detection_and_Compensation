const generateSimulation = () => {
  const fiberLoss = 10;
  const dispersion = 85;

  const snr = Number((10 + Math.random() * 5).toFixed(4));

  const crosstalkDb = Number((-5 - Math.random() * 5).toFixed(4));

  const berBefore = Number((0.04 + Math.random() * 0.04).toFixed(4));

  const berAfter = Number(
    (berBefore * (0.05 + Math.random() * 0.1)).toFixed(4),
  );

  const berImprovement = Number(
    (((berBefore - berAfter) / berBefore) * 100).toFixed(2),
  );

  const severity = "CRITICAL";

  const confidence = Number((90 + Math.random() * 8).toFixed(2));

  return {
    fiberLoss,
    dispersion,
    snr,
    receivedPower: 0.00000001,
    noiseLevel: 0.00002,
    crosstalkDb,
    berBefore,
    berAfter,
    berImprovement,
    severity,
    confidence,
  };
};

module.exports = {
  generateSimulation,
};
