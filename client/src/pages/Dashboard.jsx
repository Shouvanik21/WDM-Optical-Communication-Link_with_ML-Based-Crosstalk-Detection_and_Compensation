import { useEffect, useState } from "react";
import Header from "../components/Header";
import ResultCard from "../components/ResultCard";
import OpticalFlow from "../components/OpticalFlow";
import MLDetection from "../components/MLDetection";
import CompensationCard from "../components/CompensationCard";
import InfoSection from "../components/InfoSection";

const API_URL =
  import.meta.env.VITE_API_URL || "http://localhost:5000/api/auth";

const Dashboard = () => {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // ==========================================
  // Load latest simulation
  // ==========================================

  const loadLatestSimulation = async () => {
    try {
      const response = await fetch(`${API_URL}/getlatestsimulation`);

      if (!response.ok) {
        throw new Error("Failed to load latest simulation");
      }

      const data = await response.json();

      setResult(data.data || data.result || data);
    } catch (error) {
      console.log(error);
    }
  };

  // ==========================================
  // Run simulation
  // ==========================================

  const runSimulation = async () => {
    setLoading(true);
    setError("");

    try {
      const response = await fetch(`${API_URL}/runsimulation`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
      });

      if (!response.ok) {
        throw new Error("Simulation failed");
      }

      const data = await response.json();

      setResult(data.data || data.result || data);
    } catch (error) {
      console.error(error);

      setError("Unable to run simulation. Make sure the backend is running.");
    } finally {
      setLoading(false);
    }
  };

  // ==========================================
  // Load latest result
  // ==========================================

  useEffect(() => {
    loadLatestSimulation();
  }, []);

  // ==========================================
  // Helper
  // ==========================================

  const getValue = (key, fallback = 0) => {
    if (!result) return fallback;

    return (
      result[key] ??
      result.results?.[key] ??
      result.simulation?.[key] ??
      fallback
    );
  };

  // ==========================================
  // ML severity
  // ==========================================

  const severity =
    result?.severity ||
    result?.predictedSeverity ||
    result?.prediction?.severity ||
    "N/A";

  // ==========================================
  // BER
  // ==========================================

  const berBefore = Number(getValue("berBefore", 0));

  const berAfter = Number(getValue("berAfter", 0));

  const improvement = Number(
    result?.berImprovement ??
      result?.improvement ??
      (berBefore > 0 ? ((berBefore - berAfter) / berBefore) * 100 : 0),
  );

  // ==========================================
  // Render
  // ==========================================

  return (
    <div className="min-h-screen bg-slate-50">
      <Header />

      <main className="max-w-7xl mx-auto px-4 sm:px-6 py-6 md:py-8">
        {/* ================================== */}
        {/* Page Header */}
        {/* ================================== */}

        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5 mb-7">
          <div>
            <p className="text-xs font-semibold uppercase tracking-widest text-blue-600">
              Simulation Dashboard
            </p>

            <h2 className="text-2xl md:text-3xl font-bold text-slate-900 mt-1">
              Optical Link Analysis
            </h2>

            <p className="text-slate-500 mt-1">
              Monitor signal quality, detect crosstalk and evaluate ML-based
              compensation.
            </p>
          </div>

          <button
            onClick={runSimulation}
            disabled={loading}
            className="inline-flex items-center justify-center bg-slate-950 text-white px-6 py-3 rounded-xl font-semibold shadow-sm hover:bg-slate-800 disabled:opacity-50 disabled:cursor-not-allowed transition"
          >
            {loading ? "Running Simulation..." : "Run Simulation"}
          </button>
        </div>

        {/* ================================== */}
        {/* Error */}
        {/* ================================== */}

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 p-4 rounded-xl mb-6">
            {error}
          </div>
        )}

        {/* ================================== */}
        {/* Optical Explanation */}
        {/* ================================== */}

        <OpticalFlow />

        {/* ================================== */}
        {/* Main Measurements */}
        {/* ================================== */}

        <div className="mt-7">
          <div className="mb-4">
            <h2 className="text-lg font-semibold text-slate-900">
              Optical Link Measurements
            </h2>

            <p className="text-sm text-slate-500 mt-1">
              Real-time measurements generated by the WDM simulation.
            </p>
          </div>

          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-5">
            <ResultCard
              title="SNR"
              value={Number(getValue("snr", 0)).toFixed(2)}
              unit="dB"
              description="Signal-to-noise ratio"
            />

            <ResultCard
              title="Crosstalk"
              value={Number(getValue("crosstalkDb", 0)).toFixed(2)}
              unit="dB"
              description="Inter-channel interference"
            />

            <ResultCard
              title="BER"
              value={berBefore.toFixed(4)}
              description="Bit error rate"
            />

            <ResultCard
              title="Fiber Loss"
              value={Number(getValue("fiberLoss", 0)).toFixed(2)}
              unit="dB"
              description="Optical power lost in fiber"
            />
          </div>
        </div>

        {/* ================================== */}
        {/* ML Detection */}
        {/* ================================== */}

        <div className="mt-7">
          <MLDetection
            severity={severity}
            probabilities={result?.probabilities}
            confidence={getValue("confidence", 0)}
          />
        </div>

        {/* ================================== */}
        {/* Compensation */}
        {/* ================================== */}

        <div className="mt-7">
          <CompensationCard
            berBefore={berBefore}
            berAfter={berAfter}
            improvement={improvement}
          />
        </div>

        {/* ================================== */}
        {/* Additional Measurements */}
        {/* ================================== */}

        <div className="mt-7">
          <InfoSection
            dispersion={getValue("dispersion", 0)}
            receivedPower={getValue("receivedPower", 0)}
            bitErrors={getValue("bitErrors", 0)}
          />
        </div>

        {/* ================================== */}
        {/* Footer Explanation */}
        {/* ================================== */}

        <div className="text-center py-7 pb-2">
          <p className="text-xs text-slate-400">
            WDM Optical Communication • ML Crosstalk Detection • Signal
            Compensation
          </p>
        </div>
      </main>
    </div>
  );
};

export default Dashboard;
