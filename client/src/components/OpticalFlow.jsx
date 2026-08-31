import {
  Radio,
  GitBranch,
  Waves,
  AlertTriangle,
  Cpu,
  ArrowRight,
  Split,
  Activity,
  ShieldCheck,
} from "lucide-react";

const OpticalFlow = () => {
  const mainFlow = [
    {
      icon: Radio,
      title: "4 Channels",
      label: "λ₁  λ₂  λ₃  λ₄",
      text: "Independent optical signals are generated using different wavelengths.",
      color: "text-blue-400",
      border: "border-blue-400/30",
    },
    {
      icon: GitBranch,
      title: "WDM MUX",
      label: "MULTIPLEX",
      text: "Combines multiple wavelengths into one optical signal for transmission.",
      color: "text-indigo-400",
      border: "border-indigo-400/30",
    },
    {
      icon: Waves,
      title: "Optical Fiber",
      label: "50 km LINK",
      text: "All wavelength channels travel together through the same fiber.",
      color: "text-cyan-400",
      border: "border-cyan-400/30",
    },
    {
      icon: Split,
      title: "WDM DEMUX",
      label: "SEPARATE",
      text: "Separates the combined optical signal back into individual channels.",
      color: "text-purple-400",
      border: "border-purple-400/30",
    },
    {
      icon: Activity,
      title: "Receiver",
      label: "OPTICAL → ELECTRICAL",
      text: "Converts the selected optical signal into an electrical signal for detection.",
      color: "text-green-400",
      border: "border-green-400/30",
    },
  ];

  const analysisFlow = [
    {
      icon: AlertTriangle,
      title: "Crosstalk",
      text: "Unwanted energy from neighboring wavelengths interferes with the target signal.",
      color: "text-red-400",
      border: "border-red-400/30",
      bg: "bg-red-500/10",
    },
    {
      icon: Cpu,
      title: "ML Detection",
      text: "The trained model analyses SNR, BER, power, dispersion and crosstalk to predict severity.",
      color: "text-orange-400",
      border: "border-orange-400/30",
      bg: "bg-orange-500/10",
    },
    {
      icon: ShieldCheck,
      title: "Compensation",
      text: "Detected interference is reduced to improve the received signal and lower BER.",
      color: "text-emerald-400",
      border: "border-emerald-400/30",
      bg: "bg-emerald-500/10",
    },
  ];

  return (
    <section className="bg-slate-900 rounded-2xl p-6 md:p-8 text-white shadow-lg">
      {/* Header */}
      <div className="mb-7">
        <div className="flex items-center gap-2">
          <div className="w-2 h-2 bg-blue-400 rounded-full" />

          <h2 className="text-lg font-semibold">How the Optical Link Works</h2>
        </div>

        <p className="text-slate-400 text-sm mt-2 max-w-4xl leading-6">
          WDM allows multiple optical channels to share the same fiber. During
          transmission, neighboring channels can interfere with each other and
          create crosstalk. This system measures the link quality, uses machine
          learning to detect the severity, and then compensates for the
          interference.
        </p>
      </div>
      {/* ============================= */}
      {/* COMPLETE OPTICAL FLOW */}
      {/* ============================= */}
      <div className="mb-3">
        <p className="text-xs font-semibold tracking-wider text-slate-500 uppercase">
          Optical Transmission Flow
        </p>
      </div>
      <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3">
        {mainFlow.map((step, index) => {
          const Icon = step.icon;

          return (
            <div key={step.title} className="flex items-center flex-1">
              <div
                className={`w-full bg-slate-800 border ${step.border} rounded-xl p-4 hover:bg-slate-750 transition`}
              >
                <div className="flex items-center justify-between">
                  <Icon className={`w-6 h-6 ${step.color}`} />

                  <span className="text-[10px] font-semibold text-slate-500 tracking-wide">
                    {step.label}
                  </span>
                </div>

                <h3 className="font-semibold text-sm mt-3">{step.title}</h3>

                <p className="text-xs text-slate-400 mt-1 leading-5">
                  {step.text}
                </p>
              </div>

              {index < mainFlow.length - 1 && (
                <ArrowRight className="hidden lg:block w-5 h-5 text-slate-600 mx-2 flex-shrink-0" />
              )}
            </div>
          );
        })}
      </div>
      {/* Wavelength representation */}
      <div className="mt-5 flex flex-wrap items-center justify-center gap-2">
        <span className="text-xs text-slate-500 mr-2">
          Wavelength channels:
        </span>

        {["λ₁", "λ₂", "λ₃", "λ₄"].map((wave) => (
          <span
            key={wave}
            className="px-3 py-1 rounded-full bg-blue-500/10 border border-blue-400/20 text-xs text-blue-300"
          >
            {wave}
          </span>
        ))}
      </div>
      {/* ============================= */}
      {/* CROSSTALK BRANCH */}
      {/* ============================= */}
      <div className="flex justify-center my-5">
        <div className="h-8 border-l-2 border-dashed border-red-400/50" />
      </div>
      <div className="bg-red-500/5 border border-red-400/20 rounded-xl p-5">
        <div className="flex flex-col md:flex-row md:items-center gap-4">
          <div className="flex-shrink-0">
            <div className="w-11 h-11 rounded-lg bg-red-500/10 flex items-center justify-center">
              <AlertTriangle className="w-6 h-6 text-red-400" />
            </div>
          </div>

          <div>
            <div className="flex items-center gap-2">
              <h3 className="font-semibold text-sm text-red-300">CROSSTALK</h3>

              <span className="text-[10px] px-2 py-1 rounded-full bg-red-500/10 text-red-300 border border-red-400/20">
                INTERFERENCE
              </span>
            </div>

            <p className="text-xs text-slate-400 mt-1 leading-5">
              During transmission, energy from one wavelength can leak into
              another channel. This unwanted interference can distort the target
              signal and increase the probability of bit errors.
            </p>
          </div>
        </div>
      </div>
      {/* Arrow to ML */}
      <div className="flex justify-center my-5">
        <div className="h-8 border-l-2 border-dashed border-orange-400/50" />
      </div>
      {/* ============================= */}
      {/* INTELLIGENT ANALYSIS FLOW */}
      {/* ============================= */}
      <div className="mb-3">
        <p className="text-xs font-semibold tracking-wider text-slate-500 uppercase">
          Intelligent Detection & Recovery
        </p>
      </div>
      <div className="flex flex-col lg:flex-row items-stretch lg:items-center gap-3">
        {analysisFlow.map((step, index) => {
          const Icon = step.icon;

          return (
            <div key={step.title} className="flex items-center flex-1">
              <div
                className={`w-full ${step.bg} border ${step.border} rounded-xl p-5`}
              >
                <Icon className={`w-6 h-6 ${step.color} mb-3`} />

                <h3 className={`font-semibold text-sm ${step.color}`}>
                  {step.title}
                </h3>

                <p className="text-xs text-slate-400 mt-1 leading-5">
                  {step.text}
                </p>
              </div>

              {index < analysisFlow.length - 1 && (
                <ArrowRight className="hidden lg:block w-5 h-5 text-slate-600 mx-2 flex-shrink-0" />
              )}
            </div>
          );
        })}
      </div>
      {/* ============================= */}
      {/* ML FEATURES */}
      {/* ============================= */}
      <div className="mt-6 bg-slate-800/70 border border-slate-700 rounded-xl p-5">
        <div className="flex items-center gap-2 mb-4">
          <Cpu className="w-5 h-5 text-orange-400" />

          <h3 className="text-sm font-semibold">What the ML Model Looks At</h3>
        </div>

        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
          {[
            "SNR",
            "BER",
            "Crosstalk",
            "Received Power",
            "Fiber Loss",
            "Dispersion",
            "Noise Level",
            "Crosstalk Ratio",
          ].map((feature) => (
            <div
              key={feature}
              className="bg-slate-900 border border-slate-700 rounded-lg px-3 py-2"
            >
              <p className="text-xs text-slate-300">{feature}</p>
            </div>
          ))}
        </div>

        <p className="text-xs text-slate-500 mt-4 leading-5">
          These measurements are provided to the trained machine-learning model,
          which classifies the optical link condition as{" "}
          <span className="text-green-400">NORMAL</span>,{" "}
          <span className="text-yellow-400">WARNING</span>, or{" "}
          <span className="text-red-400">CRITICAL</span>.
        </p>
      </div>
      {/* ============================= */}
      {/* WHY CROSSTALK MATTERS */}
      {/* ============================= */}
      <div className="mt-5 bg-blue-500/10 border border-blue-400/20 rounded-xl px-4 py-4">
        <p className="text-sm text-blue-200 leading-6">
          <span className="font-semibold">Why crosstalk matters:</span> WDM
          increases the number of signals that can travel through one fiber, but
          closely packed wavelength channels can interfere with each other. More
          interference can reduce signal quality and cause bit errors. The goal
          of this project is to{" "}
          <span className="font-semibold">
            detect, predict and compensate for that degradation.
          </span>
        </p>
      </div>
      {/* ============================= */}
      {/* SIMPLE END-TO-END SUMMARY */}
      {/* ============================= */}
      <div className="mt-5 pt-5 border-t border-slate-800">
        <p className="text-center text-xs text-slate-500 mb-3">
          Complete system flow
        </p>

        <div className="flex flex-wrap items-center justify-center gap-2 text-xs">
          {[
            "λ₁ λ₂ λ₃ λ₄",
            "WDM MUX",
            "Fiber",
            "Crosstalk",
            "WDM DEMUX",
            "Receiver",
            "ML Detection",
            "Compensation",
            "Improved BER",
          ].map((item, index, array) => (
            <div key={item} className="flex items-center gap-2">
              <span className="px-3 py-1.5 rounded-lg bg-slate-800 border border-slate-700 text-slate-300">
                {item}
              </span>

              {index < array.length - 1 && (
                <ArrowRight className="w-3 h-3 text-slate-600" />
              )}
            </div>
          ))}
        </div>
      </div>
    </section>
  );
};

export default OpticalFlow;
