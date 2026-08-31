import { Activity, AlertTriangle, Gauge, Waves } from "lucide-react";

const icons = {
  SNR: Activity,
  Crosstalk: AlertTriangle,
  BER: Gauge,
  "Fiber Loss": Waves,
};

const ResultCard = ({ title, value, unit, description }) => {
  const Icon = icons[title] || Activity;

  return (
    <div className="group bg-white border border-slate-200 rounded-2xl p-5 shadow-sm hover:shadow-md hover:-translate-y-0.5 transition-all duration-200">
      <div className="flex items-center justify-between">
        <div className="p-2.5 bg-slate-100 rounded-xl group-hover:bg-blue-50 transition">
          <Icon className="w-5 h-5 text-slate-700 group-hover:text-blue-600" />
        </div>

        <span className="text-xs font-medium text-slate-400 uppercase tracking-wider">
          Measurement
        </span>
      </div>

      <p className="text-sm text-slate-500 mt-5">{title}</p>

      <div className="flex items-baseline gap-2 mt-1">
        <h2 className="text-3xl font-bold text-slate-900">{value}</h2>

        {unit && (
          <span className="text-sm font-medium text-slate-500">{unit}</span>
        )}
      </div>

      {description && (
        <p className="text-xs text-slate-400 mt-2">{description}</p>
      )}
    </div>
  );
};

export default ResultCard;
