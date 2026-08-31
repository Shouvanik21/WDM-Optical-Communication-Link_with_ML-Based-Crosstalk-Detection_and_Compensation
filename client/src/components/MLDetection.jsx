import { Brain, CheckCircle, AlertTriangle, ShieldAlert } from "lucide-react";

const MLDetection = ({ severity, probabilities, confidence }) => {
  const severityConfig = {
    NORMAL: {
      icon: CheckCircle,
      color: "text-emerald-600",
      bg: "bg-emerald-50",
      border: "border-emerald-200",
      label: "Optical link is operating normally",
    },

    WARNING: {
      icon: AlertTriangle,
      color: "text-yellow-600",
      bg: "bg-yellow-50",
      border: "border-yellow-200",
      label: "Moderate crosstalk detected",
    },

    CRITICAL: {
      icon: ShieldAlert,
      color: "text-red-600",
      bg: "bg-red-50",
      border: "border-red-200",
      label: "Severe crosstalk detected",
    },
  };

  const config = severityConfig[severity] || severityConfig.NORMAL;

  const Icon = config.icon;

  const values = probabilities || {
    NORMAL: severity === "NORMAL" ? 1 : 0,
    WARNING: severity === "WARNING" ? 1 : 0,
    CRITICAL: severity === "CRITICAL" ? 1 : 0,
  };

  return (
    <section className="bg-white border border-slate-200 rounded-2xl shadow-sm overflow-hidden">
      <div className="p-6 border-b border-slate-100">
        <div className="flex items-center gap-3">
          <div className="p-2.5 bg-purple-50 rounded-xl">
            <Brain className="w-6 h-6 text-purple-600" />
          </div>

          <div>
            <h2 className="text-lg font-semibold text-slate-900">
              ML Crosstalk Detection
            </h2>

            <p className="text-sm text-slate-500">
              Machine learning assessment of optical link quality
            </p>
          </div>
        </div>
      </div>

      <div className="p-6">
        <div
          className={`flex flex-col sm:flex-row sm:items-center justify-between gap-4 p-5 rounded-xl border ${config.bg} ${config.border}`}
        >
          <div className="flex items-center gap-4">
            <Icon className={`w-9 h-9 ${config.color}`} />

            <div>
              <p className="text-xs uppercase tracking-wider text-slate-500 font-medium">
                Predicted Severity
              </p>

              <h3 className={`text-3xl font-bold mt-1 ${config.color}`}>
                {severity || "N/A"}
              </h3>
            </div>
          </div>

          {confidence !== undefined && (
            <div className="text-left sm:text-right">
              <p className="text-xs text-slate-500">Prediction Confidence</p>

              <p className="text-2xl font-bold text-slate-900 mt-1">
                {Number(confidence).toFixed(2)}%
              </p>
            </div>
          )}
        </div>

        <p className="text-sm text-slate-500 mt-4">
          {config.label}. The model evaluates measured optical parameters and
          classifies the link condition.
        </p>

        <div className="mt-6">
          <div className="flex justify-between mb-4">
            <h3 className="font-semibold text-slate-800">
              Prediction Probabilities
            </h3>

            <span className="text-xs text-slate-400">ML model output</span>
          </div>

          <div className="space-y-4">
            {["NORMAL", "WARNING", "CRITICAL"].map((name) => {
              const value = Number(values[name] || 0);

              return (
                <div key={name}>
                  <div className="flex justify-between text-sm mb-1.5">
                    <span className="font-medium text-slate-600">{name}</span>

                    <span className="font-semibold text-slate-800">
                      {(value * 100).toFixed(2)}%
                    </span>
                  </div>

                  <div className="w-full h-2.5 bg-slate-100 rounded-full overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all duration-500 ${
                        name === "CRITICAL"
                          ? "bg-red-500"
                          : name === "WARNING"
                            ? "bg-yellow-500"
                            : "bg-emerald-500"
                      }`}
                      style={{
                        width: `${Math.min(value * 100, 100)}%`,
                      }}
                    />
                  </div>
                </div>
              );
            })}
          </div>
        </div>
      </div>
    </section>
  );
};

export default MLDetection;
