import { Activity, Radio } from "lucide-react";

const Header = () => {
  return (
    <header className="bg-slate-950 text-white border-b border-slate-800">
      <div className="max-w-7xl mx-auto px-6 py-6">
        <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-5">
          <div className="flex items-start gap-4">
            <div className="p-3 bg-blue-500/10 border border-blue-400/20 rounded-xl">
              <Radio className="w-7 h-7 text-blue-400" />
            </div>

            <div>
              <h1 className="text-2xl md:text-3xl font-bold tracking-tight">
                Intelligent WDM Optical Communication
              </h1>

              <p className="text-slate-400 mt-1">
                ML-Based Crosstalk Detection & Compensation
              </p>
            </div>
          </div>

          <div className="flex items-center gap-2 text-sm text-emerald-400 bg-emerald-400/10 border border-emerald-400/20 px-4 py-2 rounded-full w-fit">
            <Activity className="w-4 h-4" />
            Optical Link Monitoring
          </div>
        </div>
      </div>
    </header>
  );
};

export default Header;
